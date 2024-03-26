from htmlnode import ParentNode
from inline_transform import text_to_html_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        type = block_to_block_type(block)

        if type == block_type_p:
            nodes.append(p_block_to_html_node(block))
        if type == block_type_h:
            nodes.append(h_block_to_html_node(block))
        if type == block_type_c:
            nodes.append(c_block_to_html_node(block))
        if type == block_type_bq:
            nodes.append(bq_block_to_html_node(block))
        if type == block_type_ul:
            nodes.append(ul_block_to_html_node(block))
        if type == block_type_ol:
            nodes.append(ol_block_to_html_node(block))

    return ParentNode("div", nodes)


def markdown_to_blocks(markdown):
    lines = map(lambda x: x.lstrip(" "), markdown.split("\n"))

    blocks = []
    block = []

    for line in lines:
        if len(line) < 1:
            if len(block) < 1:
                continue
            blocks.append("\n".join(block))
            block = []
            continue
        block.append(line)

    return blocks


block_type_p = "paragraph"
block_type_h = "heading"
block_type_c = "code"
block_type_bq = "quote"
block_type_ul = "unordered_list"
block_type_ol = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")
    first_line = lines[0]
    if first_line.startswith("#") and len(first_line.split(" ")) > 1:
        return block_type_h
    if first_line == "```" and len(lines) > 1 and lines[-1] == "```":
        return block_type_c
    if all(x.startswith(">") for x in lines):
        return block_type_bq
    if all(x.startswith("*") for x in lines):
        return block_type_ul
    if all(x.startswith("-") for x in lines):
        return block_type_ul

    if first_line.startswith("1."):
        ol = True
        for i in range(0, len(lines)):
            if not lines[i].startswith(f"{i+1}."):
                ol = False

        if ol:
            return block_type_ol

    return block_type_p


def p_block_to_html_node(block):
    return ParentNode("p", text_to_html_nodes(" ".join(block.split("\n"))))


def h_block_to_html_node(block):
    parts = block.split(" ", 1)
    level = len(parts[0])

    return ParentNode(f"h{level}", text_to_html_nodes(parts[1]))


def c_block_to_html_node(block):
    lines = block.split("\n")[1:-1]

    return ParentNode("pre", [ParentNode("code", text_to_html_nodes(" ".join(lines)))])


def bq_block_to_html_node(block):
    lines = map(lambda x: x[2:], block.split("\n"))

    return ParentNode("blockquote", text_to_html_nodes(" ".join(lines)))


def ul_block_to_html_node(block):
    nodes = map(lambda x: ParentNode("li", text_to_html_nodes(x[2:])), block.split("\n"))

    return ParentNode("ul", nodes)


def ol_block_to_html_node(block):
    nodes = map(lambda x: ParentNode("li", text_to_html_nodes(x[3:])), block.split("\n"))

    return ParentNode("ol", nodes)
