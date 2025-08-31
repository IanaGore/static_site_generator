import unittest
from textnode import TextNode, TextType
from split_nodes_image_link import split_nodes_image, split_nodes_link


class TestSplitNodesImageLink(unittest.TestCase):
    
    def test_split_images(self):
        """Test provided example: split multiple images"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_links(self):
        """Test provided example: split multiple links"""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.PLAIN),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_images_single(self):
        """Test splitting single image"""
        node = TextNode("Text with ![alt text](https://example.com/image.jpg) here", TextType.PLAIN)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" here", TextType.PLAIN),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_links_single(self):
        """Test splitting single link"""
        node = TextNode("Text with [anchor](https://example.com) here", TextType.PLAIN)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("anchor", TextType.LINK, "https://example.com"),
            TextNode(" here", TextType.PLAIN),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_images_at_start(self):
        """Test image at the beginning"""
        node = TextNode("![start image](url) followed by text", TextType.PLAIN)
        result = split_nodes_image([node])
        expected = [
            TextNode("start image", TextType.IMAGE, "url"),
            TextNode(" followed by text", TextType.PLAIN),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_links_at_start(self):
        """Test link at the beginning"""
        node = TextNode("[start link](url) followed by text", TextType.PLAIN)
        result = split_nodes_link([node])
        expected = [
            TextNode("start link", TextType.LINK, "url"),
            TextNode(" followed by text", TextType.PLAIN),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_images_at_end(self):
        """Test image at the end"""
        node = TextNode("Text followed by ![end image](url)", TextType.PLAIN)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text followed by ", TextType.PLAIN),
            TextNode("end image", TextType.IMAGE, "url"),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_links_at_end(self):
        """Test link at the end"""
        node = TextNode("Text followed by [end link](url)", TextType.PLAIN)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text followed by ", TextType.PLAIN),
            TextNode("end link", TextType.LINK, "url"),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_images_only(self):
        """Test text that is only an image"""
        node = TextNode("![only image](url)", TextType.PLAIN)
        result = split_nodes_image([node])
        expected = [TextNode("only image", TextType.IMAGE, "url")]
        self.assertListEqual(result, expected)
    
    def test_split_links_only(self):
        """Test text that is only a link"""
        node = TextNode("[only link](url)", TextType.PLAIN)
        result = split_nodes_link([node])
        expected = [TextNode("only link", TextType.LINK, "url")]
        self.assertListEqual(result, expected)
    
    def test_split_images_no_images(self):
        """Test text with no images"""
        node = TextNode("Just plain text with no images", TextType.PLAIN)
        result = split_nodes_image([node])
        expected = [TextNode("Just plain text with no images", TextType.PLAIN)]
        self.assertListEqual(result, expected)
    
    def test_split_links_no_links(self):
        """Test text with no links"""
        node = TextNode("Just plain text with no links", TextType.PLAIN)
        result = split_nodes_link([node])
        expected = [TextNode("Just plain text with no links", TextType.PLAIN)]
        self.assertListEqual(result, expected)
    
    def test_split_images_empty_alt(self):
        """Test image with empty alt text"""
        node = TextNode("Text with ![](https://example.com/image.jpg) image", TextType.PLAIN)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" image", TextType.PLAIN),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_links_empty_anchor(self):
        """Test link with empty anchor text"""
        node = TextNode("Text with [](https://example.com) link", TextType.PLAIN)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("", TextType.LINK, "https://example.com"),
            TextNode(" link", TextType.PLAIN),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_images_adjacent(self):
        """Test adjacent images (no text between)"""
        node = TextNode("![img1](url1)![img2](url2)", TextType.PLAIN)
        result = split_nodes_image([node])
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_links_adjacent(self):
        """Test adjacent links (no text between)"""
        node = TextNode("[link1](url1)[link2](url2)", TextType.PLAIN)
        result = split_nodes_link([node])
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_non_text_nodes_unchanged(self):
        """Test that non-PLAIN nodes pass through unchanged"""
        nodes = [
            TextNode("Text with ![image](url)", TextType.PLAIN),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        
        result = split_nodes_image(nodes)
        
        # First node should be split
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.PLAIN)
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        
        # Other nodes should be unchanged
        self.assertEqual(result[2].text, "Already bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, "Already italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
    
    def test_split_preserve_url_property(self):
        """Test that original URL property is preserved in split text nodes"""
        node = TextNode("Text with ![image](img_url)", TextType.PLAIN, "original_url")
        result = split_nodes_image([node])
        
        # Text nodes should preserve the original URL
        self.assertEqual(result[0].url, "original_url")  # "Text with "
        # Image node should use the new URL from the image
        self.assertEqual(result[1].url, "img_url")       # Image node
    
    def test_split_multiple_same_type(self):
        """Test multiple instances of the same image/link"""
        node = TextNode("![img](url) text ![img](url) more ![img](url)", TextType.PLAIN)
        result = split_nodes_image([node])
        
        expected = [
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" text ", TextType.PLAIN),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" more ", TextType.PLAIN),
            TextNode("img", TextType.IMAGE, "url"),
        ]
        self.assertListEqual(result, expected)
    
    def test_split_complex_urls(self):
        """Test images and links with complex URLs"""
        image_node = TextNode(
            "![complex](https://cdn.example.com/images/photo.jpg?size=large&format=webp)",
            TextType.PLAIN
        )
        link_node = TextNode(
            "[API](https://api.example.com/v1/users?limit=10&offset=0)",
            TextType.PLAIN
        )
        
        image_result = split_nodes_image([image_node])
        link_result = split_nodes_link([link_node])
        
        expected_image = [TextNode("complex", TextType.IMAGE, "https://cdn.example.com/images/photo.jpg?size=large&format=webp")]
        expected_link = [TextNode("API", TextType.LINK, "https://api.example.com/v1/users?limit=10&offset=0")]
        
        self.assertListEqual(image_result, expected_image)
        self.assertListEqual(link_result, expected_link)
    
    def test_chaining_image_and_link_processing(self):
        """Test processing text with both images and links"""
        original = [TextNode("Text ![img](img_url) and [link](link_url) here", TextType.PLAIN)]
        
        # First pass: process images
        after_images = split_nodes_image(original)
        expected_after_images = [
            TextNode("Text ", TextType.PLAIN),
            TextNode("img", TextType.IMAGE, "img_url"),
            TextNode(" and [link](link_url) here", TextType.PLAIN),
        ]
        self.assertListEqual(after_images, expected_after_images)
        
        # Second pass: process links (on result of first pass)
        after_links = split_nodes_link(after_images)
        expected_final = [
            TextNode("Text ", TextType.PLAIN),
            TextNode("img", TextType.IMAGE, "img_url"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "link_url"),
            TextNode(" here", TextType.PLAIN),
        ]
        self.assertListEqual(after_links, expected_final)
    
    def test_empty_input_list(self):
        """Test empty input list"""
        result_images = split_nodes_image([])
        result_links = split_nodes_link([])
        
        self.assertEqual(result_images, [])
        self.assertEqual(result_links, [])
    
    def test_real_world_mixed_content(self):
        """Test realistic content with various markdown elements"""
        node = TextNode(
            "Check out this ![screenshot](https://example.com/shot.png) and visit [our docs](https://docs.example.com) for more info. Also see ![diagram](https://example.com/diagram.svg).",
            TextType.PLAIN
        )
        
        # Process images first
        after_images = split_nodes_image([node])
        expected_after_images = [
            TextNode("Check out this ", TextType.PLAIN),
            TextNode("screenshot", TextType.IMAGE, "https://example.com/shot.png"),
            TextNode(" and visit [our docs](https://docs.example.com) for more info. Also see ", TextType.PLAIN),
            TextNode("diagram", TextType.IMAGE, "https://example.com/diagram.svg"),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertListEqual(after_images, expected_after_images)
        
        # Then process links
        after_links = split_nodes_link(after_images)
        expected_final = [
            TextNode("Check out this ", TextType.PLAIN),
            TextNode("screenshot", TextType.IMAGE, "https://example.com/shot.png"),
            TextNode(" and visit ", TextType.PLAIN),
            TextNode("our docs", TextType.LINK, "https://docs.example.com"),
            TextNode(" for more info. Also see ", TextType.PLAIN),
            TextNode("diagram", TextType.IMAGE, "https://example.com/diagram.svg"),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertListEqual(after_links, expected_final)
    
    def test_images_not_affecting_links(self):
        """Test that image processing doesn't interfere with link syntax"""
        node = TextNode("![image](img_url) and [link](link_url)", TextType.PLAIN)
        
        # Split images should not affect link syntax
        after_images = split_nodes_image([node])
        
        # Should get 2 nodes: [image_node, text_node_with_link]
        self.assertEqual(len(after_images), 2)
        self.assertEqual(after_images[0].text, "image")
        self.assertEqual(after_images[0].text_type, TextType.IMAGE)
        self.assertEqual(after_images[1].text, " and [link](link_url)")
        self.assertEqual(after_images[1].text_type, TextType.PLAIN)
        
        # Link syntax should still be processable
        after_links = split_nodes_link(after_images)
        link_nodes = [n for n in after_links if n.text_type == TextType.LINK]
        self.assertEqual(len(link_nodes), 1)
        self.assertEqual(link_nodes[0].text, "link")
        self.assertEqual(link_nodes[0].url, "link_url")
    
    def test_special_characters_in_text(self):
        """Test alt text and anchor text with special characters"""
        image_node = TextNode("![Image with spaces & symbols!](url)", TextType.PLAIN)
        link_node = TextNode("[Link with 123 & symbols!](url)", TextType.PLAIN)
        
        image_result = split_nodes_image([image_node])
        link_result = split_nodes_link([link_node])
        
        expected_image = [TextNode("Image with spaces & symbols!", TextType.IMAGE, "url")]
        expected_link = [TextNode("Link with 123 & symbols!", TextType.LINK, "url")]
        
        self.assertListEqual(image_result, expected_image)
        self.assertListEqual(link_result, expected_link)


if __name__ == "__main__":
    unittest.main()