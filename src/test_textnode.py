import unittest

from textnode import (TextNode, text_type_bold, text_type_italic)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a different text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_different_text_type(self):
        node = TextNode("This is a text node", text_type_italic)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_missing_url(self):
        node = TextNode("This is a text node", text_type_bold, "https://example.com")
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_bold, "https://www.example.com")
        self.assertEqual(
            "TextNode(This is a text node, bold, https://www.example.com)",
            repr(node)
        )


if __name__ == "__main__":
    unittest.main()
