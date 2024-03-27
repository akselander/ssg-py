import os
import shutil
from generate import generate_page_recursive


def copy(source, dest):
    if os.path.isfile(source):
        print(f"Copy from {source} to {dest}")
        shutil.copy(source, dest)
        return

    if not os.path.exists(dest):
        os.mkdir(dest)
    for file in os.listdir(source):
        from_path = os.path.join(source, file)
        to_path = os.path.join(dest, file)
        copy(from_path, to_path)


path_static = "static"
path_public = "public"
path_content = "content"


def main():
    if os.path.exists(path_public):
        print(f"Deleting {path_public}")
        shutil.rmtree(path_public)
    print(f"Copying files from {path_static} to {path_public}...")
    copy("static", "public")

    generate_page_recursive(path_content, "template.html", path_public)


main()
