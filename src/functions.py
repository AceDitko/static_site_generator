import re
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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
        #    raise TypeError("Error: Cannot delimit non-text nodes")
            output.append(node)
            continue
        pieces = node.text.split(delimiter)
        tmp_result = [TextNode(pieces[i], TextType.TEXT) if i % 2 == 0 else TextNode(pieces[i], text_type) for i in range(len(pieces))]
        output.extend(tmp_result)
    return output


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return [(match[0], match[1]) for match in matches]


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return [(match[0], match[1]) for match in matches]


def split_nodes_image(old_nodes):
    output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
        #    raise TypeError("Error: Cannot delimit non-text nodes")
            output.append(node)
            continue
        pieces = re.split(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', node.text)
        tmp_result = []
        for i in range(0, len(pieces)-1, 3):
            if pieces[i]:
                tmp_result.append(TextNode(pieces[i], TextType.TEXT))
            tmp_result.append(TextNode(pieces[i+1], TextType.IMAGE, pieces[i+2]))
        if len(pieces) % 3 == 1 and pieces[-1]:
            tmp_result.append(TextNode(pieces[-1], TextType.TEXT))
        output.extend(tmp_result)
    return output
    

def split_nodes_link(old_nodes):
    output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            #raise TypeError("Error: Cannot delimit non-text nodes")
            output.append(node)
            continue
        pieces = re.split(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', node.text)
        tmp_result = []
        for i in range(0, len(pieces)-1, 3):
            if pieces[i]:
                tmp_result.append(TextNode(pieces[i], TextType.TEXT))
            tmp_result.append(TextNode(pieces[i+1], TextType.LINK, pieces[i+2]))
        if len(pieces) % 3 == 1 and pieces[-1]:
            tmp_result.append(TextNode(pieces[-1], TextType.TEXT))
        output.extend(tmp_result)
    return output


def text_to_textnodes(text):
    output = [TextNode(text, TextType.TEXT)]
    output = split_nodes_delimiter(output, "**", TextType.BOLD)
    output = split_nodes_delimiter(output, "_", TextType.ITALIC)
    output = split_nodes_delimiter(output, "`", TextType.CODE)
    output = split_nodes_image(output)
    output = split_nodes_link(output)
    return output


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]


def block_to_block_type(markdown):
    if re.match(r'#+ ', markdown[:7]):
        return BlockType.HEADING
    elif markdown.split("\n")[0].startswith('```') and markdown.split("\n")[-1].endswith('```'):
        return BlockType.CODE
    elif all([piece.startswith('>') for piece in markdown.split("\n")]):
        return BlockType.QUOTE
    elif all([piece.startswith('- ') for piece in markdown.split("\n")]):
        return BlockType.UNORDERED_LIST
    elif all([line.split(". ")[0].isdigit() and int(line.split(". ")[0]) == i+1 for i, line in enumerate(markdown.split("\n")) if line.strip()]):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH