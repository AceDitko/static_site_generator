import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"https://www.google.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src":"https://www.google.com", "alt":"This is an image node"})

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

class TestExtractMarkDown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)
