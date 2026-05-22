import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtCore import QTranslator
from PyQt6.QtWidgets import QApplication


app = QApplication.instance() or QApplication([])


EXPECTED_FIELD_TRANSLATIONS = {
    "puddletag_afr.qm": {
        "Artist": "Kunstenaar",
        "Title": "Titel",
        "Album": "Album",
        "Track": "Nommer",
        "Year": "Jaar",
        "Genre": "Genre",
        "Comment": "Kommentaar",
    },
    "puddletag_cs.qm": {
        "Artist": "Umělec",
        "Title": "Název",
        "Album": "Album",
        "Track": "Skladba",
        "Year": "Rok",
        "Genre": "Žánr",
        "Comment": "Poznámka",
    },
    "puddletag_de.qm": {
        "Artist": "Interpret",
        "Title": "Titel",
        "Album": "Album",
        "Track": "Track",
        "Year": "Jahr",
        "Genre": "Genre",
        "Comment": "Kommentar",
    },
    "puddletag_es_ES.qm": {
        "Artist": "Artista",
        "Title": "Título",
        "Album": "Álbum",
        "Track": "Pista",
        "Year": "Año",
        "Genre": "Género",
        "Comment": "Comentario",
    },
    "puddletag_fr.qm": {
        "Artist": "Artiste",
        "Title": "Titre",
        "Album": "Album",
        "Track": "Piste",
        "Year": "Année",
        "Genre": "Genre",
        "Comment": "Commentaire",
    },
    "puddletag_it.qm": {
        "Artist": "Artista",
        "Title": "Titolo",
        "Album": "Album",
        "Track": "Traccia",
        "Year": "Anno",
        "Genre": "Genere",
        "Comment": "Commento",
    },
    "puddletag_nl-nl.qm": {
        "Artist": "Artiest",
        "Title": "Titel",
        "Album": "Album",
        "Track": "Nummer",
        "Year": "Jaar",
        "Genre": "Genre",
        "Comment": "Commentaar",
    },
    "puddletag_pl_PL.qm": {
        "Artist": "Artysta",
        "Title": "Tytuł",
        "Album": "Album",
        "Track": "Utwór",
        "Year": "Rok",
        "Genre": "Gatunek",
        "Comment": "Komentarz",
    },
    "puddletag_pt_BR.qm": {
        "Artist": "Artista",
        "Title": "Título",
        "Album": "Álbum",
        "Track": "Faixa",
        "Year": "Ano",
        "Genre": "Gênero",
        "Comment": "Comentário",
    },
    "puddletag_ru_RU.qm": {
        "Artist": "Артист",
        "Title": "Заголовок",
        "Album": "Альбом",
        "Track": "Трек",
        "Year": "Год",
        "Genre": "Жанр",
        "Comment": "Комментарий",
    },
    "puddletag_sv.qm": {
        "Artist": "Artist",
        "Title": "Titel",
        "Album": "Album",
        "Track": "Spår",
        "Year": "År",
        "Genre": "Genre",
        "Comment": "Kommentar",
    },
}


class TestFieldTranslations(unittest.TestCase):
    def test_bundled_catalogs_translate_default_table_fields(self):
        for catalog, expected in EXPECTED_FIELD_TRANSLATIONS.items():
            with self.subTest(catalog=catalog):
                translator = QTranslator()
                path = str(Path("puddlestuff/translations") / catalog)
                self.assertTrue(translator.load(path))

                app.installTranslator(translator)
                try:
                    translated = {
                        source: QApplication.translate("Fields", source)
                        for source in expected
                    }
                finally:
                    app.removeTranslator(translator)

                self.assertEqual(translated, expected)

    def test_saved_english_default_table_headers_are_retranslated(self):
        from puddlestuff import tagmodel

        translator = QTranslator()
        self.assertTrue(
            translator.load("puddlestuff/translations/puddletag_es_ES.qm")
        )

        app.installTranslator(translator)
        try:
            titles = tagmodel._table_titles(
                tagmodel.DEFAULT_TABLE_TITLE_KEYS,
                tagmodel.DEFAULT_TABLE_TAGS,
            )
        finally:
            app.removeTranslator(translator)

        expected = {
            "artist": "Artista",
            "title": "Título",
            "album": "Álbum",
            "track": "Pista",
            "year": "Año",
            "genre": "Género",
            "comment": "Comentario",
        }

        translated_by_tag = dict(zip(tagmodel.DEFAULT_TABLE_TAGS, titles))
        for tag, title in expected.items():
            self.assertEqual(translated_by_tag[tag], title)


if __name__ == "__main__":
    unittest.main()
