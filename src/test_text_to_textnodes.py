import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    
    def test_assignment_example(self):
        """Test the provided assignment example"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        self.assertEqual(len(result), len(expected))
        for i, (actual, expected_node) in enumerate(zip(result, expected)):
            with self.subTest(i=i):
                self.assertEqual(actual.text, expected_node.text)
                self.assertEqual(actual.text_type, expected_node.text_type)
                self.assertEqual(actual.url, expected_node.url)
    
    def test_plain_text_only(self):
        """Test text with no formatting"""
        text = "This is just plain text with no formatting"
        result = text_to_textnodes(text)
        
        expected = [TextNode("This is just plain text with no formatting", TextType.PLAIN)]
        self.assertEqual(result, expected)
    
    def test_bold_only(self):
        """Test text with only bold formatting"""
        text = "This has **bold text** in it"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.PLAIN),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in it", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    def test_italic_only(self):
        """Test text with only italic formatting"""
        text = "This has _italic text_ in it"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.PLAIN),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    def test_code_only(self):
        """Test text with only code formatting"""
        text = "This has `code text` in it"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.PLAIN),
            TextNode("code text", TextType.CODE),
            TextNode(" in it", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    def test_image_only(self):
        """Test text with only an image"""
        text = "This has an ![image](https://example.com/image.jpg) in it"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("This has an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" in it", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    def test_link_only(self):
        """Test text with only a link"""
        text = "This has a [link](https://example.com) in it"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("This has a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in it", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_same_type(self):
        """Test multiple instances of the same formatting type"""
        text = "This has **bold1** and **bold2** text"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.PLAIN),
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("bold2", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    def test_adjacent_formatting(self):
        """Test adjacent formatting with no text between"""
        text = "**bold**_italic_`code`"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)
    
    def test_formatting_at_boundaries(self):
        """Test formatting at the beginning and end"""
        text = "**start bold** middle _end italic_"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("start bold", TextType.BOLD),
            TextNode(" middle ", TextType.PLAIN),
            TextNode("end italic", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)
    
    def test_mixed_images_and_links(self):
        """Test text with both images and links"""
        text = "Check out ![image](https://example.com/img.jpg) and visit [website](https://example.com)"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("Check out ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" and visit ", TextType.PLAIN),
            TextNode("website", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)
    
    def test_all_formatting_types(self):
        """Test text with all possible formatting types"""
        text = "Text **bold** _italic_ `code` ![img](url1) [link](url2) end"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("Text ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.PLAIN),
            TextNode("img", TextType.IMAGE, "url1"),
            TextNode(" ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "url2"),
            TextNode(" end", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    
    def test_nested_syntax_not_processed(self):
        """Test that we don't process nested formatting (as specified)"""
        # The ** inside the image alt text should not be processed as bold
        text = "![alt with **stars**](url) and more text"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("alt with **stars**", TextType.IMAGE, "url"),
            TextNode(" and more text", TextType.PLAIN),
        ]
        self.assertEqual(result, expected)
    
    
    def test_complex_urls(self):
        """Test images and links with complex URLs"""
        text = "![complex](https://cdn.example.com/img.jpg?w=800&h=600) and [API](https://api.example.com/v1/data?limit=10)"
        result = text_to_textnodes(text)
        
        expected = [
            TextNode("complex", TextType.IMAGE, "https://cdn.example.com/img.jpg?w=800&h=600"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("API", TextType.LINK, "https://api.example.com/v1/data?limit=10"),
        ]
        self.assertEqual(result, expected)
    
    def test_real_world_paragraph(self):
        """Test a realistic paragraph with mixed formatting"""
        text = """Welcome to our `Python` **tutorial**! This guide covers _advanced techniques_ 
        for web development. Check out our ![logo](https://example.com/logo.png) and 
        visit [our docs](https://docs.example.com) for more `code examples`."""
        
        result = text_to_textnodes(text)
        
        # Verify we got the right types and count
        text_nodes = [n for n in result if n.text_type == TextType.PLAIN]
        bold_nodes = [n for n in result if n.text_type == TextType.BOLD]
        italic_nodes = [n for n in result if n.text_type == TextType.ITALIC]
        code_nodes = [n for n in result if n.text_type == TextType.CODE]
        image_nodes = [n for n in result if n.text_type == TextType.IMAGE]
        link_nodes = [n for n in result if n.text_type == TextType.LINK]
        
        self.assertEqual(len(bold_nodes), 1)
        self.assertEqual(bold_nodes[0].text, "tutorial")
        
        self.assertEqual(len(italic_nodes), 1)
        self.assertEqual(italic_nodes[0].text, "advanced techniques")
        
        self.assertEqual(len(code_nodes), 2)
        self.assertEqual(code_nodes[0].text, "Python")
        self.assertEqual(code_nodes[1].text, "code examples")
        
        self.assertEqual(len(image_nodes), 1)
        self.assertEqual(image_nodes[0].text, "logo")
        self.assertEqual(image_nodes[0].url, "https://example.com/logo.png")
        
        self.assertEqual(len(link_nodes), 1)
        self.assertEqual(link_nodes[0].text, "our docs")
        self.assertEqual(link_nodes[0].url, "https://docs.example.com")
    
    def test_empty_string_input(self):
        """Test empty string input"""
        result = text_to_textnodes("")
        # Empty string gets filtered out during processing
        expected = []
        self.assertEqual(result, expected)
    
    def test_whitespace_only(self):
        """Test whitespace-only input"""
        text = "   \n\t  "
        result = text_to_textnodes(text)
        expected = [TextNode("   \n\t  ", TextType.PLAIN)]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()