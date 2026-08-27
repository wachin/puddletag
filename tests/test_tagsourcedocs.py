import shutil
import unittest

from puddlestuff.tagsourcedocs import (
    iter_tag_source_docs,
    tag_sources_rst,
)


class TestTagSourceDocs(unittest.TestCase):
    def test_tag_source_docs_use_registered_sources(self):
        rows = {row.name: row for row in iter_tag_source_docs()}

        self.assertIn("Amazon", rows)
        self.assertIn("FreeDB", rows)
        self.assertIn("MusicBrainz", rows)
        self.assertEqual(rows["MusicBrainz"].group_by, ("album", "artist"))
        self.assertEqual(rows["FreeDB"].group_by, ("album",))
        self.assertFalse(rows["MusicBrainz"].supports_submit)

    def test_tag_source_docs_include_preferences(self):
        rows = {row.name: row for row in iter_tag_source_docs()}

        self.assertIn("Retrieve Cover (checkbox)", rows["Amazon"].preferences)
        self.assertIn(
            "Cover size to retrieve: (combo)", rows["MusicBrainz"].preferences)
        self.assertEqual(rows["FreeDB"].preferences, ())

    @unittest.skipUnless(shutil.which("fpcalc"),
                         "AcoustID requires the fpcalc binary")
    def test_acoustid_docs_support_submission(self):
        rows = {row.name: row for row in iter_tag_source_docs()}

        self.assertIn("AcoustID", rows)
        self.assertEqual(rows["AcoustID"].group_by, ("album",))
        self.assertTrue(rows["AcoustID"].supports_submit)

    def test_tag_sources_rst_contains_registry_table(self):
        rst = tag_sources_rst()

        self.assertIn("Generated Tag Source Reference", rst)
        self.assertIn(
            "This table is generated from the tag source registry", rst)
        self.assertIn("MusicBrainz", rst)
        self.assertIn("Retrieve Cover (checkbox)", rst)
        self.assertTrue(rst.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
