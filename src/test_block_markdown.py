import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from block_markdown import BlockType

class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        
    def test_block_to_block_type_paragraph(self):
        md="This is a paragraph"
        block_type =block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARA)

    def test_block_to_block_type_heading(self):
        md="#### This is a heading"
        block_type=block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEAD)

    def test_block_to_block_type_code(self):
        md="```This is a code block```"
        block_type=block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md="> this is a quote"
        block_type =block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        md="- This is a uol item"
        block_type =block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UOL)

    def test_block_to_block_type_ordered_list(self):
        md="1. This is a ordered list item"
        block_type =block_to_block_type(md)
        self.assertEqual(block_type, BlockType.OL)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md ="""
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    if __name__ == "__main__":
        unittest.main()