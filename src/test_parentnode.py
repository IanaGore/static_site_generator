import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    
    def test_to_html_with_children(self):
        """Test provided example: simple parent with one child"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """Test provided example: nested parent nodes (recursion)"""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_mixed_children(self):
        """Test the main example from assignment: paragraph with mixed formatting"""
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)
    
    def test_to_html_with_props(self):
        """Test parent node with attributes"""
        child = LeafNode("p", "Content")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        result = parent.to_html()
        # Check structure
        self.assertTrue(result.startswith('<div '))
        self.assertTrue(result.endswith('><p>Content</p></div>'))
        # Check attributes are present
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
    
    def test_to_html_multiple_children(self):
        """Test parent with multiple direct children"""
        children = [
            LeafNode("h1", "Title"),
            LeafNode("p", "First paragraph"),
            LeafNode("p", "Second paragraph")
        ]
        parent = ParentNode("div", children)
        expected = "<div><h1>Title</h1><p>First paragraph</p><p>Second paragraph</p></div>"
        self.assertEqual(parent.to_html(), expected)
    
    def test_to_html_deep_nesting(self):
        """Test deeply nested structure (multiple levels of recursion)"""
        # Build from inside out: span -> p -> div -> section
        innermost = LeafNode("strong", "Deep content")
        level3 = ParentNode("span", [innermost])
        level2 = ParentNode("p", [level3])
        level1 = ParentNode("div", [level2])
        root = ParentNode("section", [level1])
        
        expected = "<section><div><p><span><strong>Deep content</strong></span></p></div></section>"
        self.assertEqual(root.to_html(), expected)
    
    def test_to_html_mixed_parent_leaf_children(self):
        """Test parent with both ParentNode and LeafNode children"""
        leaf_child = LeafNode("span", "Leaf content")
        parent_child = ParentNode("p", [LeafNode("em", "Nested content")])
        root = ParentNode("div", [leaf_child, parent_child])
        
        expected = "<div><span>Leaf content</span><p><em>Nested content</em></p></div>"
        self.assertEqual(root.to_html(), expected)
    
    def test_to_html_list_structure(self):
        """Test typical list structure with multiple nested elements"""
        list_items = [
            ParentNode("li", [LeafNode(None, "First item")]),
            ParentNode("li", [LeafNode("strong", "Important item")]),
            ParentNode("li", [LeafNode(None, "Last item")])
        ]
        unordered_list = ParentNode("ul", list_items)
        
        expected = "<ul><li>First item</li><li><strong>Important item</strong></li><li>Last item</li></ul>"
        self.assertEqual(unordered_list.to_html(), expected)
    
    def test_to_html_table_structure(self):
        """Test complex table structure (multiple levels of nesting)"""
        cell1 = ParentNode("td", [LeafNode(None, "Cell 1")])
        cell2 = ParentNode("td", [LeafNode("strong", "Cell 2")])
        row = ParentNode("tr", [cell1, cell2])
        table = ParentNode("table", [row])
        
        expected = "<table><tr><td>Cell 1</td><td><strong>Cell 2</strong></td></tr></table>"
        self.assertEqual(table.to_html(), expected)
    
    def test_to_html_no_tag_raises_error(self):
        """Test that ParentNode with no tag raises ValueError"""
        child = LeafNode("p", "content")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag")
    
    def test_to_html_no_children_raises_error(self):
        """Test that ParentNode with no children raises ValueError"""
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children")
    
    def test_to_html_empty_children_list(self):
        """Test ParentNode with empty children list (should work)"""
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")
    
    def test_constructor_inheritance(self):
        """Test that ParentNode properly inherits from HTMLNode"""
        child = LeafNode("p", "content")
        parent = ParentNode("div", [child])
        self.assertIsInstance(parent, HTMLNode)
        self.assertIsInstance(parent, ParentNode)
    
    def test_constructor_sets_properties(self):
        """Test that constructor properly sets all properties"""
        child = LeafNode("p", "content")
        parent = ParentNode("div", [child], {"class": "container"})
        
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, {"class": "container"})
        self.assertIsNone(parent.value)  # Should always be None for parent nodes
    
    def test_constructor_no_props(self):
        """Test constructor with no props parameter"""
        child = LeafNode("p", "content")
        parent = ParentNode("div", [child])
        
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child])
        self.assertIsNone(parent.props)
        self.assertIsNone(parent.value)
    
    def test_repr_inherited(self):
        """Test that __repr__ method is inherited from HTMLNode"""
        child = LeafNode("p", "content")
        parent = ParentNode("div", [child], {"class": "test"})
        repr_str = repr(parent)
        
        # Should show HTMLNode format since that's what it inherits
        self.assertIn("HTMLNode(div,", repr_str)
        self.assertIn("None,", repr_str)  # value should be None
        self.assertIn("test", repr_str)   # props should be present
    
    def test_complex_real_world_example(self):
        """Test a complex, realistic HTML structure"""
        # Build a complex article structure
        title = LeafNode("h1", "Article Title")
        
        intro_text = ParentNode("p", [
            LeafNode(None, "This is an "),
            LeafNode("em", "important"),
            LeafNode(None, " article about "),
            LeafNode("strong", "web development"),
            LeafNode(None, ".")
        ])
        
        list_items = [
            ParentNode("li", [LeafNode(None, "First point")]),
            ParentNode("li", [LeafNode("code", "Code example")]),
        ]
        bullet_list = ParentNode("ul", list_items)
        
        article = ParentNode("article", [title, intro_text, bullet_list], {
            "class": "blog-post",
            "data-id": "123"
        })
        
        result = article.to_html()
        
        # Verify structure without worrying about attribute order
        self.assertTrue(result.startswith('<article '))
        self.assertIn('class="blog-post"', result)
        self.assertIn('data-id="123"', result)
        self.assertIn('<h1>Article Title</h1>', result)
        self.assertIn('<em>important</em>', result)
        self.assertIn('<strong>web development</strong>', result)
        self.assertIn('<code>Code example</code>', result)
        self.assertTrue(result.endswith('</ul></article>'))


if __name__ == "__main__":
    unittest.main()
