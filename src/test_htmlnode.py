import unittest

from htmlnode import HTMLNode

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
   