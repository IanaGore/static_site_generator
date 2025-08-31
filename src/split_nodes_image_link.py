from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_image(old_nodes):
    """
    Split TextNodes containing images into separate nodes.
    
    Processes a list of TextNodes and splits any PLAIN type nodes that contain
    markdown image syntax into separate TextNode objects.
    
    Args:
        old_nodes (list): List of TextNode objects to process
        
    Returns:
        list: New list of TextNode objects with images split out
        
    Example:
        Input: [TextNode("Text with ![alt](url) image", TextType.PLAIN)]
        Output: [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" image", TextType.PLAIN)
        ]
        
    Algorithm:
        1. For each node in old_nodes:
           - If not PLAIN type: add to result unchanged
           - If PLAIN type: extract images and split around them
        2. Split process:
           - Extract all images from text using regex
           - For each image, split text around the image markdown
           - Create nodes for text before, the image itself, and continue with remaining text
           - Handle multiple images by processing recursively
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process PLAIN type nodes - leave other types unchanged
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        # Extract all images from this node's text
        images = extract_markdown_images(old_node.text)
        
        # If no images found, keep the original node
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Process the text by splitting around each image
        current_text = old_node.text
        
        for alt_text, url in images:
            # Construct the full markdown syntax for this image
            image_markdown = f"![{alt_text}]({url})"
            
            # Split the current text around this image (only first occurrence)
            sections = current_text.split(image_markdown, 1)
            
            if len(sections) != 2:
                # This shouldn't happen if extraction worked correctly
                continue
            
            before_text, after_text = sections
            
            # Add the text before the image (if not empty)
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.PLAIN, old_node.url))
            
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Continue processing with the text after this image
            current_text = after_text
        
        # Add any remaining text after all images (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.PLAIN, old_node.url))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextNodes containing links into separate nodes.
    
    Processes a list of TextNodes and splits any PLAIN type nodes that contain
    markdown link syntax into separate TextNode objects.
    
    Args:
        old_nodes (list): List of TextNode objects to process
        
    Returns:
        list: New list of TextNode objects with links split out
        
    Example:
        Input: [TextNode("Text with [anchor](url) link", TextType.PLAIN)]
        Output: [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("anchor", TextType.LINK, "url"),
            TextNode(" link", TextType.PLAIN)
        ]
        
    Algorithm:
        Same as split_nodes_image but for links instead of images.
        Uses extract_markdown_links to find link syntax.
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process PLAIN type nodes - leave other types unchanged
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        # Extract all links from this node's text
        links = extract_markdown_links(old_node.text)
        
        # If no links found, keep the original node
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Process the text by splitting around each link
        current_text = old_node.text
        
        for anchor_text, url in links:
            # Construct the full markdown syntax for this link
            link_markdown = f"[{anchor_text}]({url})"
            
            # Split the current text around this link (only first occurrence)
            sections = current_text.split(link_markdown, 1)
            
            if len(sections) != 2:
                # This shouldn't happen if extraction worked correctly
                continue
            
            before_text, after_text = sections
            
            # Add the text before the link (if not empty)
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.PLAIN, old_node.url))
            
            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # Continue processing with the text after this link
            current_text = after_text
        
        # Add any remaining text after all links (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.PLAIN, old_node.url))
    
    return new_nodes


