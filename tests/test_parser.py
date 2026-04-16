from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from parse_articles import parse_article_text, process_directory


class ParseArticleTextTests(unittest.TestCase):
    def test_extracts_title_authors_and_abstract(self) -> None:
        text = """
        A Practical Parser for Scientific Articles
        John Doe, Jane Smith
        Abstract
        This paper presents a parser for scientific articles.
        Introduction
        The rest of the paper starts here.
        """

        parsed = parse_article_text(text, "paper.pdf")

        self.assertEqual(parsed.source_filename, "paper.pdf")
        self.assertEqual(parsed.title, "A Practical Parser for Scientific Articles")
        self.assertEqual(parsed.authors, "John Doe, Jane Smith")
        self.assertEqual(
            parsed.abstract,
            "This paper presents a parser for scientific articles.",
        )

    def test_extracts_inline_abstract_heading(self) -> None:
        text = """
        Multi Line Title for a Scientific Parser
        Alice Martin and Bob Leroy
        Abstract: This study evaluates a parser on several inputs.
        1 Introduction
        More content.
        """

        parsed = parse_article_text(text, "study.pdf")

        self.assertEqual(parsed.title, "Multi Line Title for a Scientific Parser")
        self.assertEqual(parsed.authors, "Alice Martin and Bob Leroy")
        self.assertEqual(
            parsed.abstract,
            "This study evaluates a parser on several inputs.",
        )

    def test_supports_multiline_titles(self) -> None:
        text = """
        A Robust Parser for
        Scientific Article Metadata
        John Doe
        Abstract
        Metadata extraction remains a practical problem.
        """

        parsed = parse_article_text(text, "metadata.pdf")

        self.assertEqual(
            parsed.title,
            "A Robust Parser for Scientific Article Metadata",
        )
        self.assertEqual(parsed.authors, "John Doe")
        self.assertEqual(
            parsed.abstract,
            "Metadata extraction remains a practical problem.",
        )

    def test_missing_sections_keep_empty_lines(self) -> None:
        text = """
        Minimal Example
        """

        parsed = parse_article_text(text, "minimal.pdf")

        self.assertEqual(parsed.title, "Minimal Example")
        self.assertEqual(parsed.authors, "")
        self.assertEqual(parsed.abstract, "")

    def test_process_directory_reads_txt_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir)
            source = input_dir / "paper.txt"
            source.write_text(
                "\n".join(
                    [
                        "A Practical Parser for Scientific Articles",
                        "John Doe, Jane Smith",
                        "Abstract",
                        "This paper presents a parser for scientific articles.",
                    ]
                ),
                encoding="utf-8",
            )

            processed_count, output_dir = process_directory(input_dir, "parsed_output")

            self.assertEqual(processed_count, 1)
            output_lines = (output_dir / "paper.txt").read_text(encoding="utf-8").splitlines()
            self.assertEqual(output_lines[0], "paper.pdf")
            self.assertEqual(output_lines[1], "A Practical Parser for Scientific Articles")
            self.assertEqual(output_lines[2], "John Doe, Jane Smith")
            self.assertEqual(
                output_lines[3],
                "This paper presents a parser for scientific articles.",
            )


if __name__ == "__main__":
    unittest.main()
