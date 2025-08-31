import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_attribute(self):
        node = HTMLNode(
            tag="a",
            value="Link text",
            props={"href": "https://www.google.com"}
        )
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_multiple_attributes(self):
        node = HTMLNode(
            tag="a",
            value="Link text",
            props={
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        result = node.props_to_html()
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertTrue(result.startswith(" "))
        self.assertEqual(result.count(" "), 2)

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p", value="Just text")
        self.assertEqual(node.props_to_html(), "")

                    
