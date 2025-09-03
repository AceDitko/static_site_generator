from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import text_node_to_html_node, publish_static, generate_pages_recursive
import sys


basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]

publish_static("static", "docs")
generate_pages_recursive("content", "template.html", "docs", basepath)

