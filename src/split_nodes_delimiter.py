from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextNodes based on a delimiter to create formatted text nodes.
    
    This function processes a list of TextNodes and splits any PLAIN type nodes
    that contain the specified delimiter into multiple nodes with appropriate formatting.
    
    Args:
        old_nodes (list): List of TextNode objects to process
        delimiter (str): The delimiter to split on (e.g., "**", "_", "`")
        text_type (TextType): The TextType to assign to text between delimiters
        
    Returns:
        list: New list of TextNode objects with delimiter-based formatting applied
        
    Raises:
        ValueError: If a delimiter is opened but not closed (unmatched delimiter)
        
    Example:
        Input: [TextNode("Text with **bold** word", TextType.PLAIN)]
        Delimiter: "**"
        TextType: TextType.BOLD
        Output: [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.PLAIN)
        ]
        
    Algorithm:
        1. For each node in old_nodes:
           - If not PLAIN type: add to result unchanged
           - If PLAIN type: split on delimiter and create new nodes
        2. Split process:
           - Split text on delimiter
           - Odd indices = normal text (outside delimiters)
           - Even indices = formatted text (inside delimiters)
           - Validate that delimiters are properly paired
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process PLAIN type nodes - leave other types unchanged
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        # Split the text content by the delimiter
        split_parts = old_node.text.split(delimiter)
        
        # Check for unmatched delimiter
        # If delimiter count is odd, we have unmatched delimiters
        # split() creates len(delimiters) + 1 parts
        # So odd number of parts means even number of delimiters (matched pairs)
        # Even number of parts means odd number of delimiters (unmatched)
        if len(split_parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {old_node.text}")
        
        # Process each part of the split
        for i, part in enumerate(split_parts):
            # Skip empty parts (can happen when delimiter is at start/end)
            if part == "":
                continue
            
            # Determine the text type based on position
            if i % 2 == 0:
                # Even indices (0, 2, 4, ...) are outside delimiters = normal text
                new_nodes.append(TextNode(part, TextType.PLAIN, old_node.url))
            else:
                # Odd indices (1, 3, 5, ...) are inside delimiters = formatted text
                new_nodes.append(TextNode(part, text_type, old_node.url))
    
    return new_nodes