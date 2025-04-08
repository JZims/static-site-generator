
from copy_static import copy_static_files
import shutil, os

dir_path_static = "./static"
dir_path_public = "./public"

def main():

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_static_files(dir_path_static, dir_path_public)

    

if __name__ == "__main__":
    main()