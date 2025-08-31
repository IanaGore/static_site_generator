from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter
from split_nodes_image_link import split_nodes_image, split_nodes_link


def text_to_textnodes(text):
    """
    Convert raw markdown text into a list of TextNode objects.
    
    This function is the main entry point for markdown parsing. It takes a string
    of markdown-formatted text and returns a list of properly structured TextNode
    objects representing all the different formatting types.
    
    Args:
        text (str): Raw markdown text containing various formatting
        
    Returns:
        list: List of TextNode objects representing the parsed markdown
        
    Example:
        Input: "This is **bold** and _italic_ text with `code`"
        Output: [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with ", TextType.PLAIN),
            TextNode("code", TextType.CODE)
        ]
    
    Processing Order:
        1. Start with single PLAIN node containing all text
        2. Split out images (![alt](url))
        3. Split out links ([anchor](url))  
        4. Split out bold text (**bold**)
        5. Split out italic text (_italic_)
        6. Split out code text (`code`)
        
    Why This Order Matters:
        - Images and links first: They have complex syntax that could interfere with delimiters
        - Bold/italic/code last: Simple delimiters are processed after complex patterns
        - Order within delimiters doesn't matter much, but bold -> italic -> code is logical
    """
    # Step 1: Start with a single PLAIN node containing all the text
    nodes = [TextNode(text, TextType.PLAIN)]
    
    # Step 2: Split out images first (most complex syntax)
    nodes = split_nodes_image(nodes)
    
    # Step 3: Split out links (also complex syntax)  
    nodes = split_nodes_link(nodes)
    
    # Step 4: Split out bold text (delimiter: **)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Step 5: Split out italic text (delimiter: _)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # Step 6: Split out code text (delimiter: `)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes


# Example usage and demonstration
if __name__ == "__main__":
    print("Text to TextNodes Examples:\n")
    
    # Example 1: The assignment example
    print("Example 1: Assignment example")
    text1 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    result1 = text_to_textnodes(text1)
    
    print(f"Input: {text1}")
    print("\nOutput:")
    for i, node in enumerate(result1):
        print(f"  [{i}] {node}")
    print()
    
    # Example 2: Simple formatting
    print("Example 2: Simple formatting")
    text2 = "Just some **bold** and _italic_ text"
    result2 = text_to_textnodes(text2)
    
    print(f"Input: {text2}")
    print("Output:")
    for i, node in enumerate(result2):
        print(f"  [{i}] {node}")
    print()
    
    # Example 3: Only plain text
    print("Example 3: Plain text only")
    text3 = "Just plain text with no formatting"
    result3 = text_to_textnodes(text3)
    
    print(f"Input: {text3}")
    print("Output:")
    for i, node in enumerate(result3):
        print(f"  [{i}] {node}")
    print()
    
    # Example 4: Mixed complex content
    print("Example 4: Complex mixed content")
    text4 = "Check out ![this image](https://example.com/img.jpg) and visit [our **bold** docs](https://docs.com) for `code` examples!"
    result4 = text_to_textnodes(text4)
    
    print(f"Input: {text4}")
    print("Output:")
    for i, node in enumerate(result4):
        print(f"  [{i}] {node}")
    print()
    
    # Example 5: Edge cases
    print("Example 5: Edge cases")
    
    # Only formatting, no plain text
    text5a = "**bold**_italic_`code`"
    result5a = text_to_textnodes(text5a)
    print("Only formatting:")
    for node in result5a:
        print(f"  {node}")
    
    # Adjacent formatting
    text5b = "**bold**and**more bold**"
    result5b = text_to_textnodes(text5b)
    print("Adjacent formatting:")
    for node in result5b:
        print(f"  {node}")
    print()
    
    # Example 6: Show processing pipeline step-by-step
    print("Example 6: Processing pipeline demonstration")
    text6 = "Text with ![img](url) and **bold** text"
    
    print(f"Original: {text6}")
    
    # Step by step processing
    step1 = [TextNode(text6, TextType.PLAIN)]
    print(f"Step 1 - Initial: {step1}")
    
    step2 = split_nodes_image(step1)
    print("Step 2 - After images:")
    for node in step2:
        print(f"  {node}")
    
    step3 = split_nodes_link(step2)
    print("Step 3 - After links:")
    for node in step3:
        print(f"  {node}")
    
    step4 = split_nodes_delimiter(step3, "**", TextType.BOLD)
    print("Step 4 - After bold:")
    for node in step4:
        print(f"  {node}")
    
    final = text_to_textnodes(text6)
    print("Final result (using text_to_textnodes):")
    for node in final:
        print(f"  {node}")
    print()
    
    # Example 7: Why processing order matters
    print("Example 7: Understanding processing order")
    print("Images and links are processed first because:")
    print("  - They have complex, variable-length syntax")
    print("  - Their content might contain delimiter characters")
    print("  - Example: ![alt with **stars**](url) - the ** inside shouldn't be processed as bold")
    print()
    print("Delimiters are processed after because:")
    print("  - They have simple, fixed-length syntax")  
    print("  - They only operate on PLAIN nodes (not IMAGE/LINK nodes)")
    print("  - Order within delimiters (bold -> italic -> code) is less critical")
    print()
    
    # Example 8: Performance characteristics
    print("Example 8: Performance notes")
    print("Each processing step:")
    print("  - Operates on the result of the previous step")
    print("  - Only processes PLAIN nodes (other nodes pass through unchanged)")
    print("  - Maintains O(n) complexity where n is text length")
    print("  - Results in clean separation of concerns")