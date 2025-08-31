import unittest
from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        """Test provided example: multiple block types"""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_single_block(self):
        """Test markdown with only one block"""
        md = "This is just a single paragraph with no blank lines."
        blocks = markdown_to_blocks(md)
        expected = ["This is just a single paragraph with no blank lines."]
        self.assertEqual(blocks, expected)
    
    def test_multiple_paragraphs(self):
        """Test multiple simple paragraphs"""
        md = """First paragraph here.

Second paragraph here.

Third paragraph here."""
        blocks = markdown_to_blocks(md)
        expected = [
            "First paragraph here.",
            "Second paragraph here.", 
            "Third paragraph here."
        ]
        self.assertEqual(blocks, expected)
    
    def test_heading_blocks(self):
        """Test various heading levels"""
        md = """# Main Heading

## Sub Heading

### Sub Sub Heading

Regular paragraph."""
        blocks = markdown_to_blocks(md)
        expected = [
            "# Main Heading",
            "## Sub Heading",
            "### Sub Sub Heading", 
            "Regular paragraph."
        ]
        self.assertEqual(blocks, expected)
    
    def test_list_blocks(self):
        """Test different list types"""
        md = """- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2

* Different bullet style
* Another item"""
        blocks = markdown_to_blocks(md)
        expected = [
            "- Unordered item 1\n- Unordered item 2",
            "1. Ordered item 1\n2. Ordered item 2",
            "* Different bullet style\n* Another item"
        ]
        self.assertEqual(blocks, expected)
    
    def test_code_block(self):
        """Test code blocks"""
        md = """Here's some code:

```python
def hello():
    print("Hello, world!")
```

And here's more text."""
        blocks = markdown_to_blocks(md)
        expected = [
            "Here's some code:",
            "```python\ndef hello():\n    print(\"Hello, world!\")\n```",
            "And here's more text."
        ]
        self.assertEqual(blocks, expected)
    
    def test_blockquote(self):
        """Test blockquote blocks"""
        md = """Regular paragraph.

> This is a blockquote
> It spans multiple lines
> All part of the same block

Another paragraph."""
        blocks = markdown_to_blocks(md)
        expected = [
            "Regular paragraph.",
            "> This is a blockquote\n> It spans multiple lines\n> All part of the same block",
            "Another paragraph."
        ]
        self.assertEqual(blocks, expected)
    
    def test_excessive_newlines(self):
        """Test handling of excessive newlines"""
        md = """Block 1


Block 2



Block 3"""
        blocks = markdown_to_blocks(md)
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(blocks, expected)
    
    def test_leading_trailing_whitespace(self):
        """Test stripping of leading and trailing whitespace"""
        md = """
  
  Block 1 with spaces  
  
  
  Block 2 with tabs	
  
  
"""
        blocks = markdown_to_blocks(md)
        expected = ["Block 1 with spaces", "Block 2 with tabs"]
        self.assertEqual(blocks, expected)
    
    def test_mixed_whitespace_in_blocks(self):
        """Test blocks with internal whitespace preservation"""
        md = """Block with  multiple   spaces

Block with
newline in middle

	Block with tabs	and  spaces"""
        blocks = markdown_to_blocks(md)
        expected = [
            "Block with  multiple   spaces",
            "Block with\nnewline in middle",
            "Block with tabs	and  spaces"  # Internal whitespace preserved
        ]
        self.assertEqual(blocks, expected)
    
    def test_empty_markdown(self):
        """Test empty markdown input"""
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])
    
    def test_only_whitespace(self):
        """Test markdown that is only whitespace"""
        md = "   \n\n\t\n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_single_newlines_preserved(self):
        """Test that single newlines within blocks are preserved"""
        md = """Multi-line paragraph
continues on this line
and this line too

Another block here"""
        blocks = markdown_to_blocks(md)
        expected = [
            "Multi-line paragraph\ncontinues on this line\nand this line too",
            "Another block here"
        ]
        self.assertEqual(blocks, expected)
    
    def test_complex_real_world_example(self):
        """Test a realistic markdown document"""
        md = """# My Blog Post

Welcome to my **awesome** blog post! This is the introduction paragraph.

## What You'll Learn

In this post, you'll learn about:

- Markdown parsing
- Block-level vs inline elements  
- Python implementation details

## Code Example

Here's a simple example:

```python
def parse_markdown(text):
    blocks = markdown_to_blocks(text)
    return blocks
```

That's all for now!

## Conclusion

Thanks for reading. Visit [my site](https://example.com) for more content.
"""
        blocks = markdown_to_blocks(md)
        
        # Verify we got the right number of blocks
        self.assertEqual(len(blocks), 8)
        
        # Verify specific blocks
        self.assertEqual(blocks[0], "# My Blog Post")
        self.assertTrue(blocks[1].startswith("Welcome to my"))
        self.assertEqual(blocks[2], "## What You'll Learn")
        self.assertTrue(blocks[3].startswith("In this post"))
        self.assertTrue(blocks[4].startswith("- Markdown parsing"))
        self.assertEqual(blocks[5], "## Code Example")
        self.assertTrue(blocks[6].startswith("Here's a simple example:"))
        self.assertTrue(blocks[7].startswith("```python"))
        
    def test_windows_line_endings(self):
        """Test handling of Windows-style line endings"""
        # Windows uses \r\n, but we should handle \n\n splitting
        md = "Block 1\r\n\r\nBlock 2\r\n\r\nBlock 3"
        blocks = markdown_to_blocks(md)
        # Note: This assumes the input has been normalized to \n
        # In a real implementation, you might want to handle \r\n explicitly
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(blocks, expected)
    
    def test_mixed_block_content(self):
        """Test blocks with mixed content types"""
        md = """# Heading with **bold** text

Paragraph with _italic_ and `code` and [links](url).

- List with **bold** item
- List with _italic_ item
- List with `code` item

> Blockquote with **bold** text
> And _italic_ text too"""
        
        blocks = markdown_to_blocks(md)
        expected = [
            "# Heading with **bold** text",
            "Paragraph with _italic_ and `code` and [links](url).",
            "- List with **bold** item\n- List with _italic_ item\n- List with `code` item",
            "> Blockquote with **bold** text\n> And _italic_ text too"
        ]
        self.assertEqual(blocks, expected)
    
    def test_preserve_internal_formatting(self):
        """Test that inline formatting is preserved within blocks"""
        md = """This paragraph has **bold**, _italic_, and `code`.

This list has formatting:
- **Bold** item
- _Italic_ item  
- `Code` item"""
        
        blocks = markdown_to_blocks(md)
        
        # Verify formatting is preserved as raw text (not processed)
        self.assertIn("**bold**", blocks[0])
        self.assertIn("_italic_", blocks[0])
        self.assertIn("`code`", blocks[0])
        self.assertIn("**Bold**", blocks[1])
        self.assertIn("_Italic_", blocks[1])
        self.assertIn("`Code`", blocks[1])


def identify_block_type(block):
    """
    Helper function to identify markdown block types.
    Not part of the assignment, just for demonstration.
    """
    if block.startswith('#'):
        return "Heading"
    elif block.startswith('```'):
        return "Code Block"
    elif block.startswith('>'):
        return "Blockquote"
    elif block.startswith(('- ', '* ', '+ ')):
        return "Unordered List"
    elif any(line.split('.', 1)[0].strip().isdigit() for line in block.split('\n') if '.' in line):
        return "Ordered List"
    else:
        return "Paragraph"


if __name__ == "__main__":
    unittest.main()