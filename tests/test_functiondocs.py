import unittest

from puddlestuff.functiondocs import (
    action_functions_rst,
    iter_action_function_docs,
)


class TestFunctionDocs(unittest.TestCase):
    def test_action_function_docs_use_registered_function_docstrings(self):
        rows = list(iter_action_function_docs())
        by_key = {row.key: row for row in rows}

        self.assertIn("autonumbering", by_key)
        self.assertEqual(by_key["autonumbering"].name, "Autonumbering")
        self.assertEqual(
            by_key["autonumbering"].arguments,
            ("Start", "Restart for dir", "Padding"),
        )
        self.assertIn("save_artwork", by_key)
        self.assertEqual(by_key["save_artwork"].name, "Export artwork to file")

    def test_action_functions_rst_contains_registry_table(self):
        rst = action_functions_rst()

        self.assertIn("Generated Function Reference", rst)
        self.assertIn("This table is generated from the action function registry", rst)
        self.assertIn("``autonumbering``", rst)
        self.assertIn("``save_artwork``", rst)
        self.assertTrue(rst.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
