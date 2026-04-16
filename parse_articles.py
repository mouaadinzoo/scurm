from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


NOISE_PREFIXES = (
    "doi",
    "https://",
    "http://",
    "www.",
    "arxiv",
    "preprint",
    "copyright",
)

SECTION_HEADINGS = {
    "keywords",
    "index terms",
    "introduction",
    "related work",
    "materials and methods",
    "methodology",
    "methods",
    "background",
    "results",
    "discussion",
    "conclusion",
    "references",
}

AFFILIATION_HINTS = {
    "university",
    "department",
    "laboratory",
    "school",
    "faculty",
    "institute",
    "college",
    "center",
    "centre",
    "hospital",
    "research",
}

TITLE_CONTINUATION_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "from",
    "in",
    "of",
    "on",
    "the",
    "to",
    "using",
    "via",
    "with",
}


@dataclass(slots=True)
class ParsedArticle:
    source_filename: str
    title: str
    authors: str
    abstract: str


def normalize_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip(" \t-")


def text_lines(text: str) -> list[str]:
    lines = [normalize_line(line) for line in text.splitlines()]
    return [line for line in lines if line]


def is_noise_line(line: str) -> bool:
    lowered = line.lower()
    if lowered.startswith(NOISE_PREFIXES):
        return True
    if re.fullmatch(r"\d+", line):
        return True
    if len(line) <= 2:
        return True
    return False


def is_abstract_heading(line: str) -> bool:
    lowered = line.lower().strip()
    return lowered == "abstract" or lowered.startswith("abstract:")


def is_section_heading(line: str) -> bool:
    lowered = line.lower().strip(" :.")
    if lowered in SECTION_HEADINGS:
        return True
    if re.fullmatch(r"(?:\d+(?:\.\d+)*)\s+[a-z].*", lowered):
        return True
    if re.fullmatch(r"(?:[ivxlcdm]+)\.?\s+[a-z].*", lowered):
        return True
    if line.isupper() and len(line.split()) <= 6:
        return True
    return False


def looks_like_author_line(line: str) -> bool:
    cleaned = re.sub(r"[\d*†‡§]", "", line)
    if "@" in cleaned:
        return False
    tokens = re.findall(r"[A-Za-z][A-Za-z'`-]*", cleaned)
    if not 2 <= len(tokens) <= 18:
        return False

    lower_tokens = {token.lower() for token in tokens}
    if lower_tokens & AFFILIATION_HINTS:
        return False

    capitalized = sum(token[0].isupper() for token in tokens)
    connectors = cleaned.count(",") + cleaned.count("&")
    if " and " in cleaned.lower():
        connectors += 1

    if connectors > 0 and capitalized >= 2:
        return True

    return 2 <= len(tokens) <= 4 and capitalized == len(tokens)


def should_extend_title(title_lines: list[str], line: str) -> bool:
    words = line.split()
    if not 3 <= len(words) <= 14:
        return False
    if any(separator in line for separator in (",", "&")):
        return False
    if " and " in line.lower():
        return False
    if "." in line or ":" in line:
        return False

    previous_last_word = title_lines[-1].split()[-1].lower()
    if previous_last_word in TITLE_CONTINUATION_WORDS:
        return True

    return len(title_lines) == 1 and len(title_lines[0].split()) <= 6


def extract_abstract(lines: list[str]) -> str:
    for index, line in enumerate(lines):
        lowered = line.lower()
        if lowered == "abstract":
            start_index = index + 1
            prefix = ""
        elif lowered.startswith("abstract:"):
            start_index = index + 1
            prefix = line.split(":", 1)[1].strip()
        else:
            continue

        collected: list[str] = []
        if prefix:
            collected.append(prefix)

        for candidate in lines[start_index:]:
            if collected and is_section_heading(candidate):
                break
            collected.append(candidate)

        return " ".join(collected).strip()
    return ""


def extract_title_and_authors(lines: list[str]) -> tuple[str, str]:
    preface: list[str] = []
    for line in lines:
        if is_abstract_heading(line):
            break
        if not is_noise_line(line):
            preface.append(line)

    if not preface:
        return "", ""

    title_lines: list[str] = [preface[0]]
    remainder = preface[1:]

    for line in remainder:
        candidate_title = " ".join(title_lines + [line])
        if (
            len(title_lines) < 3
            and len(candidate_title) <= 220
            and should_extend_title(title_lines, line)
        ):
            title_lines.append(line)
            continue
        if looks_like_author_line(line):
            break
        if is_section_heading(line):
            break
        break

    title = " ".join(title_lines).strip()
    authors = ""

    title_count = len(title_lines)
    for line in preface[title_count:title_count + 6]:
        if looks_like_author_line(line):
            authors = line.strip()
            break

    return title, authors


def parse_article_text(text: str, source_filename: str) -> ParsedArticle:
    lines = text_lines(text)
    title, authors = extract_title_and_authors(lines)
    abstract = extract_abstract(lines)

    return ParsedArticle(
        source_filename=source_filename,
        title=title,
        authors=authors,
        abstract=abstract,
    )


def read_text_file(text_path: Path) -> str:
    return text_path.read_text(encoding="utf-8-sig", errors="ignore")


def source_pdf_name_from_text_file(text_path: Path) -> str:
    return f"{text_path.stem}.pdf"


def write_output(article: ParsedArticle, output_path: Path) -> None:
    payload = "\n".join(
        [
            article.source_filename,
            article.title,
            article.authors,
            article.abstract,
        ]
    )
    output_path.write_text(payload, encoding="utf-8")


def recreate_output_dir(output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def process_directory(input_dir: Path, output_subdir: str) -> tuple[int, Path]:
    text_files = sorted(path for path in input_dir.glob("*.txt") if path.is_file())
    if not text_files:
        raise FileNotFoundError(f"No TXT files found in '{input_dir}'.")

    output_dir = input_dir / output_subdir
    recreate_output_dir(output_dir)

    for text_path in text_files:
        article = parse_article_text(
            read_text_file(text_path),
            source_filename=source_pdf_name_from_text_file(text_path),
        )
        write_output(article, output_dir / text_path.name)

    return len(text_files), output_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse converted scientific TXT files into plain-text summaries."
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing TXT files produced by a PDF-to-text converter.",
    )
    parser.add_argument(
        "--output-subdir",
        default="parsed_output",
        help="Name of the subdirectory created inside input_dir.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    if not input_dir.is_dir():
        parser.error(f"'{input_dir}' is not a directory.")

    processed_count, output_dir = process_directory(input_dir, args.output_subdir)
    print(f"Processed {processed_count} TXT file(s).")
    print(f"Output directory: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
