# Sample Markdown Document

This is a sample Markdown document that demonstrates various Markdown elements and how they are handled by our chunking strategy.

## Headings and Paragraphs

Here's a paragraph with some text. It includes **bold text**, *italic text*, and `inline code`. The paragraph continues with more text to demonstrate how longer paragraphs are handled by the chunking strategy.

### Subheading

Another paragraph under a subheading. This helps demonstrate how headings are preserved and how content is organized around them.

## Code Blocks

Here's a Python code block:

```python
def example_function():
    """This is a sample function."""
    print("Hello, World!")
    
    for i in range(10):
        print(f"Count: {i}")
    
    return True
```

## Tables

Here's a sample table:

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |
| Value 7  | Value 8  | Value 9  |

## Lists

Here's an ordered list:

1. First item
2. Second item
   - Subitem 1
   - Subitem 2
3. Third item
   1. Nested ordered item 1
   2. Nested ordered item 2

And an unordered list:

- Main item 1
  - Subitem A
  - Subitem B
- Main item 2
  - Subitem C
  - Subitem D

## Blockquotes

Here's a blockquote:

> This is a blockquote that contains multiple lines of text.
> It demonstrates how blockquotes are handled by the chunking strategy.
> 
> It even includes multiple paragraphs to show how paragraph breaks
> within blockquotes are preserved.

## Links and Images

Here are some [links](https://example.com) and ![images](https://example.com/image.jpg).

## Mixed Content

This section demonstrates how different types of content are handled when mixed together:

1. First, a list item
2. Then, some code:
   ```python
   print("Inside a list")
   ```
3. Followed by a table:
   | Col 1 | Col 2 |
   |-------|--------|
   | Data  | More   |

> And a blockquote within the list
> with multiple lines

## Repeating Headers and Footers

---
Page 1 Header
---

Some content for page 1.

---
Page 1 Footer
---

---
Page 1 Header
---

Some content for page 2.

---
Page 1 Footer
---

## Duplicate Content

This content will appear multiple times:

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

This content will appear multiple times:

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

## Final Section

This is the final section of our sample document. It includes enough text to demonstrate how the chunking strategy handles content near the end of the document. 