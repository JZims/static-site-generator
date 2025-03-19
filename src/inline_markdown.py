import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # initialize List to be built
    new_nodes = []
    # Iterate through old nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # Split words by delimiter
        split_nodes=[]
        word_sections = node.text.split(delimiter)
        for i in range(len(word_sections)):
            if word_sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(word_sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(word_sections[i], text_type))
        new_nodes.extend(split_nodes) 
    return new_nodes
    

def split_nodes_image(old_node):
    new_nodes = []
    for node in old_node:
        found_images=extract_markdown_images(node)
        if not found_images:
            new_nodes.append(TextNode(node, TextType.TEXT))
        else:
        # Unpack furst tuple
            img_alt, img_url = found_images[0]
        # Split Node on this info
            split_node = node.text.split(f"![{img_alt}]({img_url})", 1)
            first_half = split_node[0]
            second_half = split_node[1] if len(split_node[1]) > 1 else ""

            if first_half.strip():
                new_nodes.append(TextNode(first_half, TextType.TEXT))

            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))
            
        # If second half of node exists, format it into a node and recurse
            if second_half.strip():
                remaining_node = TextNode(second_half, TextType.TEXT)
                new_nodes += split_nodes_image([remaining_node])
    return new_nodes

def split_nodes_link(old_node):
    new_nodes = []
    for node in old_node:
        found_links=extract_markdown_link(node)
        if not found_links:
            new_nodes.append(TextNode(node, TextType.TEXT))
        else:
        # Unpack furst tuple
            link_alt, link_url = found_links[0]
        # Split Node on this info
            split_node = node.text.split(f"[{link_alt}]({link_url})", 1)
            first_half = split_node[0]
            second_half = split_node[1] if len(split_node[1]) > 1 else ""

            if first_half.strip():
                new_nodes.append(TextNode(first_half, TextType.TEXT))

            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            
        # If second half of node exists, format it into a node and recurse
            if second_half.strip():
                remaining_node = TextNode(second_half, TextType.TEXT)
                new_nodes += split_nodes_link([remaining_node])
    return new_nodes

def extract_markdown_images(sample_text):
    img_node_alt_text= re.findall(r"\!\[(.*?)\]", sample_text.text)
    img_node_url = re.findall(r"\((https?://[^\s)]+)\)", sample_text.text)

    md_images = list(zip(img_node_alt_text, img_node_url))
    return md_images
    
def extract_markdown_link(sample_text):
    link_node_alt_text= re.findall(r"\[(.*?)\]", sample_text[0][0])
    link_node_url= re.findall(r"\((https?://[^\s)]+)\)", sample_text[0][1])
    md_links = list(zip(link_node_alt_text, link_node_url))
    return md_links

def text_to_textnodes(text):
    nodes=[TextNode(text, TextType.TEXT)]

    # For bold nodes using split_nodes_delimiter
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # For italic nodes
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # For code nodes
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes