import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_basic_bold_split(self):
        """Test basic bold text splitting"""
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.PLAIN),
        ]
        
        self.assertEqual(len(result), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)
    
    def test_basic_code_split(self):
        """Test basic code text splitting"""
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        
        self.assertEqual(len(result), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)
    
    def test_basic_italic_split(self):
        """Test basic italic text splitting"""
        node = TextNode("This has _italic text_ in it", TextType.PLAIN)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        expected = [
            TextNode("This has ", TextType.PLAIN),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it", TextType.PLAIN),
        ]
        
        self.assertEqual(len(result), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)
    
    def test_multiple_delimiters(self):
        """Test text with multiple delimiter pairs"""
        node = TextNode("Start **bold1** middle **bold2** end", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("Start ", TextType.PLAIN),
            TextNode("bold1", TextType.BOLD),
            TextNode(" middle ", TextType.PLAIN),
            TextNode("bold2", TextType.BOLD),
            TextNode(" end", TextType.PLAIN),
        ]
        
        self.assertEqual(len(result), 5)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)
    
    def test_delimiter_at_start(self):
        """Test delimiter at the beginning of text"""
        node = TextNode("**bold** at start", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.PLAIN),
        ]
        
        self.assertEqual(len(result), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)
    
    def test_delimiter_at_end(self):
        """Test delimiter at the end of text"""
        node = TextNode("ends with **bold**", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("ends with ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
        ]
        
        self.assertEqual(len(result), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)
    
    def test_only_formatted_text(self):
        """Test text that is entirely within delimiters"""
        node = TextNode("**entirely bold**", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [TextNode("entirely bold", TextType.BOLD)]
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)
    
    def test_no_delimiters(self):
        """Test text with no delimiters (should remain unchanged)"""
        node = TextNode("Plain text with no formatting", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [TextNode("Plain text with no formatting", TextType.PLAIN)]
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)
    
    def test_non_text_nodes_unchanged(self):
        """Test that non-PLAIN nodes pass through unchanged"""
        nodes = [
            TextNode("Plain text with **bold**", TextType.PLAIN),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("Already code", TextType.CODE),
        ]
        
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        # First node should be split (was PLAIN type)
        self.assertEqual(result[0].text, "Plain text with ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        
        # Other nodes should be unchanged
        self.assertEqual(result[2].text, "Already bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "Already italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, "Already code")
        self.assertEqual(result[4].text_type, TextType.CODE)
    
    def test_empty_between_delimiters(self):
        """Test empty text between delimiters (should be skipped)"""
        node = TextNode("Text with **** empty bold", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Empty text between delimiters should be skipped
        # So we only get the parts before and after
        expected = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode(" empty bold", TextType.PLAIN),
        ]
        
        self.assertEqual(len(result), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(result[i].text, expected_node.text)
            self.assertEqual(result[i].text_type, expected_node.text_type)
    
    def test_unmatched_delimiter_raises_error(self):
        """Test that unmatched delimiter raises ValueError"""
        node = TextNode("Unmatched **bold text", TextType.PLAIN)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertIn("Unmatched delimiter", str(context.exception))
        self.assertIn("**", str(context.exception))
    
    def test_multiple_unmatched_delimiters(self):
        """Test multiple unmatched delimiters"""
        node = TextNode("**bold1** and **bold2", TextType.PLAIN)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertIn("Unmatched delimiter", str(context.exception))
    
    def test_chaining_multiple_delimiter_types(self):
        """Test chaining multiple delimiter processing"""
        # Start with text that has both bold and code
        original = [TextNode("Text with **bold** and `code` formatting", TextType.PLAIN)]
        
        # First pass: process bold
        after_bold = split_nodes_delimiter(original, "**", TextType.BOLD)
        expected_after_bold = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and `code` formatting", TextType.PLAIN),
        ]
        
        self.assertEqual(len(after_bold), 3)
        for i, expected in enumerate(expected_after_bold):
            self.assertEqual(after_bold[i].text, expected.text)
            self.assertEqual(after_bold[i].text_type, expected.text_type)
        
        # Second pass: process code (on the result of first pass)
        after_code = split_nodes_delimiter(after_bold, "`", TextType.CODE)
        expected_final = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" formatting", TextType.PLAIN),
        ]
        
        self.assertEqual(len(after_code), 5)
        for i, expected in enumerate(expected_final):
            self.assertEqual(after_code[i].text, expected.text)
            self.assertEqual(after_code[i].text_type, expected.text_type)
    
    def test_preserve_url_property(self):
        """Test that URL property is preserved in split nodes"""
        node = TextNode("Text with **bold**", TextType.PLAIN, "https://example.com")
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # All resulting nodes should preserve the original URL
        for result_node in result:
            self.assertEqual(result_node.url, "https://example.com")
    
    def test_empty_input_list(self):
        """Test empty input list"""
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(result, [])
    
    def test_complex_real_world_example(self):
        """Test a realistic paragraph with multiple formatting types"""
        node = TextNode(
            "Welcome to our `Python` tutorial! Learn **advanced** techniques and _best practices_.", 
            TextType.PLAIN
        )
        
        # Process bold first
        after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then italic
        after_italic = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)
        # Finally code
        final_result = split_nodes_delimiter(after_italic, "`", TextType.CODE)
        
        # Verify we got the right structure
        text_parts = [n.text for n in final_result]
        type_parts = [n.text_type for n in final_result]
        
        expected_texts = ["Welcome to our ", "Python", " tutorial! Learn ", "advanced", " techniques and ", "best practices", "."]
        expected_types = [TextType.PLAIN, TextType.CODE, TextType.PLAIN, TextType.BOLD, TextType.PLAIN, TextType.ITALIC, TextType.PLAIN]
        
        self.assertEqual(text_parts, expected_texts)
        self.assertEqual(type_parts, expected_types)


if __name__ == "__main__":
    unittest.main()