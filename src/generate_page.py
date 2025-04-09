from block_markdown import markdown_to_html_node
import os
from pathlib import Path


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(F"Generating a page from {from_path} to {dest_path}.")
    with open(from_path, "r") as source_md:
        read_data = source_md.read()
    html = markdown_to_html_node(read_data).to_html()

    with open(template_path, "r") as temp_md:
        temp_data = temp_md.read()
    
    title = extract_title(from_path)
    temp_data = temp_data.replace("{{ Title }}", title)
    temp_data = temp_data.replace("{{ Content }}", html)
    temp_data = temp_data.replace("href=\"/", f"href=\"{basepath}")
    temp_data = temp_data.replace("src=\"/", f"src=\"{basepath}")

    # Ensure directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as output_file:
        output_file.write(temp_data)


def extract_title(markdown_path):
    with open(markdown_path, "r") as example_dir:
        lines = example_dir.readlines()
    
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found.")

