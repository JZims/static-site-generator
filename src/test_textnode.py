import unittest
from textnode import TextNode, TextType, text_node_to_html_node



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("this is a text node", TextType.ITALIC)
        self.assertFalse(node.url)
    
    def test_text_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "lul.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "lul.com")
        if self.assertEqual(node.text, node2.text):
            print("Text is equal")
            return True
        else:
            return False
        
    def test_text_type_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "lul.com")
        node2 = TextNode("This is (probably) a text node", TextType.BOLD, "lul.com")
        if self.assertEqual(node.text_type, node2.text_type):
            return "Text type is equal"
        else:
            return False
    def test_err_on_type_mismatch(self):
        self.assertRaises(ValueError, TextNode, "This is a text node", "bold")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()