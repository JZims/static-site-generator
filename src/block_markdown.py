from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
import re

class BlockType(Enum):
    PARA="p"
    HEAD="h1"
    CODE="code"
    QUOTE="quote"
    UOL="ul"
    OL="ol"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks=[]
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    heading=re.match(r'^#{3,6}\s', block)
    if heading:
        return BlockType("h1")
    code=re.match(r'^```[\s\S]*```$', block)
    if code:
        return BlockType("code")
    quote=re.match(r'^\>', block)
    if quote:
        return BlockType("quote")
    unordered=re.match(r'^\- ', block)
    if unordered:
        return BlockType("ul")
    ordered=re.match(r'^\d\. ', block)
    if ordered:
        return BlockType("ol")
    else:
        return BlockType("p")
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_with_types = list(zip(blocks,map(lambda x: block_to_block_type(x).value, blocks)))
    html_nodes=[]
    for block in block_with_types:

        # Determine which are parent nodes and which are leaf nodes
        # html_node = LeafNode(block[1], block[0]).to_html()
        # html_nodes.append(html_node)
   
    return html_nodes

md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
print(markdown_to_html_node(md))