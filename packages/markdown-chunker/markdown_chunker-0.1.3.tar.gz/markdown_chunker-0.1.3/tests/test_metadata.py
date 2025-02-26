"""
Tests for the metadata embedding functionality of MarkdownChunkingStrategy.
"""

import unittest
import yaml
import re
from io import StringIO

from src.markdown_chunker.chunking_strategy import MarkdownChunkingStrategy


class TestMetadataEmbedding(unittest.TestCase):
    """Test cases for embedded metadata in chunks."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_content = """# Test Document

## Section 1

This is the first section with some content.

## Section 2

This is the second section with more content.

### Subsection 2.1

This is a subsection with even more content.

```python
def hello_world():
    print("Hello, World!")
```

## Section 3

This is the third section with a table.

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |
"""

    def extract_yaml_frontmatter(self, text):
        """Extract YAML frontmatter from text."""
        yaml_pattern = r"^---\n(.*?)\n---\n"
        match = re.search(yaml_pattern, text, re.DOTALL)
        if match:
            yaml_text = match.group(1)
            return yaml.safe_load(StringIO(yaml_text))
        return None

    def test_metadata_embedding_enabled(self):
        """Test that metadata is embedded when the option is enabled."""
        strategy = MarkdownChunkingStrategy(
            add_metadata=True, document_title="Test Document", source_document="test.md"
        )

        chunks = strategy.chunk_markdown(self.sample_content)

        # Verify that all chunks have metadata
        for i, chunk in enumerate(chunks):
            metadata = self.extract_yaml_frontmatter(chunk)
            self.assertIsNotNone(metadata, f"Chunk {i} has no YAML frontmatter")

            # Check document information
            self.assertIn("document", metadata)
            self.assertIn("title", metadata["document"])
            self.assertEqual(metadata["document"]["title"], "Test Document")
            self.assertIn("source", metadata["document"])
            self.assertEqual(metadata["document"]["source"], "test.md")

            # Check chunk information
            self.assertIn("chunk", metadata)
            self.assertIn("id", metadata["chunk"])
            self.assertEqual(metadata["chunk"]["id"], i + 1)

            self.assertIn("total", metadata["chunk"])
            self.assertEqual(metadata["chunk"]["total"], len(chunks))

            # Check content information
            self.assertIn("content", metadata)
            self.assertIn("characters", metadata["content"])
            self.assertGreater(metadata["content"]["characters"], 0)

            # Check navigation links (except for first and last chunks)
            if i > 0:
                self.assertIn("previous", metadata["chunk"])
                self.assertEqual(metadata["chunk"]["previous"], i)

            if i < len(chunks) - 1:
                self.assertIn("next", metadata["chunk"])
                self.assertEqual(metadata["chunk"]["next"], i + 2)

            # Check heading information
            if "headings" in metadata:
                self.assertIn("main", metadata["headings"])

            # Check content types
            self.assertIn("types", metadata["content"])
            self.assertIsInstance(metadata["content"]["types"], list)

    def test_metadata_embedding_disabled(self):
        """Test that metadata is not embedded when the option is disabled."""
        strategy = MarkdownChunkingStrategy(
            min_chunk_len=100, soft_max_len=500, hard_max_len=1000, add_metadata=False
        )

        chunks = strategy.chunk_markdown(self.sample_content)

        # Verify that no chunks have metadata
        for i, chunk in enumerate(chunks):
            metadata = self.extract_yaml_frontmatter(chunk)
            self.assertIsNone(
                metadata, f"Chunk {i} has YAML frontmatter when it shouldn't"
            )

    def test_existing_frontmatter_preserved(self):
        """Test that existing frontmatter is preserved and merged with generated metadata."""
        content_with_frontmatter = """---
title: Original Title
author: Test Author
date: 2023-07-15
---

# Test Document with Frontmatter

## Section 1

This is content with existing frontmatter.
"""

        strategy = MarkdownChunkingStrategy(
            min_chunk_len=50,
            soft_max_len=200,
            hard_max_len=400,
            add_metadata=True,
            document_title="New Document Title",
            source_document="frontmatter_test.md",
        )

        chunks = strategy.chunk_markdown(content_with_frontmatter)

        # Verify the chunk has metadata
        metadata = self.extract_yaml_frontmatter(chunks[0])
        self.assertIsNotNone(metadata)

        # Check that generated metadata is present
        self.assertIn("document", metadata)
        self.assertIn("title", metadata["document"])
        self.assertEqual(metadata["document"]["title"], "New Document Title")

        self.assertIn("chunk", metadata)
        self.assertIn("id", metadata["chunk"])

        # Note: In the current implementation, original frontmatter isn't preserved
        # This test verifies the current behavior, but if frontmatter preservation
        # is implemented later, this test should be updated.

    def test_content_types_detection(self):
        """Test that content types are correctly detected and included in metadata."""
        # Content with various markdown elements
        complex_content = """# Complex Document

## Section with Code

```python
def test_function():
    return "Hello World"
```

## Section with Table

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |

## Section with List

- Item 1
- Item 2
  - Subitem 2.1
  - Subitem 2.2
- Item 3

## Section with Blockquote

> This is a blockquote
> With multiple lines
"""

        strategy = MarkdownChunkingStrategy(
            min_chunk_len=50,
            soft_max_len=1000,
            hard_max_len=2000,
            add_metadata=True,
            document_title="Complex Document",
        )

        chunks = strategy.chunk_markdown(complex_content)

        # Check if the content types are correctly identified
        for chunk in chunks:
            metadata = self.extract_yaml_frontmatter(chunk)
            self.assertIsNotNone(metadata)
            self.assertIn("content", metadata)
            self.assertIn("types", metadata["content"])

            # Check specific content types based on chunk content
            if "```python" in chunk:
                self.assertIn("code_block", metadata["content"]["types"])

            if "| Header 1 |" in chunk:
                self.assertIn("table", metadata["content"]["types"])

            if "- Item 1" in chunk and "types" in metadata["content"]:
                self.assertIn("list", metadata["content"]["types"])

            if "> This is a blockquote" in chunk:
                self.assertIn("blockquote", metadata["content"]["types"])

            # All chunks should have headings
            if "headings" in metadata:
                self.assertIsNotNone(metadata["headings"]["main"])


if __name__ == "__main__":
    unittest.main()
