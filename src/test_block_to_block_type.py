import unittest
from block_to_block_type import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    
    def test_heading_single_hash(self):
        """Test level 1 heading"""
        block = "# This is a main heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_multiple_hashes(self):
        """Test different heading levels"""
        test_cases = [
            ("# Level 1", BlockType.HEADING),
            ("## Level 2", BlockType.HEADING),
            ("### Level 3", BlockType.HEADING),
            ("#### Level 4", BlockType.HEADING),
            ("##### Level 5", BlockType.HEADING),
            ("###### Level 6", BlockType.HEADING),
        ]
        
        for block, expected in test_cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, expected)
    
    def test_heading_invalid(self):
        """Test invalid heading syntax"""
        invalid_headings = [
            "####### Too many hashes",  # More than 6
            "#No space after hash",     # No space
            " # Leading space",         # Leading space (assumes stripped)
            "Not # a heading",          # Hash not at start
            "#",                        # Just hash, no content
            "## ",                      # Hash and space but no content
        ]
        
        for block in invalid_headings:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_code_block(self):
        """Test code block detection"""
        code_blocks = [
            "```\nprint('hello')\n```",
            "```python\ndef hello():\n    return 'world'\n```",
            "```\n```",  # Empty code block
            "```single line```",
        ]
        
        for block in code_blocks:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_invalid(self):
        """Test invalid code block syntax"""
        invalid_code = [
            "``not enough backticks``",
            "```no closing",
            "no opening```",
            "`single backtick`",
            "```", # Too short
        ]
        
        for block in invalid_code:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_quote_single_line(self):
        """Test single line quote"""
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_multi_line(self):
        """Test multi-line quote"""
        block = "> This is a quote\n> That spans multiple lines\n> All starting with >"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_nested(self):
        """Test nested quote syntax"""
        block = ">> This is a nested quote\n>> Still a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_invalid(self):
        """Test invalid quote syntax"""
        invalid_quotes = [
            "> Quote line\nNot a quote line",  # Mixed content
            "Not a quote\n> This line is",     # Doesn't start with >
            ">No space but still valid",       # Actually should be quote
        ]
        
        # Test the mixed content case
        result1 = block_to_block_type("> Quote line\nNot a quote line")
        self.assertEqual(result1, BlockType.PARAGRAPH)
        
        result2 = block_to_block_type("Not a quote\n> This line is")
        self.assertEqual(result2, BlockType.PARAGRAPH)
        
        # Test no space case (should actually be quote)
        result3 = block_to_block_type(">No space but still valid")
        self.assertEqual(result3, BlockType.QUOTE)
    
    def test_unordered_list_single_item(self):
        """Test single item unordered list"""
        block = "- Single list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_multiple_items(self):
        """Test multi-item unordered list"""
        block = "- First item\n- Second item\n- Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_invalid(self):
        """Test invalid unordered list syntax"""
        invalid_lists = [
            "- Item\nNot an item",     # Mixed content
            "-No space",               # No space after dash
            " - Leading space",        # Leading space (assumes stripped)
            "* Different bullet",      # Different bullet style
            "+ Different bullet",      # Different bullet style
        ]
        
        for block in invalid_lists:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_simple(self):
        """Test simple ordered list"""
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_single_item(self):
        """Test single item ordered list"""
        block = "1. Single item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_invalid_numbering(self):
        """Test ordered lists with invalid numbering"""
        invalid_ordered = [
            "2. Doesn't start at 1",
            "1. First\n3. Skips 2",
            "1. First\n1. Duplicate number",
            "1. First\n2. Second\n2. Duplicate",
            "0. Starts at zero",
        ]
        
        for block in invalid_ordered:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_invalid_format(self):
        """Test ordered lists with invalid format"""
        invalid_format = [
            "1.No space",
            "1) Wrong punctuation",
            "a. Letter instead of number",
            "1. Item\nNot numbered",
        ]
        
        for block in invalid_format:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_default(self):
        """Test that plain text defaults to paragraph"""
        paragraphs = [
            "Just plain text",
            "Text with **bold** and _italic_ formatting",
            "Multi line paragraph\nwith newlines\nbut no special formatting",
            "Text with [links](url) and ![images](url)",
        ]
        
        for block in paragraphs:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_empty_block(self):
        """Test empty block (should be paragraph)"""
        result = block_to_block_type("")
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_whitespace_only_block(self):
        """Test block with only whitespace (assumes already stripped)"""
        # Since we assume blocks are already stripped, this shouldn't happen
        # But test it anyway for completeness
        result = block_to_block_type("   ")
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_complex_content_blocks(self):
        """Test blocks with complex internal content"""
        test_cases = [
            ("# Heading with **bold** and _italic_ text", BlockType.HEADING),
            ("> Quote with **bold** text\n> And _italic_ text", BlockType.QUOTE),
            ("- List item with `code`\n- Another item with [link](url)", BlockType.UNORDERED_LIST),
            ("1. Ordered item with **bold**\n2. Another with _italic_", BlockType.ORDERED_LIST),
            ("```python\n# This comment has a hash\n> And this looks like quote\n```", BlockType.CODE),
        ]
        
        for block, expected in test_cases:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, expected)
    
    def test_priority_order(self):
        """Test that block type detection follows correct priority"""
        # This tests edge cases where multiple patterns might match
        
        # A code block that contains quote-like text
        code_with_quote = "```\n> This looks like a quote but it's in code\n```"
        result = block_to_block_type(code_with_quote)
        self.assertEqual(result, BlockType.CODE)
        
        # Make sure we check headings properly
        fake_heading = "This line has # but not at start"
        result = block_to_block_type(fake_heading)
        self.assertEqual(result, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()