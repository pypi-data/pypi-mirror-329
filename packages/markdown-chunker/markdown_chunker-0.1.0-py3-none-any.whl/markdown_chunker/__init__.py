"""
Markdown Chunker package for splitting markdown documents into chunks while preserving structure.

The main class is MarkdownChunkingStrategy, which implements the chunking algorithm.
"""

from .chunking_strategy import MarkdownChunkingStrategy
from .content_handlers import (
    ContentHandler,
    HeadingHandler,
    TableHandler,
    CodeBlockHandler,
    ListHandler,
    BlockquoteHandler,
    ParagraphHandler,
    FootnoteHandler,
    HtmlHandler,
    YamlFrontMatterHandler,
)

__all__ = [
    "MarkdownChunkingStrategy",
    "ContentHandler",
    "HeadingHandler",
    "TableHandler",
    "CodeBlockHandler",
    "ListHandler",
    "BlockquoteHandler",
    "ParagraphHandler",
    "FootnoteHandler",
    "HtmlHandler",
    "YamlFrontMatterHandler",
]

__version__ = "0.1.0"
