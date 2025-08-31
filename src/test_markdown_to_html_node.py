import unittest
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    
    def test_paragraphs(self):
        """Test provided example: multiple paragraphs"""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        """Test provided example: code block"""
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_single_paragraph(self):
        """Test single paragraph with inline formatting"""
        md = "This is a paragraph with **bold**, _italic_, and `code` text."
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><p>This is a paragraph with <b>bold</b>, <i>italic</i>, and <code>code</code> text.</p></div>"
        self.assertEqual(html, expected)
    
    def test_headings_all_levels(self):
        """Test all heading levels"""
        md = """# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        self.assertEqual(html, expected)
    
    def test_heading_with_inline_formatting(self):
        """Test heading with inline formatting"""
        md = "# Heading with **bold** and _italic_ text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading with <b>bold</b> and <i>italic</i> text</h1></div>"
        self.assertEqual(html, expected)
    
    def test_unordered_list(self):
        """Test unordered list"""
        md = """- First item
- Second item with **bold**
- Third item with _italic_"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i></li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_ordered_list(self):
        """Test ordered list"""
        md = """1. First item
2. Second item with `code`
3. Third item"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>First item</li><li>Second item with <code>code</code></li><li>Third item</li></ol></div>"
        self.assertEqual(html, expected)
    
    def test_quote_block(self):
        """Test blockquote"""
        md = """> This is a quote
> It spans multiple lines
> With **bold** text"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote\nIt spans multiple lines\nWith <b>bold</b> text</blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_code_block_with_language(self):
        """Test code block with language specification"""
        md = """```python
def hello():
    print("Hello, world!")
```"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><pre><code>def hello():\n    print("Hello, world!")\n</code></pre></div>'
        self.assertEqual(html, expected)
    
    def test_mixed_content_document(self):
        """Test document with all block types"""
        md = """# Main Title

This is an introduction paragraph.

## Features

Key features include:

- Easy to use
- Fast processing
- Great results

## Installation

Follow these steps:

1. Download package
2. Install it
3. Configure

```bash
npm install package
```

> Note: Read the docs first."""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Verify structure without checking exact HTML (too long)
        self.assertTrue(html.startswith("<div>"))
        self.assertTrue(html.endswith("</div>"))
        self.assertIn("<h1>Main Title</h1>", html)
        self.assertIn("<h2>Features</h2>", html)
        self.assertIn("<ul><li>Easy to use</li>", html)
        self.assertIn("<ol><li>Download package</li>", html)
        self.assertIn("<pre><code>npm install package\n</code></pre>", html)
        self.assertIn("<blockquote>Note: Read the docs first.</blockquote>", html)
    
    def test_links_and_images(self):
        """Test paragraph with links and images"""
        md = "Check out this ![cool image](https://example.com/image.jpg) and visit [our site](https://example.com)."
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected = '<div><p>Check out this <img src="https://example.com/image.jpg" alt="cool image"></img> and visit <a href="https://example.com">our site</a>.</p></div>'
        self.assertEqual(html, expected)
    
    def test_empty_markdown(self):
        """Test empty markdown input"""
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div></div>"
        self.assertEqual(html, expected)
    
    def test_whitespace_only_markdown(self):
        """Test markdown with only whitespace"""
        md = "   \n\n\t  "
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div></div>"
        self.assertEqual(html, expected)
    
    def test_single_heading(self):
        """Test document with only a heading"""
        md = "# Just a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Just a heading</h1></div>"
        self.assertEqual(html, expected)
    
    def test_nested_formatting_in_lists(self):
        """Test complex inline formatting within list items"""
        md = """- Item with **bold** and _italic_
- Item with `code` and [link](url)
- Item with ![image](img_url)"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertIn("<li>Item with <b>bold</b> and <i>italic</i></li>", html)
        self.assertIn('<li>Item with <code>code</code> and <a href="url">link</a></li>', html)
        self.assertIn('<li>Item with <img src="img_url" alt="image"></img></li>', html)
    
    def test_multiline_blocks_preserve_structure(self):
        """Test that different block types handle newlines appropriately"""
        md = """This is a paragraph
that spans multiple
lines but is still one block

> This is a quote
> that also spans
> multiple lines

- List item one
- List item two"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Paragraphs should convert internal newlines to spaces (standard markdown behavior)
        self.assertIn("<p>This is a paragraph that spans multiple lines but is still one block</p>", html)
        
        # Quotes should preserve newlines (multi-line quotes maintain structure)
        self.assertIn("<blockquote>This is a quote\nthat also spans\nmultiple lines</blockquote>", html)
    
    def test_code_block_preserves_formatting(self):
        """Test that code blocks preserve all formatting characters"""
        md = """```
def example():
    # This has markdown **bold** and _italic_
    # But should not be processed
    return "Hello > World"
```"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Verify that markdown inside code is not processed
        self.assertIn("**bold**", html)  # Should be literal, not <b>bold</b>
        self.assertIn("_italic_", html)  # Should be literal, not <i>italic</i>
        self.assertIn("> World", html)   # Should be literal, not quote
    
    def test_return_type_structure(self):
        """Test that the function returns the correct node structure"""
        md = "# Heading\n\nParagraph"
        node = markdown_to_html_node(md)
        
        # Should return a ParentNode with tag "div"
        from parentnode import ParentNode
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "div")
        
        # Should have 2 children (heading and paragraph)
        self.assertEqual(len(node.children), 2)
        
        # First child should be h1
        self.assertEqual(node.children[0].tag, "h1")
        
        # Second child should be p
        self.assertEqual(node.children[1].tag, "p")


if __name__ == "__main__":
    unittest.main()