from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import TextType, text_node_to_html_node
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
    heading=re.match(r'^#{1,6}\s', block)
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
    

def text_to_children(markdown):
    all_text_nodes=text_to_textnodes(markdown)
    child_nodes=[]
    for node in all_text_nodes:
        if node.text_type != TextType.TEXT:
            child_nodes.append(text_node_to_html_node(node).to_html())
    return child_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_with_types = list(zip(blocks,map(lambda x: block_to_block_type(x).value, blocks)))
    child_nodes=[]
    wrapper = ParentNode('div', child_nodes)

    for block in block_with_types:
        stylized_text = "".join(list(map(lambda x: x.to_html(), map(lambda x: text_node_to_html_node(x), text_to_textnodes(block[0])))))
        child_nodes.append(LeafNode(block[1], stylized_text))
        # Determine which are parent nodes and which are leaf nodes

    return wrapper.to_html()

md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
print(markdown_to_html_node(md))
