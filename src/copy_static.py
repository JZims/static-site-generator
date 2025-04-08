import os, shutil

def copy_static_files(source, destination):
        # Delete all contents in public folder if it exists
            # perform a check to ensure it's clean
        if not os.path.exists(destination):
             os.mkdir(destination)

        # Copy all files and subdirectories from Static
            # print each processed path to the console to show progress
        items=os.listdir(source)

        for item in items:
           source_path = os.path.join(source, item)
           dest_path = os.path.join(destination, item)
           
           if os.path.isfile(source_path):
               # if file, copy it
               print(f"Copying file: {source_path} to {dest_path}")
               shutil.copy(source_path, dest_path)
           else:
               # if it's a dir, create it in destination and recursively call function
               print(f"Creating directory: {dest_path}")
               os.mkdir(dest_path)
               copy_static_files(source_path, dest_path)