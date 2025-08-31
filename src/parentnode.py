from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        opening_tag = f"<{self.tag}{self.props_to_html()}>"

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        closing_tag = f"</{self.tag}>"

        return f"{opening_tag}{children_html}{closing_tag}"
