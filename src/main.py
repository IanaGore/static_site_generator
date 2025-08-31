import os
import shutil
import sys
from generate_page import generate_pages_recursive

def copy_static(src_dir, dest_dir):
    if os.path.exists(dest_dir):
        print(f"Removing existing destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    print(f"Creating destination directory: {dest_dir}")
    os.mkdir(dest_dir)
    
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Copying directory: {src_path} -> {dest_path}")
            copy_static(src_path, dest_path)

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    copy_static("static", "docs")
    
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
   main()
