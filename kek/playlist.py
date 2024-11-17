# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Defines a Qt model that lists the music files currently in the playlist for playing.
"""

import logging
import math  # To calculate durations of tracks.
import os.path  # For adding directories to the playlist.
import PySide6.QtCore  # This defines a Qt list model.
import typing

import kek.music_directory  # To add directories of music to the playlist.
import kek.music_metadata  # To get metadata of music to add.


class Playlist(PySide6.QtCore.QAbstractListModel):
	"""
	A list of the tracks currently in the playlist.
	"""

	instance: typing.Optional["Playlist"] = None
	"""
	This class is a singleton. This stores the one instance that is allowed to exist.
	"""

	@classmethod
	def get_instance(cls) -> "Playlist":
		"""
		Gets the singleton instance. If no instance was made yet, it will be instantiated here.
		:return: The single instance of this class.
		"""
		if cls.instance is None:
			cls.instance = Playlist()
		return cls.instance

	def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject] = None) -> None:
		"""
		Construct a new playlist model.
		:param parent: The parent element to this QML element, if any.
		"""
		super().__init__(parent)

		user_role = PySide6.QtCore.Qt.UserRole
		self.role_to_field = {
			user_role + 1: "path",
			user_role + 2: "title",
			user_role + 3: "artist",
			user_role + 4: "album",
			user_role + 5: "duration",
			user_role + 6: "cover",
		}

		self.music: list[dict[str, typing.Any]] = []  # The actual playlist, in order.

	def rowCount(self, parent: typing.Optional[PySide6.QtCore.QModelIndex]=PySide6.QtCore.QModelIndex()) -> int:
		"""
		Returns the number of music files in the playlist.
		:param parent: The parent element to display the child entries under. This is a plain list, so no parent should
		be provided.
		:return: The number of tracks in the playlist.
		"""
		if parent.isValid():
			return 0
		return len(self.music)

	def columnCount(self, parent: typing.Optional[PySide6.QtCore.QModelIndex]=PySide6.QtCore.QModelIndex()) -> int:
		"""
		Returns the number of columns in the playlist.

		Since this is a regular list, there is just one column.
		:param parent: The parent element to display the child entries under. This is a plain list, so no parent should
		be provided.
		:return: The number of columns in the playlist.
		"""
		if parent.isValid():
			return 0
		return 1

	def roleNames(self) -> dict[int, bytes]:
		"""
		Gets the names of the roles as exposed to QML.

		This function is called internally by Qt to match a model field in the QML code with the roles in this model.
		:return: A mapping of roles to filed names. The field names are bytes.
		"""
		return {role: field.encode("utf-8") for role, field in self.role_to_field.items()}

	def data(self, index: PySide6.QtCore.QModelIndex, role: int=PySide6.QtCore.Qt.DisplayRole) -> typing.Any:
		"""
		Returns one field of the data in the list.
		:param index: The row and column index of the cell to give the data from.
		:param role: Which data to return for this cell. Defaults to the data displayed, which is the only data we
		store for a cell.
		:return: The data contained in that cell, as a string.
		"""
		if not index.isValid():
			return None  # Only valid indices return data.
		if role not in self.role_to_field:
			return None
		field = self.role_to_field[role]
		value = self.music[index.row()][field]
		if field == "duration":
			if value < 0:
				return ""
			seconds = round(value)
			return str(math.floor(seconds / 60)) + ":" + ("0" if (seconds % 60 < 10) else "") + str(seconds % 60)
		return str(value)  # Default, just convert to string.

	@PySide6.QtCore.Slot(str, int)
	def add(self, path: str, index: int) -> None:
		"""
		Add a certain file or directory to the playlist.

		When adding a directory, all music files in the directory will be added, and all subdirectories will also be
		added recursively. When adding a playlist file (m3u), all tracks in the playlist will be added. But when adding
		a directory, playlist files in the directory will get ignored, because that would tend to add the same music
		files twice.
		:param path: The path to the file or directory to add to the playlist.
		:param index: The place in the playlist to insert the track(s). Index 0 means that it gets added to the very
		start of the playlist, and index len(self.music) means that it will get added to the end.
		"""
		if os.path.isdir(path):
			entries = os.listdir(path)
			entries = kek.music_directory.sort_directory(entries)
			for entry in entries:
				self.add(entry, index)
				index += 1
		else:
			extension = os.path.splitext(path)[-1]
			if extension not in kek.music_directory.supported_extensions:
				return
			meta = kek.music_metadata.metadata[path]

			self.beginInsertRows(PySide6.QtCore.QModelIndex(), index, index + 1)
			self.music.insert(index, meta)
			self.endInsertRows()
			self.dataChanged.emit(self.createIndex(index, 0), self.createIndex(index + 1, 0))
			logging.info(f"Added {path} to the playlist.")

instance = Playlist()
