import unittest

from puddlestuff.plugindocs import (
    iter_plugin_docs,
    plugins_rst,
)


class TestPluginDocs(unittest.TestCase):
    def test_plugin_docs_use_bundled_plugin_info(self):
        rows = {row.module: row for row in iter_plugin_docs()}

        self.assertIn("view_all_fields", rows)
        self.assertEqual(rows["view_all_fields"].name, "View All Fields")
        self.assertEqual(rows["view_all_fields"].version, "1.0")
        self.assertEqual(rows["view_all_fields"].author, "concentricpuddle")
        self.assertIn("extended_tags", rows)
        self.assertEqual(rows["extended_tags"].version, "1.2")

    def test_plugins_without_info_are_skipped(self):
        modules = {row.module for row in iter_plugin_docs()}

        self.assertNotIn("export_tags", modules)

    def test_plugins_rst_contains_registry_table(self):
        rst = plugins_rst()

        self.assertIn("Generated Plugin Reference", rst)
        self.assertIn(
            "This table is generated from the bundled plugin registry", rst)
        self.assertIn("``view_all_fields``", rst)
        self.assertTrue(rst.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
