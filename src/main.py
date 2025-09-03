from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import text_node_to_html_node, publish_static, generate_page
import os

publish_static()
generate_page("content/index.md", "template.html", "public/index.html")

