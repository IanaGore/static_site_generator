import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Just some raw text")
        self.assertEqual(node.to_html(), "Just some raw text")
