import re
import os
import shutil

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
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            text = " ".join(line.strip() for line in lines if line.strip() != "")
            p_children = text_to_children(text)
            children.append(ParentNode("p",p_children))
        elif block_type == BlockType.HEADING:
            line = block.split("\n", 1)[0]
            pieces = line.split(" ")
            level = len(pieces[0])
            text = " ".join(pieces[1:]).strip()
            p_children = text_to_children(text)
            children.append(ParentNode(f"h{level}",p_children))
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            inner = "\n".join(lines[1:-1])
            if block.endswith("\n```"):
                inner += "\n"
            code_leaf = LeafNode("code", inner)
            children.append(ParentNode("pre",[code_leaf]))
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            stripped = [re.sub(r"^>\s?", "", l) for l in lines]
            text = " ".join(s.strip() for s in stripped if s.strip())
            children.append(ParentNode("blockquote", text_to_children(text)))
        elif block_type == BlockType.UNORDERED_LIST:
            items =  [re.sub(r"^-\s", "", l, count=1).strip() for l in block.split("\n")]
            list_nodes = [ParentNode("li", text_to_children(t)) for t in items if t]
            children.append(ParentNode("ul",list_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            items = [re.sub(r"^\d+\.\s", "", l, count=1).strip() for l in block.split("\n")]
            list_nodes = [ParentNode("li", text_to_children(t)) for t in items if t]
            children.append(ParentNode("ol", list_nodes))
    return ParentNode("div", children)


def text_to_children(text):
    if text.strip() == "":
        return []
    try:
        text_nodes = text_to_textnodes(text)
        children = [text_node_to_html_node(node) for node in text_nodes if node.text != ""]
        return children
    except Exception as e:
        raise ValueError(f"Error - Invalid inline markdown: {e}")
    

def publish_static(source="static", destination="docs"):
    source_path = os.path.abspath(source)
    destination_path = os.path.abspath(destination)

    if not os.path.isdir(source_path):
        raise ValueError('Error: Invalid source directory - source path is not a directory!')
    
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)

    os.makedirs(destination_path, exist_ok=True)

    def copy_dir(src, dst):
        for item in os.listdir(src):
            src_child = os.path.join(src, item)
            dst_child = os.path.join(dst, item)
            if os.path.isfile(src_child):
                shutil.copy(src_child, dst_child)
            elif os.path.isdir(src_child):
                os.makedirs(dst_child, exist_ok=True)
                copy_dir(src_child, dst_child)
    copy_dir(source_path, destination_path)


def extract_title(markdown):
    title_lines = [line for line in markdown.split("\n") if line.startswith('# ')]
    if len(title_lines) < 1:
        raise Exception("Error: no title detected!")
    else:
        return title_lines[0][2:].strip()


def generate_page(from_path, template_path, dest_path, basepath):
    if not os.path.exists(from_path):
        raise ValueError(f"Error: from_path '{from_path}' does not exist!")
    if not os.path.exists(template_path):
        raise ValueError(f"Error: template_path '{template_path}' does not exist!")
    if not os.path.isfile(from_path):
        raise ValueError(f"Error: {from_path} does not point to a valid file!")
    if not os.path.isfile(template_path):
        raise ValueError(f"Error: {template_path} does not point to a valid file!")
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        file_content = f.read()

    with open(template_path, "r") as t:
        template_content = t.read()
    
    file_content_html = markdown_to_html_node(file_content).to_html()
    title = extract_title(file_content)

    template_content = template_content.replace('{{ Title }}', title)
    template_content = template_content.replace('{{ Content }}', file_content_html)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as d:
        d.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Error: dir_path_content '{dir_path_content}' does not exist!")
    if not os.path.exists(template_path):
        raise ValueError(f"Error: template_path '{template_path}' does not exist!")
    if not os.path.isdir(dir_path_content):
        raise ValueError(f"Error: {dir_path_content} does not point to a directory!")
    if not os.path.isfile(template_path):
        raise ValueError(f"Error: {template_path} does not point to a valid file!")
    
    if not os.path.exists(os.path.abspath(dest_dir_path)):
        os.makedirs(os.path.abspath(dest_dir_path), exist_ok=True)

    for item in os.listdir(dir_path_content):
        src_child = os.path.join(dir_path_content, item)
        dst_child = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_child):
            if '.md' in item:
                new_item = item.removesuffix('.md')
                new_item += '.html'
                dst_child = os.path.join(dest_dir_path, new_item)
                generate_page(src_child, template_path, dst_child, basepath)
            else:
                shutil.copy(src_child, dst_child)
        else:
            os.makedirs(dst_child, exist_ok=True)
            generate_pages_recursive(src_child, template_path, dst_child, basepath)