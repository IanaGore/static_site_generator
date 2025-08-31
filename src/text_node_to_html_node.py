from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("Image TextNode must have a URL")
        return LeafNode("img", "", {
                        "src": text_node.url,
                        "alt": text_node.text
        })

    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")
