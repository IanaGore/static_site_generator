import os
from pathlib import Path
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    title = extract_title(markdown_content)
    
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, 'w') as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(src_path):
            if item.endswith('.md'):
                relative_path = os.path.relpath(src_path, dir_path_content)
                relative_dir = os.path.dirname(relative_path)
                filename = Path(item).stem
                
                if relative_dir:
                    dest_path = os.path.join(dest_dir_path, relative_dir, f"{filename}.html")
                else:
                    dest_path = os.path.join(dest_dir_path, f"{filename}.html")
                
                generate_page(src_path, template_path, dest_path)
        else:
            dest_subdir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, dest_subdir)