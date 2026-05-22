import importlib.util
from importlib.machinery import SourceFileLoader
import os
import unittest


def load_launcher():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "puddletag"))
    loader = SourceFileLoader("puddletag_launcher", path)
    spec = importlib.util.spec_from_loader("puddletag_launcher", loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestTranslations(unittest.TestCase):
    def test_auto_language_falls_back_to_same_language_catalog(self):
        launcher = load_launcher()
        languages = {
            "es_ES": "/tmp/puddletag_es_ES.qm",
            "es-ES": "/tmp/puddletag_es_ES.qm",
        }

        self.assertEqual(
            launcher.select_language_file("auto", languages, ["es-EC"], {}),
            "/tmp/puddletag_es_ES.qm",
        )

    def test_auto_language_uses_lang_when_qt_reports_c_locale(self):
        launcher = load_launcher()
        languages = {"es_ES": "/tmp/puddletag_es_ES.qm"}

        self.assertEqual(
            launcher.select_language_file(
                "auto",
                languages,
                ["C"],
                {"LC_ALL": "C.UTF-8", "LANG": "es_EC.UTF-8"},
            ),
            "/tmp/puddletag_es_ES.qm",
        )

    def test_auto_language_does_not_override_english_qt_locale(self):
        launcher = load_launcher()
        languages = {"es_ES": "/tmp/puddletag_es_ES.qm"}

        self.assertIsNone(
            launcher.select_language_file(
                "auto",
                languages,
                ["en-US", "en"],
                {"LANG": "es_EC.UTF-8"},
            )
        )


if __name__ == "__main__":
    unittest.main()
