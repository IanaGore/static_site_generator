import re
from textnode import TextNode, TextType


def extract_markdown_images(text):
    # Regex pattern for markdown images: ![alt text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    # re.findall returns list of tuples when regex has multiple capture groups
    # Each tuple contains (alt_text, url)
    matches = re.findall(pattern, text)
    
    return matches


def extract_markdown_links(text):
    # Regex pattern for markdown links: [anchor text](url)
    # (?<!!): negative lookbehind to exclude images (which start with !)
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    # re.findall returns list of tuples when regex has multiple capture groups
    # Each tuple contains (anchor_text, url)
    matches = re.findall(pattern, text)
    
    return matches