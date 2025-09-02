import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import text_node_to_html_node, split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT)
        ]
        desired = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), desired)

    def test_bold(self):
        nodes = [
            TextNode("This is text with a **bold** word", TextType.TEXT)
        ]
        desired = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), desired)

    def test_italic(self):
        nodes = [
            TextNode("This is text with an __italic__ word", TextType.TEXT)
        ]
        desired = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "__", TextType.ITALIC), desired)


    def test_double_code(self):
        nodes = [
            TextNode("This is text with two `code block` words in the `same` sentence", TextType.TEXT)
        ]
        desired = [
            TextNode("This is text with two ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" words in the ", TextType.TEXT),
            TextNode("same", TextType.CODE),
            TextNode(" sentence", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), desired)