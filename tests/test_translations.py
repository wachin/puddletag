import importlib.util
from importlib.machinery import SourceFileLoader
import os
from pathlib import Path
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

    def test_documented_automatic_locale_commands_match_bundled_catalogs(self):
        launcher = load_launcher()
        languages = {
            "afr": "/tmp/puddletag_afr.qm",
            "cs": "/tmp/puddletag_cs.qm",
            "de": "/tmp/puddletag_de.qm",
            "es_ES": "/tmp/puddletag_es_ES.qm",
            "fr": "/tmp/puddletag_fr.qm",
            "it": "/tmp/puddletag_it.qm",
            "nl-nl": "/tmp/puddletag_nl-nl.qm",
            "pl_PL": "/tmp/puddletag_pl_PL.qm",
            "pt_BR": "/tmp/puddletag_pt_BR.qm",
            "ru_RU": "/tmp/puddletag_ru_RU.qm",
            "sv": "/tmp/puddletag_sv.qm",
        }

        cases = {
            "afr.UTF-8": "/tmp/puddletag_afr.qm",
            "cs.UTF-8": "/tmp/puddletag_cs.qm",
            "de.UTF-8": "/tmp/puddletag_de.qm",
            "es_EC.UTF-8": "/tmp/puddletag_es_ES.qm",
            "fr.UTF-8": "/tmp/puddletag_fr.qm",
            "it.UTF-8": "/tmp/puddletag_it.qm",
            "nl_NL.UTF-8": "/tmp/puddletag_nl-nl.qm",
            "pl_PL.UTF-8": "/tmp/puddletag_pl_PL.qm",
            "pt_BR.UTF-8": "/tmp/puddletag_pt_BR.qm",
            "ru_RU.UTF-8": "/tmp/puddletag_ru_RU.qm",
            "sv.UTF-8": "/tmp/puddletag_sv.qm",
        }

        for lang, expected in cases.items():
            with self.subTest(lang=lang):
                self.assertEqual(
                    launcher.select_language_file(
                        "auto",
                        languages,
                        ["C"],
                        {"LC_ALL": "", "LANG": lang},
                    ),
                    expected,
                )

    def test_all_bundled_translation_catalogs_are_represented_in_locale_tests(self):
        catalogs = {
            path.stem.removeprefix("puddletag_")
            for path in Path("puddlestuff/translations").glob("puddletag_*.qm")
        }

        tested_catalogs = {
            "afr",
            "cs",
            "de",
            "es_ES",
            "fr",
            "it",
            "nl-nl",
            "pl_PL",
            "pt_BR",
            "ru_RU",
            "sv",
        }

        self.assertEqual(catalogs, tested_catalogs)


if __name__ == "__main__":
    unittest.main()
