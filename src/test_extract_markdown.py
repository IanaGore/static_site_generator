import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        """Test provided example: single image extraction"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        """Test extraction of multiple images"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(result, expected)
    
    def test_extract_markdown_images_no_images(self):
        """Test text with no images"""
        text = "This is just plain text with no images"
        result = extract_markdown_images(text)
        self.assertListEqual(result, [])
    
    def test_extract_markdown_images_empty_alt(self):
        """Test image with empty alt text"""
        text = "Image with empty alt: ![](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        expected = [("", "https://example.com/image.jpg")]
        self.assertListEqual(result, expected)
    
    def test_extract_markdown_images_complex_urls(self):
        """Test images with complex URLs"""
        text = "![image1](https://cdn.example.com/images/photo.jpg?size=large&format=webp) and ![image2](/relative/path/image.png)"
        result = extract_markdown_images(text)
        expected = [
            ("image1", "https://cdn.example.com/images/photo.jpg?size=large&format=webp"),
            ("image2", "/relative/path/image.png")
        ]
        self.assertListEqual(result, expected)
    
    def test_extract_markdown_links_single(self):
        """Test extraction of single link"""
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        result = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(result, expected)
    
    def test_extract_markdown_links_multiple(self):
        """Test extraction of multiple links"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(result, expected)
    
    def test_extract_markdown_links_no_links(self):
        """Test text with no links"""
        text = "This is just plain text with no links"
        result = extract_markdown_links(text)
        self.assertListEqual(result, [])
    
    def test_extract_markdown_links_empty_anchor(self):
        """Test link with empty anchor text"""
        text = "Link with empty anchor: [](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("", "https://example.com")]
        self.assertListEqual(result, expected)
    
    def test_extract_markdown_links_complex_urls(self):
        """Test links with complex URLs"""
        text = "Visit [our API](https://api.example.com/v1/users?limit=10&offset=0) or [local page](/about#team)"
        result = extract_markdown_links(text)
        expected = [
            ("our API", "https://api.example.com/v1/users?limit=10&offset=0"),
            ("local page", "/about#team")
        ]
        self.assertListEqual(result, expected)
    
    def test_images_and_links_together(self):
        """Test text with both images and links (should not interfere)"""
        text = "Check out this ![cool image](https://example.com/image.jpg) and visit [our site](https://example.com)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        expected_images = [("cool image", "https://example.com/image.jpg")]
        expected_links = [("our site", "https://example.com")]
        
        self.assertListEqual(images, expected_images)
        self.assertListEqual(links, expected_links)
    
    def test_links_not_capturing_images(self):
        """Test that link extractor does not capture images (negative lookbehind)"""
        text = "An image ![test image](https://example.com/image.jpg) and a link [test link](https://example.com)"
        
        # Links should only find the actual link, not the image
        links = extract_markdown_links(text)
        expected_links = [("test link", "https://example.com")]
        self.assertListEqual(links, expected_links)
        
        # Images should only find the actual image
        images = extract_markdown_images(text)
        expected_images = [("test image", "https://example.com/image.jpg")]
        self.assertListEqual(images, expected_images)
    
    def test_special_characters_in_text(self):
        """Test alt text and anchor text with special characters"""
        text = "![Image with spaces & symbols](url1) and [Link with 123 & symbols](url2)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        expected_images = [("Image with spaces & symbols", "url1")]
        expected_links = [("Link with 123 & symbols", "url2")]
        
        self.assertListEqual(images, expected_images)
        self.assertListEqual(links, expected_links)
    
    def test_nested_brackets_not_captured(self):
        """Test that nested brackets are handled correctly (should not match)"""
        # These should not be captured because they have nested brackets
        text = "Invalid: ![nested [brackets]](url) and [nested [brackets]](url)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        # Should not match due to nested brackets
        self.assertListEqual(images, [])
        self.assertListEqual(links, [])
    
    def test_nested_parentheses_not_captured(self):
        """Test that nested parentheses are handled correctly (should not match)"""
        # These should not be captured because they have nested parentheses
        text = "Invalid: ![alt](url(with)parens) and [anchor](url(with)parens)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        # Should not match due to nested parentheses
        self.assertListEqual(images, [])
        self.assertListEqual(links, [])
    
    def test_multiple_same_type(self):
        """Test multiple instances of same type"""
        text = "![img1](url1) text ![img2](url2) more text ![img3](url3)"
        
        images = extract_markdown_images(text)
        expected = [("img1", "url1"), ("img2", "url2"), ("img3", "url3")]
        self.assertListEqual(images, expected)
    
    def test_adjacent_markdown_elements(self):
        """Test adjacent markdown elements"""
        text = "![image](img_url)[link](link_url)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        expected_images = [("image", "img_url")]
        expected_links = [("link", "link_url")]
        
        self.assertListEqual(images, expected_images)
        self.assertListEqual(links, expected_links)
    
    def test_empty_string(self):
        """Test empty string input"""
        images = extract_markdown_images("")
        links = extract_markdown_links("")
        
        self.assertListEqual(images, [])
        self.assertListEqual(links, [])
    
    def test_only_partial_markdown(self):
        """Test text with partial markdown syntax (should not match)"""
        text = "Incomplete: ![alt text](no closing or [anchor text](no closing"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        # Incomplete markdown should not match
        self.assertListEqual(images, [])
        self.assertListEqual(links, [])
    
    def test_real_world_example(self):
        """Test realistic markdown content"""
        text = """
        # My Blog Post
        
        Welcome to my blog! Here's a cool ![profile pic](https://example.com/me.jpg) of myself.
        
        You can follow me on [Twitter](https://twitter.com/myhandle) or check out my 
        [GitHub](https://github.com/myusername) for code examples.
        
        Here's another image: ![code screenshot](https://example.com/code.png)
        """
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        expected_images = [
            ("profile pic", "https://example.com/me.jpg"),
            ("code screenshot", "https://example.com/code.png")
        ]
        expected_links = [
            ("Twitter", "https://twitter.com/myhandle"),
            ("GitHub", "https://github.com/myusername")
        ]
        
        self.assertListEqual(images, expected_images)
        self.assertListEqual(links, expected_links)
    
    def test_case_sensitivity(self):
        """Test that extraction is case sensitive (as it should be)"""
        text = "![Image](URL1) and [Link](URL2)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        # Should preserve exact case
        expected_images = [("Image", "URL1")]
        expected_links = [("Link", "URL2")]
        
        self.assertListEqual(images, expected_images)
        self.assertListEqual(links, expected_links)


if __name__ == "__main__":
    unittest.main()