from importlib import import_module
from platform import python_version

import mutagen
from PyQt6.QtCore import PYQT_VERSION_STR, Qt, qVersion
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from . import changeset, version_string
from .puddleobjects import OKCancel
from .translations import translate

desc = translate(
    "About",
    """puddletag es un editor de etiquetas de audio para GNU/Linux similar al editor Mp3tag.

<br /><br />Incluye: edición de etiquetas por lotes, renombrar archivos usando etiquetas, extraer etiquetas desde el nombre de archivo, usar Acciones para automatizar tareas repetitivas, importar tu biblioteca musical y muchas cosas más. <br /><br />

Formatos soportados: id3v1, id3v2 (.mp3, .wav, .aac, .aiff, .dsf), AAC (.mp4, .m4a), VorbisComments (.ogg, .flac) y APEv2 (.ape, .ofr, .ofs, .tak, .tta) <br /><br />

Visita el sitio web de puddletag (<a href="https://docs.puddletag.net/">https://docs.puddletag.net/</a>) para ayuda y novedades.<br /><br />
&copy; 2008-2012 concentricpuddle (concentricpuddle@gmail.com) <br />
Fork modernizado y mantenido por Washington Indacochea (<a href="mailto:linuxfrontier@proton.me">linuxfrontier@proton.me</a>), 2026. <br />
Licencia GPLv3 (<a href="www.gnu.org/licenses/gpl-3.0.html">www.gnu.org/licenses/gpl-3.0.html</a>).
""",
)

thanks = translate(
    "About",
    """<b>Washington Indacochea</b> (<a href="mailto:linuxfrontier@proton.me">linuxfrontier@proton.me</a>) por desarrollar y mantener este fork modernizado: la migración a PyQt6, la modernización completa del código a estándares 2026, el soporte de nuevos formatos de audio y el modo oscuro, entre otras mejoras.<br /><br />

<b>Evan Devetzis</b> por sus muchísimas ideas excelentes y por soportar más errores de los humanamente posible.<br /><br />

Ante todo, un gran agradecimiento a <b>Evan Devetzis</b> por trabajar incansablemente para ayudarme a mejorar puddletag aportando muchísimas ideas excelentes y por ser un gran cazador de errores.

Gracias a <b>Raphaël Rochet</b>, <b>Fabian Bakkum</b>, <b>Alan Gomes</b> y otros por contribuir traducciones.

A los autores de las bibliotecas de las que depende puddletag (sin ellas probablemente seguiría escribiendo un lector id3).<br /><br />

<b>Paul McGuire</b> por PyParsing.<br />
<b>Michael Urman</b> y <b>Joe Wreschnig</b> por Mutagen (es increíble).<br />
<b>Phil Thomson</b> y todos los responsables de PyQt (PyQt4 y PyQt6).<br />
<b>Michael Foord</b> y <b>Nicola Larosa</b> por ConfigObj (en serio, deberían reemplazar ConfigParser con esto).<br />
El <b>equipo Oxygen</b> por los iconos Oxygen.

""",
)


def versions():
    def get_module_version(module_name):
        try:
            from importlib.metadata import version

            return version(module_name)
        except ModuleNotFoundError:
            pass

        try:
            module = import_module(module_name)
            return getattr(module, "__version__", translate("About", "unknown version"))
        except ModuleNotFoundError:
            return translate("About", "not installed")

    return {
        "Python": python_version(),
        "PyQt": PYQT_VERSION_STR,
        "Qt": qVersion(),
        "Mutagen": mutagen.version_string,
        "PyParsing": get_module_version("pyparsing"),
        "ConfigObj": get_module_version("configobj"),
        "Unidecode": get_module_version("unidecode"),
        "lxml": get_module_version("lxml"),
        "pyacoustid": get_module_version("pyacoustid"),
        "Levenshtein": get_module_version("Levenshtein"),
    }


class ScrollLabel(QWidget):
    def __init__(self, text, alignment=Qt.AlignmentFlag.AlignCenter, parent=None):
        QWidget.__init__(self, parent)
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        label = QLabel(text)

        label.setTextFormat(Qt.TextFormat.RichText)
        label.setAlignment(alignment)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        sa = QScrollArea()
        sa.setWidget(label)
        sa.setWidgetResizable(True)
        vbox.addWidget(sa)
        self.label = label


class AboutPuddletag(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(translate("About", "About puddletag"))
        icon = QLabel()
        icon.setPixmap(QPixmap("icons:appicon.svg").scaled(48, 48))
        lib_versions = "<br />".join(
            f"{lib}: {version}" for lib, version in versions().items()
        )

        if changeset:
            version = translate("About", "<h2>puddletag {}</h2>Changeset {}").format(
                version_string, changeset
            )
        else:
            version = translate("About", "<h2>puddletag {}</h2>").format(version_string)
        label = QLabel(version)

        tab = QTabWidget()
        tab.addTab(ScrollLabel(desc), translate("About", "&About"))
        tab.addTab(
            ScrollLabel(thanks, Qt.AlignmentFlag.AlignLeft),
            translate("About", "&Thanks"),
        )
        tab.addTab(
            ScrollLabel(lib_versions, Qt.AlignmentFlag.AlignLeft),
            translate("About", "&Libraries"),
        )

        vbox = QVBoxLayout()
        version_layout = QHBoxLayout()
        version_layout.addWidget(icon)
        version_layout.addWidget(label, 1)
        vbox.addLayout(version_layout)
        vbox.addWidget(tab, 1)
        ok = OKCancel()
        ok.cancelButton.setVisible(False)
        vbox.addLayout(ok)
        ok.ok.connect(self.close)
        self.setLayout(vbox)


if __name__ == "__main__":
    app = QApplication([])
    win = AboutPuddletag()
    win.show()
    app.exec()
