from inline_markdown import (
    split_nodes_delimiter, 
    split_nodes_image, 
    split_nodes_link, 
    extract_markdown_images, 
    extract_markdown_link, 
    text_to_textnodes
)
import unittest
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):

    def test_text_delimitter(self):
            old_nodes = [
                TextNode("This is text with a `code block` word", TextType.TEXT)
            ]
            new_nodes_expected = [ 
                TextNode("This is text with a ",TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT) 
            ]
            self.assertListEqual(new_nodes_expected, split_nodes_delimiter(old_nodes, "`", TextType.CODE))

    def test_delim_bold(self):
            node = TextNode("This is text with a **bolded** word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded", TextType.BOLD),
                    TextNode(" word", TextType.TEXT),
                ],
                new_nodes,
            )
    def test_delim_bold_multiword(self):
            node = TextNode(
                "This is text with a **bolded word** and **another**", TextType.TEXT
            )
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded word", TextType.BOLD),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("another", TextType.BOLD),
                ],
                new_nodes,
            )

    def test_delim_bold_and_italic(self):
            node = TextNode("**bold** and _italic_", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
            self.assertListEqual(
                [
                    TextNode("bold", TextType.BOLD),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                ],
                new_nodes,
            )
    def test_extract_markdown_images(self):
            matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
            matches = extract_markdown_link(
                "This is text with a [link]](https://www.link.com)"
            )
            self.assertListEqual([("link", "https://www.link.com")], matches)

    def test_extract_double_markdown_link(self):
            matches = extract_markdown_link(
                "This is text with a [link]](https://www.link.com) but there's [another link](https://www.anotherlink.com) as well!"
            )
            self.assertListEqual([("link", "https://www.link.com"), ("another link", "https://www.anotherlink.com" )], matches)

    def test_split_images(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes
        )
            
    def test_split_links(self):
            node = TextNode(
                "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_link([node])
            self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode(
                        "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                    ),
                ],
                new_nodes
        )
    def test_text_to_textnodes(self):
        sample_node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(sample_node)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ], 
        new_nodes
        )

    def test_text_to_textnodes_basic(self):
        text = "This is **bold** text with _italic_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD), 
            TextNode(" text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC)
        ]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_nested(self):
        text = "**Bold _italic_ text**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold ", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.BOLD)
        ]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_code(self):
        text = "Text with `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertListEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()