def markdown_to_blocks(markdown):
    """
    Split a markdown document into separate block-level elements.
    
    Block-level elements are separated by blank lines (double newlines).
    This function handles the document structure parsing, while inline
    formatting within blocks is handled by other functions.
    
    Args:
        markdown (str): Raw markdown document string
        
    Returns:
        list: List of block strings, each representing a distinct markdown block
        
    Block Types Handled:
        - Headings (# ## ###)
        - Paragraphs (plain text)
        - Lists (- * +)
        - Code blocks (```)
        - Quotes (>)
        - Any other block-level content
        
    Processing Steps:
        1. Split on double newlines (\n\n) to separate blocks
        2. Strip whitespace from each block
        3. Remove empty blocks (caused by excessive newlines)
        4. Return clean list of block strings
        
    Example:
        Input: "# Heading\n\nParagraph text\n\n- List item"
        Output: ["# Heading", "Paragraph text", "- List item"]
    """
    # Step 1: Split the markdown on double newlines
    # Double newlines (\n\n) are the standard way to separate blocks in markdown
    raw_blocks = markdown.split("\n\n")
    
    # Step 2: Clean up each block and filter out empty ones
    blocks = []
    for block in raw_blocks:
        # Strip leading and trailing whitespace from each block
        # This removes extra spaces, tabs, and single newlines
        cleaned_block = block.strip()
        
        # Only add non-empty blocks to the result
        # This handles cases where there are excessive newlines creating empty blocks
        if cleaned_block:
            blocks.append(cleaned_block)
    
    return blocks