from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import BlockType, block_to_block_type
from text_to_textnodes import text_to_textnodes
from text_node_to_html_node import text_node_to_html_node
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document to a single HTML node tree.
    
    This is the main function that orchestrates the entire markdown-to-HTML conversion.
    It processes both block-level structure and inline formatting.
    
    Args:
        markdown (str): Complete markdown document string
        
    Returns:
        ParentNode: A div element containing all the converted blocks as children
        
    Process:
        1. Split markdown into blocks
        2. For each block:
           a. Determine block type
           b. Create appropriate HTML structure
           c. Process inline content within the block
        3. Wrap all blocks in a parent div element
        
    Example:
        Input: "# Title\n\nParagraph with **bold**"
        Output: ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "Title")]),
            ParentNode("p", [LeafNode(None, "Paragraph with "), LeafNode("b", "bold")])
        ])
    """
    # Step 1: Split the markdown document into individual blocks
    blocks = markdown_to_blocks(markdown)
    
    # Step 2: Convert each block to an HTMLNode
    block_nodes = []
    for block in blocks:
        # Determine what type of block this is
        block_type = block_to_block_type(block)
        
        # Convert the block to an HTMLNode based on its type
        html_node = block_to_html_node(block, block_type)
        block_nodes.append(html_node)
    
    # Step 3: Wrap all blocks in a parent div element
    return ParentNode("div", block_nodes)


def block_to_html_node(block, block_type):
    """
    Convert a single markdown block to an HTMLNode based on its type.
    
    Args:
        block (str): The raw markdown block text
        block_type (BlockType): The type of block this represents
        
    Returns:
        HTMLNode: The HTML representation of this block
    """
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unsupported block type: {block_type}")


def text_to_children(text):
    """
    Convert markdown text to a list of child HTMLNodes (for inline processing).
    
    This is the bridge between block-level and inline processing.
    It handles all inline markdown within a block.
    
    Args:
        text (str): Raw markdown text containing inline formatting
        
    Returns:
        list: List of HTMLNode objects representing the inline content
    """
    # Convert text to TextNodes (handles inline markdown)
    text_nodes = text_to_textnodes(text)
    
    # Convert TextNodes to HTMLNodes
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    return html_nodes


def paragraph_to_html_node(block):
    """
    Convert a paragraph block to a <p> HTMLNode.
    
    Paragraphs can span multiple lines in markdown, but in HTML they should
    be rendered as continuous text with spaces instead of line breaks.
    
    Args:
        block (str): Paragraph text with potential inline formatting and newlines
        
    Returns:
        ParentNode: <p> element containing the processed inline content
    """
    # Convert internal newlines to spaces for proper paragraph formatting
    # In markdown, paragraphs can span multiple lines, but HTML paragraphs should be continuous
    normalized_text = block.replace('\n', ' ')
    
    children = text_to_children(normalized_text)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """
    Convert a heading block to an <h1>-<h6> HTMLNode.
    
    Args:
        block (str): Heading text starting with 1-6 # characters
        
    Returns:
        ParentNode: <h1>-<h6> element containing the heading content
    """
    # Count the number of # characters to determine heading level
    hash_count = 0
    for char in block:
        if char == '#':
            hash_count += 1
        else:
            break
    
    # Extract the heading text (everything after "# " or "## ", etc.)
    heading_text = block[hash_count + 1:]  # Skip the hashes and space
    
    # Create the appropriate heading tag
    heading_tag = f"h{hash_count}"
    
    # Process inline content within the heading
    children = text_to_children(heading_text)
    
    return ParentNode(heading_tag, children)


def code_to_html_node(block):
    """
    Convert a code block to a <pre><code> HTMLNode.
    
    Code blocks are special - they don't process inline markdown.
    The content is preserved exactly as-is, including trailing newlines.
    
    Args:
        block (str): Code block text surrounded by ```
        
    Returns:
        ParentNode: <pre> element containing <code> element with raw text
    """
    # Extract the code content by removing the opening and closing ```
    lines = block.split('\n')
    
    # Remove first line (```[language]) and last line (```)
    code_lines = lines[1:-1]
    code_content = '\n'.join(code_lines)
    
    # Add trailing newline to match expected test behavior
    # This preserves the newline that was before the closing ```
    if code_lines:
        code_content += '\n'
    
    # Create code element with raw text (no inline processing)
    code_node = LeafNode("code", code_content)
    
    # Wrap in pre element
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """
    Convert a quote block to a <blockquote> HTMLNode.
    
    Args:
        block (str): Quote text with each line starting with >
        
    Returns:
        ParentNode: <blockquote> element containing the quote content
    """
    # Remove the > character from each line
    lines = block.split('\n')
    quote_lines = []
    
    for line in lines:
        # Remove the > and any space after it
        if line.startswith('> '):
            quote_lines.append(line[2:])  # Remove "> "
        elif line.startswith('>'):
            quote_lines.append(line[1:])  # Remove just ">"
    
    # Join the quote content back together
    quote_text = '\n'.join(quote_lines)
    
    # Process inline content within the quote
    children = text_to_children(quote_text)
    
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """
    Convert an unordered list block to a <ul> HTMLNode.
    
    Args:
        block (str): Unordered list with each line starting with "- "
        
    Returns:
        ParentNode: <ul> element containing <li> elements
    """
    # Split into individual list items
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Remove the "- " prefix from each line
        item_text = line[2:]  # Remove "- "
        
        # Process inline content within the list item
        item_children = text_to_children(item_text)
        
        # Create <li> element for this item
        list_item = ParentNode("li", item_children)
        list_items.append(list_item)
    
    # Wrap all items in <ul> element
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """
    Convert an ordered list block to an <ol> HTMLNode.
    
    Args:
        block (str): Ordered list with each line starting with "1. ", "2. ", etc.
        
    Returns:
        ParentNode: <ol> element containing <li> elements
    """
    # Split into individual list items
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Find the ". " and extract text after it
        dot_index = line.find('. ')
        if dot_index != -1:
            item_text = line[dot_index + 2:]  # Text after ". "
            
            # Process inline content within the list item
            item_children = text_to_children(item_text)
            
            # Create <li> element for this item
            list_item = ParentNode("li", item_children)
            list_items.append(list_item)
    
    # Wrap all items in <ol> element
    return ParentNode("ol", list_items)


