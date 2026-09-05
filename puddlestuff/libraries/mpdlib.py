from collections import defaultdict

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget

from ..musiclib import MusicLibError
from ..util import translate

name = "MPD"
description = "Music Player Daemon Database"
author = "concentricpuddle"


class MPDLibrary:
    def __init__(self, host, port, password=None):
        self.host = host
        self.port = port
        self.password = password
        self.tracks = []
        self.albums = defaultdict(dict)
        self.client = None

    def connect(self):
        try:
            import mpd

            self.client = mpd.MPDClient()
            self.client.connect(self.host, self.port)
            if self.password:
                self.client.password(self.password)
        except ImportError:
            raise MusicLibError(0, translate("MPD", "python-mpd2 module not found."))
        except OSError as e:
            raise MusicLibError(0, str(e))

    def load(self):
        if not self.client:
            self.connect()

        try:
            # Fetch all songs
            songs = self.client.listallinfo()

            for song in songs:
                if "file" not in song:
                    continue

                # Convert MPD song to puddletag format
                tag = {
                    "artist": song.get("artist", [""])[0]
                    if isinstance(song.get("artist"), list)
                    else song.get("artist", ""),
                    "album": song.get("album", [""])[0]
                    if isinstance(song.get("album"), list)
                    else song.get("album", ""),
                    "title": song.get("title", [""])[0]
                    if isinstance(song.get("title"), list)
                    else song.get("title", ""),
                    "track": song.get("track", [""])[0]
                    if isinstance(song.get("track"), list)
                    else song.get("track", ""),
                    "genre": song.get("genre", [""])[0]
                    if isinstance(song.get("genre"), list)
                    else song.get("genre", ""),
                    "path": song["file"],
                }

                # Check if path is absolute or relative to MPD music dir
                # (This is a simplified version, real MPD integration would need music_directory)

                artist = tag["artist"]
                album = tag["album"]

                if album not in self.albums[artist]:
                    self.albums[artist][album] = len(self.tracks)
                    self.tracks.append([tag])
                else:
                    self.tracks[self.albums[artist][album]].append(tag)

            return self.albums, self.tracks
        except Exception as e:  # noqa: BLE001
            raise MusicLibError(0, str(e))
        finally:
            if self.client:
                self.client.disconnect()


class InitWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)

        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel(translate("MPD", "Host:")))
        self.host_edit = QLineEdit("localhost")
        host_layout.addWidget(self.host_edit)
        layout.addLayout(host_layout)

        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel(translate("MPD", "Port:")))
        self.port_edit = QLineEdit("6600")
        port_layout.addWidget(self.port_edit)
        layout.addLayout(port_layout)

        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel(translate("MPD", "Password:")))
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        pass_layout.addWidget(self.pass_edit)
        layout.addLayout(pass_layout)

        layout.addStretch()

    def library(self):
        host = self.host_edit.text()
        try:
            port = int(self.port_edit.text())
        except ValueError:
            port = 6600
        password = self.pass_edit.text() or None

        lib = MPDLibrary(host, port, password)
        return lib.load()
