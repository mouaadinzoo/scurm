from __future__ import annotations

import unittest

from parse_articles import parse_article_text


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


if __name__ == "__main__":
    unittest.main()
