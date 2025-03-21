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
        self.assertEqual(node.text, node2.text, msg="Text is Equal")
        
    def test_text_type_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "lul.com")
        node2 = TextNode("This is (probably) a text node", TextType.BOLD, "lul.com")
        self.assertEqual(node.text_type, node2.text_type, msg="Text type is equal")

    def test_err_on_type_mismatch(self):
        self.assertRaises(ValueError, TextNode, "This is a text node", "bold")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_url(self):
        node = TextNode("This is a Link node", TextType.LINK, "www.test.omg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a Link node")

    

if __name__ == "__main__":
    unittest.main()