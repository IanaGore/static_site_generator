from enum import Enum


class BlockType(Enum):
    """
    Enum representing different types of markdown blocks.
    
    Each block type corresponds to a different markdown syntax pattern
    and will eventually be converted to different HTML structures.
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Analyzes a block of markdown text and returns the corresponding BlockType.
    The function checks patterns in a specific order, from most specific to least specific.
    
    Args:
        block (str): A single block of markdown text (whitespace already stripped)
        
    Returns:
        BlockType: The type of block this text represents
        
    Block Type Rules:
        1. HEADING: Starts with 1-6 # characters + space + content
        2. CODE: Starts and ends with ``` (three backticks)
        3. QUOTE: Every line starts with > character
        4. UNORDERED_LIST: Every line starts with - followed by space
        5. ORDERED_LIST: Every line starts with number + . + space, incrementing from 1
        6. PARAGRAPH: Default if none of the above match
        
    Examples:
        "# Heading" → BlockType.HEADING
        "```code```" → BlockType.CODE
        "> Quote line" → BlockType.QUOTE
        "- List item" → BlockType.UNORDERED_LIST
        "1. First item" → BlockType.ORDERED_LIST
        "Plain text" → BlockType.PARAGRAPH
    """
    
    # Check for HEADING (1-6 # characters + space + content)
    if block.startswith('#'):
        # Count consecutive # characters from the start
        hash_count = 0
        for char in block:
            if char == '#':
                hash_count += 1
            else:
                break
        
        # Valid heading: 1-6 #'s followed by a space and actual content
        if (1 <= hash_count <= 6 and 
            len(block) > hash_count and 
            block[hash_count] == ' ' and
            len(block) > hash_count + 1):  # Must have content after space
            return BlockType.HEADING
    
    # Check for CODE block (starts and ends with ```)
    if block.startswith('```') and block.endswith('```') and len(block) >= 6:
        return BlockType.CODE
    
    # Check for QUOTE (every line starts with >)
    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check for UNORDERED_LIST (every line starts with "- ")
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ORDERED_LIST (every line starts with number + ". ", incrementing from 1)
    if _is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    
    # Default: PARAGRAPH
    return BlockType.PARAGRAPH


def _is_ordered_list(lines):
    """
    Helper function to check if lines form a valid ordered list.
    
    Rules:
    - Every line must start with a number followed by ". "
    - Numbers must start at 1 and increment by 1
    - No gaps or wrong numbers allowed
    
    Args:
        lines (list): List of lines to check
        
    Returns:
        bool: True if lines form a valid ordered list
    """
    for i, line in enumerate(lines):
        expected_number = i + 1  # Should be 1, 2, 3, ...
        expected_prefix = f"{expected_number}. "
        
        if not line.startswith(expected_prefix):
            return False
    
    return True