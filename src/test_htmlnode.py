import unittest

from htmlnode import HTMLNode, LeafNode

class TextHTMLNode(unittest.TestCase):
    def test_noneProp(self):
        node = HTMLNode("p", "I love refrigerators", [])
        self.assertEqual(node.props_to_html(), "")

    def test_oneProp(self):
        node = HTMLNode("p", "I love refrigerators", [], {"class": "my-class"})
        self.assertEqual(node.props_to_html(), ' class="my-class"')

    def test_twoProp(self):
        node = HTMLNode("p", "I love refrigerators", [], {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
   
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')