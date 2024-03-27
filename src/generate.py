import os
from block_transform import markdown_to_html_node


def extract_titlie(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]

    raise Exception("Document with no h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as markdown_file:
        markdown = markdown_file.read()
        title = extract_titlie(markdown)
        content = markdown_to_html_node(markdown).to_html()
        with open(template_path) as template_file:
            template = template_file.read()
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", content)
            dest_dir_path = os.path.dirname(dest_path)
            if dest_dir_path != "":
                os.makedirs(dest_dir_path, exist_ok=True)
            with open(dest_path, "w") as dest_file:
                dest_file.write(template)
