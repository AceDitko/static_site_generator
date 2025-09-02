import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})
    else:
        raise TypeError("Error: text_node is of invalid TextType!")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            raise TypeError("Error: Cannot delimit non-text nodes")
        pieces = node.text.split(delimiter)
        tmp_result = [TextNode(pieces[i], TextType.TEXT) if i % 2 == 0 else TextNode(pieces[i], text_type) for i in range(len(pieces))]
        output.extend(tmp_result)
    return output