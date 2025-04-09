
from copy_static import copy_static_files
import shutil, os
from generate_page import generate_page, generate_pages_recursive
import sys

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
basepath=sys.argv[0]

def main():

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_static_files(dir_path_static, dir_path_public)

    print("Generating content")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)


    

if __name__ == "__main__":
    main()