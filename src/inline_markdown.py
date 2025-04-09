import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # initialize List to be built
    new_nodes = []
    # Iterate through old nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT and node.text_type != text_type:
            inner_splits = node.text.split(delimiter)
            if len(inner_splits) > 1:
                current_type = node.text_type
                for i, split in enumerate(inner_splits):
                    if split == "":
                        continue
                    if  1 % 2 == 0:
                        new_nodes.append(TextNode(split, current_type))
                    else:
                        new_nodes.append(TextNode(split, text_type))
            else:
                new_nodes.append(node)
            continue

        word_sections = node.text.split(delimiter)
        if len(word_sections) % 2 ==0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i, split in enumerate(word_sections):
            if split == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split, TextType.TEXT))
            else:
                new_nodes.append(TextNode(split, text_type))

    return new_nodes
    

def split_nodes_image(old_node):
    new_nodes = []
    for node in old_node:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        found_images=extract_markdown_images(original_text)

        if len(found_images) == 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
            continue

        for image in found_images:
            img_alt, img_url = image
            sections = original_text.split(f"![{img_alt}]({img_url})", 1)

            first_half = sections[0]
            second_half = sections[1] if len(sections[1]) > 1 else ""

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            
            if first_half != "":
                new_nodes.append(TextNode(first_half, TextType.TEXT))

            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))
            original_text = second_half

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        found_links=extract_markdown_link(original_text)

        if len(found_links) == 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
            continue

        for link in found_links:
            link_alt, link_url = link
            sections = original_text.split(f"[{link_alt}]({link_url})", 1)

            first_half = sections[0]
            second_half = sections[1] if len(sections[1]) > 1 else ""

            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            
            if first_half != "":
                new_nodes.append(TextNode(first_half, TextType.TEXT))

            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            original_text = second_half
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    
    return new_nodes

def extract_markdown_images(sample_text):
    img_node_alt_text= re.findall(r"\!\[(.*?)\]", sample_text)
    img_node_url = re.findall(r"\(((?:https?://[^\s)]+)|(?:[^)\s]+))\)", sample_text)

    md_images = list(zip(img_node_alt_text, img_node_url))
    return md_images
    
def extract_markdown_link(sample_text):
    link_node_alt_text= re.findall(r"\[(.*?)\]", sample_text)
    link_node_url= re.findall(r"\(((?:https?://[^\s)]+)|(?:[^)\s]+))\)", sample_text)
    md_links = list(zip(link_node_alt_text, link_node_url))
    return md_links

def text_to_textnodes(text):
    nodes=[TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
