from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
    )

from htmlnode import LeafNode


def text_to_html_nodes(text):
    nodes = text_to_textnodes(text)
    return map(text_node_to_html_node, nodes)


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    value = text_node.text

    if text_type == text_type_text:
        return LeafNode(None, value)

    if text_type == text_type_bold:
        return LeafNode("b", value)
    if text_type == text_type_italic:
        return LeafNode("i", value)
    if text_type == text_type_code:
        return LeafNode("code", value)
    if text_type == text_type_link:
        return LeafNode("a", value, {"href": text_node.url})
    if text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url,
                                    "alt": text_node.text,
                                    })


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) == 0:
            continue
        if len(parts) % 2 == 0:
            raise ValueError("Invalid: mising closing delimiter")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                nodes.append(TextNode(parts[i], text_type_text))
            else:
                nodes.append(TextNode(parts[i], text_type))

    return nodes


def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            nodes.append(node)
            continue
        images = extract_markdown_images(node.text)

        text = node.text
        for image in images:
            parts = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(parts[0]) > 0:
                nodes.append(TextNode(parts[0], text_type_text))
            nodes.append(TextNode(image[0], text_type_image, image[1]))
            text = parts[1]

        if len(text) > 0:
            nodes.append(TextNode(text, text_type_text))

    return nodes


def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            nodes.append(node)
            continue
        links = extract_markdown_links(node.text)

        text = node.text
        for link in links:
            parts = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(parts[0]) > 0:
                nodes.append(TextNode(parts[0], text_type_text))
            nodes.append(TextNode(link[0], text_type_link, link[1]))
            text = parts[1]

        if len(text) > 0:
            nodes.append(TextNode(text, text_type_text))

    return nodes


def extract_markdown_images(text):
    if len(text) < 1:
        return []
    images = []
    try:
        bang = text.index("!")
        text = text[bang:]
        alt_start = text.index("[")
        alt_end = text.index("]")
        if alt_start > alt_end:
            raise ValueError("Invalid: image missing alt closing bracket")

        url_start = text.index("(")

        if url_start != alt_end + 1:
            raise ValueError("Invalid: image missing url after alt")

        url_end = text.index(")")

        if url_start > url_end:
            raise ValueError("Invalid: image url closing bracket")
    except ValueError:
        return []

    alt_text = text[alt_start+1:alt_end]
    url = text[url_start+1:url_end]
    images.append((alt_text, url))

    new_text = text[url_end + 1:]
    images.extend(extract_markdown_images(new_text))
    return images


def extract_markdown_links(text):
    if len(text) < 1:
        return []
    links = []
    try:
        alt_start = text.index("[")
        if text[alt_start - 1] == "!":
            raise ValueError("Invalid: parsing image as link")
        text = text[alt_start:]
        alt_end = text.index("]")

        url_start = text.index("(")

        if url_start != alt_end + 1:
            raise ValueError("Invalid: link missing url after link text.")

        url_end = text.index(")")

        if url_start > url_end:
            raise ValueError("Invalid: link url closing bracket")

    except ValueError:
        return []
    link_text = text[1:alt_end]
    url = text[url_start+1:url_end]
    links.append((link_text, url))
    new_text = text[url_end + 1:]
    links.extend(extract_markdown_links(new_text))
    return links
