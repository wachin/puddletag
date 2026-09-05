import traceback

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from . import findfunc
from .puddleobjects import PuddleConfig
from .translations import translate


class ExportDialog(QDialog):
    def __init__(self, parent=None, tracks=None):
        super().__init__(parent)
        self.tracks = tracks
        self.setWindowTitle(translate("Export", "Export Tags"))
        self.setMinimumSize(600, 400)

        self.cparser = PuddleConfig()

        layout = QVBoxLayout(self)

        # Template selection
        tpl_layout = QHBoxLayout()
        tpl_layout.addWidget(QLabel(translate("Export", "Template:")))
        self.tpl_combo = QComboBox()
        self.tpl_combo.addItems(["CSV", "HTML", "RTF", "Custom"])

        # Load custom templates from config
        self.custom_templates = self.cparser.get("export", "custom_templates", {})
        for name in self.custom_templates:
            if name not in ["CSV", "HTML", "RTF", "Custom"]:
                self.tpl_combo.addItem(name)

        self.tpl_combo.currentIndexChanged.connect(self.template_changed)
        tpl_layout.addWidget(self.tpl_combo)

        self.save_tpl_btn = QPushButton(translate("Export", "&Save Template"))
        self.save_tpl_btn.clicked.connect(self.save_template)
        tpl_layout.addWidget(self.save_tpl_btn)

        layout.addLayout(tpl_layout)

        # Template editor
        layout.addWidget(QLabel(translate("Export", "Template Editor:")))
        self.tpl_edit = QTextEdit()
        layout.addWidget(self.tpl_edit)

        # Buttons
        btn_layout = QHBoxLayout()
        self.export_btn = QPushButton(translate("Export", "&Export"))
        self.export_btn.clicked.connect(self.perform_export)
        self.cancel_btn = QPushButton(translate("Defaults", "&Cancel"))
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.templates = {
            "CSV": "%artist%;%album%;%title%;%track%;%year%;%genre%",
            "HTML": """<html>
<head><title>Export</title></head>
<body>
<table border="1">
  <tr>
    <th>Artist</th>
    <th>Album</th>
    <th>Title</th>
  </tr>
$loop(%artist%)  <tr>
    <td>%artist%</td>
    <td>%album%</td>
    <td>%title%</td>
  </tr>
$loopend()</table>
</body>
</html>""",
            "RTF": "Artist: %artist%\\line Album: %album%\\line Title: %title%\\line\\line",
            "Custom": "",
        }
        self.templates.update(self.custom_templates)

        self.template_changed(0)

    def template_changed(self, index):
        name = self.tpl_combo.currentText()
        self.tpl_edit.setPlainText(self.templates.get(name, ""))

    def save_template(self):
        from PyQt6.QtWidgets import QInputDialog

        name, ok = QInputDialog.getText(
            self,
            translate("Export", "Save Template"),
            translate("Export", "Template Name:"),
        )
        if ok and name:
            template = self.tpl_edit.toPlainText()
            self.templates[name] = template
            self.custom_templates[name] = template
            self.cparser.set("export", "custom_templates", self.custom_templates)
            if self.tpl_combo.findText(name) == -1:
                self.tpl_combo.addItem(name)
            self.tpl_combo.setCurrentText(name)

    def perform_export(self):
        if not self.tracks:
            QMessageBox.warning(
                self, "puddletag", translate("Export", "No tracks selected for export.")
            )
            return

        file_filter = "All Files (*)"
        name = self.tpl_combo.currentText()
        if name == "CSV":
            file_filter = "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)"
        elif name == "HTML":
            file_filter = "HTML Files (*.html *.htm);;All Files (*)"

        filename, _ = QFileDialog.getSaveFileName(
            self, translate("Export", "Save Export As..."), "", file_filter
        )
        if not filename:
            return

        template = self.tpl_edit.toPlainText()
        try:
            result = self.process_template(template, self.tracks)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result)
            QMessageBox.information(
                self, "puddletag", translate("Export", "Export completed successfully.")
            )
            self.accept()
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "puddletag",
                translate("Export", "Error during export: {}").format(str(e)),
            )

    def process_template(self, template, tracks):
        # Very basic loop support: $loop(sort_field) ... $loopend()
        loop_match = re.search(
            r"\$loop\((.*?)\)(.*?)\$loopend\(\)", template, re.DOTALL
        )
        if loop_match:
            sort_field = loop_match.group(1).strip("%")
            loop_body = loop_match.group(2)

            # Sort tracks if needed
            sorted_tracks = sorted(tracks, key=lambda t: t.get(sort_field, ""))

            loop_result = ""
            for track in sorted_tracks:
                loop_result += findfunc.parsefunc(loop_body, track)

            return (
                template[: loop_match.start()]
                + loop_result
                + template[loop_match.end() :]
            )
        else:
            # No loop, just process for each track (like CSV)
            result = ""
            for track in tracks:
                result += findfunc.parsefunc(template, track) + "\n"
            return result


import re
