

def extract_title(markdown_path):
    example_dir = open(markdown_path, "r")
    lines = example_dir.readlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No titla found.")
   