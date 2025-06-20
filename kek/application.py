# Desktop environment for a domotics hub.
# Copyright (C) 2025 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
A module that provides the application class, which is a QtApplication object.
"""

import logging
import os.path  # To call on Git to update the source code automatically.
import PySide6.QtCore  # To remove the cursor.
import PySide6.QtGui  # To remove the cursor.
import PySide6.QtQml  # To register types with the QML engine, and create the engine.
import PySide6.QtWidgets  # This is an application.
import subprocess  # To call on Git to update the source code automatically.
import typing

import kek.map  # Registering map Qt objects.
import kek.music_directory  # Registering music Qt objects.
import kek.music_player  # Registering music Qt objects.
import kek.playlist  # Registering music Qt objects.
import kek.video_directory  # Registering video Qt objects.
import kek.video_player  # Registering video Qt objects.


instance = None


class Application(PySide6.QtWidgets.QApplication):
	"""
	The Qt application that runs the whole thing.

	This provides a QML engine and keeps it running until the application quits.
	"""

	version = "1.0.0"
	"""
	The current application version.
	"""

	def __init__(self, argv: typing.List[str]) -> None:
		"""
		Begins the start-up process.
		:param argv: Command-line parameters provided to the application. Qt understands some of these.
		"""
		global instance
		instance = self
		logging.info(f"Starting application version {Application.version}.")
		super().__init__(argv)

		self.setApplicationName("Kek")
		self.setApplicationDisplayName("Kek")
		self.setApplicationVersion(Application.version)
		self.setOrganizationName("Ghostkeeper")

		logging.debug("Registering QML types.")
		PySide6.QtQml.qmlRegisterSingletonInstance(Application, "Kek", 1, 0, "Application", self)
		PySide6.QtQml.qmlRegisterSingletonInstance(kek.map.Map, "Kek", 1, 0, "Map", kek.map.Map.get_instance())
		PySide6.QtQml.qmlRegisterSingletonInstance(kek.music_player.MusicPlayer, "Kek", 1, 0, "MusicPlayer", kek.music_player.MusicPlayer.get_instance())
		PySide6.QtQml.qmlRegisterSingletonInstance(kek.playlist.Playlist, "Kek", 1, 0, "Playlist", kek.playlist.Playlist.get_instance())
		PySide6.QtQml.qmlRegisterType(kek.music_directory.MusicDirectory, "Kek", 1, 0, "MusicDirectory")
		PySide6.QtQml.qmlRegisterSingletonInstance(kek.video_player.VideoPlayer, "Kek", 1, 0, "VideoPlayer", kek.video_player.VideoPlayer.get_instance())
		PySide6.QtQml.qmlRegisterType(kek.video_directory.VideoDirectory, "Kek", 1, 0, "VideoDirectory")

		logging.debug("Loading QML engine.")
		self.engine = PySide6.QtQml.QQmlApplicationEngine()
		self.engine.quit.connect(self.quit)
		logging.debug("Creating main window.")
		self.engine.load("gui/MainWindow.qml")
		self.setOverrideCursor(PySide6.QtGui.QCursor(PySide6.QtCore.Qt.BlankCursor))

		logging.info("Start-up complete.")

		# Update my own source code.
		source_directory = os.path.dirname(__file__)
		os.chdir(source_directory)
		subprocess.Popen(["git", "pull"])