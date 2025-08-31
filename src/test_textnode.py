import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("World", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_different_text_type(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_eq_different_url(self):
        node1 = TextNode("Link text", TextType.LINK, "https://google.com")
        node2 = TextNode("Link text", TextType.LINK, "https://azure.com")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
