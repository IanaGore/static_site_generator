import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")
    
    def test_extract_title_with_whitespace(self):
        markdown = "#   Hello World   "
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")
    
    def test_extract_title_multiline(self):
        markdown = """Some text here
# My Title
More content"""
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")
    
    def test_extract_title_with_other_headers(self):
        markdown = """## Not this one
# This is the title
### Also not this one"""
        result = extract_title(markdown)
        self.assertEqual(result, "This is the title")
    
    def test_extract_title_no_h1_raises_exception(self):
        markdown = """## Only h2 headers here
### And h3 headers
But no h1"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")
    
    def test_extract_title_empty_string_raises_exception(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()