import unittest
from msg_split import split_html_structure, FragmentTooLargeError


class TestSplitHtmlPreservingStructure(unittest.TestCase):
    def test_simple_split(self):
        html_content = "<p>Hello, world!</p><p>This is a test.</p>"
        max_len = 20
        result = split_html_structure(html_content, max_len=max_len)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "<p>Hello, world!</p>")
        self.assertEqual(result[1], "<p>This is a test.</p>")


    def test_large_fragment(self):
        html_content = "<p>" + "A" * 500 + "</p>"
        max_len = 400

        with self.assertRaises(FragmentTooLargeError) as context:
            split_html_structure(html_content, max_len=max_len)

        self.assertIn(f"Текстовый элемент слишком велик для max_len ({max_len} символов)", str(context.exception))

    def test_nested_structure(self):
        html_content = ("<div><p><b>Important: Hello, world!</b>"
                        "This is a test sentence that exceeds the max length for splitting.</p>"
                        "<p>This is another paragraph.</p></div>")
        max_len = 100

        result = split_html_structure(html_content, max_len=max_len)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "<div><p><b>Important: Hello, world!</b></p></div>")
        self.assertEqual(result[1], "<div><p>This is a test sentence that exceeds the max length for splitting."
                                    "</p><p></p></div>")
        self.assertEqual(result[2], "<div><p>This is another paragraph.</p></div>")

    def test_only_text(self):
        html_content = "Hello, world! This is a test."
        max_len = 50
        result = split_html_structure(html_content, max_len=max_len)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Hello, world! This is a test.")

    def test_empty_content(self):
        html_content = ""
        max_len = 10
        result = split_html_structure(html_content, max_len=max_len)

        self.assertEqual(result, [])

    def test_fragment_length(self):
        html_content = "<p>Hello, <b>world!</b> This is <i>a test</i>.</p>"
        max_len = 30
        result = split_html_structure(html_content, max_len=max_len)

        for fragment in result:
            self.assertLessEqual(len(fragment), max_len)



if __name__ == "__main__":
    unittest.main()