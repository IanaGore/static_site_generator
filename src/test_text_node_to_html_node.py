import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode
from text_node_to_html_node import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):
    
    def test_text(self):
        """Test provided example: plain text conversion"""
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_to_html_output(self):
        """Test that plain text produces correct HTML output"""
        node = TextNode("Plain text", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Plain text")
    
    def test_bold(self):
        """Test bold text conversion"""
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)
    
    def test_bold_to_html_output(self):
        """Test that bold text produces correct HTML output"""
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")
    
    def test_italic(self):
        """Test italic text conversion"""
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.props)
    
    def test_italic_to_html_output(self):
        """Test that italic text produces correct HTML output"""
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")
    
    def test_code(self):
        """Test code text conversion"""
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertIsNone(html_node.props)
    
    def test_code_to_html_output(self):
        """Test that code text produces correct HTML output"""
        node = TextNode("console.log('test')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>console.log('test')</code>")
    
    def test_link(self):
        """Test link conversion"""
        node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
    
    def test_link_to_html_output(self):
        """Test that link produces correct HTML output"""
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Google</a>')
    
    def test_link_no_url_raises_error(self):
        """Test that link without URL raises ValueError"""
        node = TextNode("Bad link", TextType.LINK, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Link TextNode must have a URL")
    
    def test_image(self):
        """Test image conversion"""
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Images have empty value
        self.assertEqual(html_node.props, {
            "src": "https://example.com/image.jpg",
            "alt": "Alt text"
        })
    
    def test_image_to_html_output(self):
        """Test that image produces correct HTML output"""
        node = TextNode("A beautiful sunset", TextType.IMAGE, "https://example.com/sunset.jpg")
        html_node = text_node_to_html_node(node)
        result = html_node.to_html()
        # Check structure
        self.assertTrue(result.startswith('<img '))
        self.assertTrue(result.endswith('></img>'))
        # Check attributes
        self.assertIn('src="https://example.com/sunset.jpg"', result)
        self.assertIn('alt="A beautiful sunset"', result)
    
    def test_image_no_url_raises_error(self):
        """Test that image without URL raises ValueError"""
        node = TextNode("Alt text", TextType.IMAGE, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Image TextNode must have a URL")
    
    def test_return_type_is_leafnode(self):
        """Test that all conversions return LeafNode instances"""
        test_cases = [
            TextNode("Text", TextType.PLAIN),
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("Code", TextType.CODE),
            TextNode("Link", TextType.LINK, "https://example.com"),
            TextNode("Image", TextType.IMAGE, "https://example.com/img.jpg")
        ]
        
        for text_node in test_cases:
            html_node = text_node_to_html_node(text_node)
            self.assertIsInstance(html_node, LeafNode)
    
    def test_complex_conversion_chain(self):
        """Test converting multiple TextNodes and combining their HTML"""
        text_nodes = [
            TextNode("Start with ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text, plus a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.PLAIN)
        ]
        
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        combined_html = "".join(node.to_html() for node in html_nodes)
        
        expected = 'Start with <b>bold</b> and <i>italic</i> text, plus a <a href="https://example.com">link</a>.'
        self.assertEqual(combined_html, expected)
    
    def test_special_characters_preserved(self):
        """Test that special characters in text are preserved"""
        special_text = "Text with <special> & characters"
        node = TextNode(special_text, TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, special_text)
        self.assertEqual(html_node.to_html(), special_text)
    
    def test_empty_text_allowed(self):
        """Test that empty text is allowed for text types"""
        node = TextNode("", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), "")
    
    def test_empty_text_in_tags(self):
        """Test empty text in HTML tags"""
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b></b>")
    
    def test_url_variations(self):
        """Test different URL formats"""
        url_test_cases = [
            "https://www.example.com",
            "http://localhost:3000",
            "ftp://files.example.com",
            "mailto:user@example.com",
            "/relative/path",
            "#anchor-link"
        ]
        
        for url in url_test_cases:
            link_node = TextNode("Link text", TextType.LINK, url)
            html_node = text_node_to_html_node(link_node)
            self.assertEqual(html_node.props["href"], url)
            
            image_node = TextNode("Alt text", TextType.IMAGE, url)
            html_node = text_node_to_html_node(image_node)
            self.assertEqual(html_node.props["src"], url)


if __name__ == "__main__":
    unittest.main()

