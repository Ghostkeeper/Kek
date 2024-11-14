# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Defines a Qt model that lists the music files in a directory.
"""

import itertools  # To sort directories.
import logging
import math  # To format track duration.
import mutagen  # To read metadata from music files.
import os.path  # To list files in the music directory.
import PySide6.QtCore  # To expose this table to QML.
import re  # To implement human sorting.
import typing

import kek.music_metadata  # To get the duration of files quickly.


class MusicDirectory(PySide6.QtCore.QAbstractListModel):
	"""
	A list of the tracks contained within a certain directory, and their metadata.
	"""

	def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject]=None) -> None:
		"""
		Construct a new music directory table.
		:param parent: The parent element to this QML element, if any.
		"""
		super().__init__(parent)

		kek.music_metadata.load()

		user_role = PySide6.QtCore.Qt.UserRole
		self.role_to_field = {
			user_role + 1: "path",
			user_role + 2: "type",
			user_role + 3: "name",
			user_role + 4: "duration",
		}

		self.music: list[dict[str, typing.Any]] = []  # The actual data contained in this table.

		music_locations = PySide6.QtCore.QStandardPaths.standardLocations(PySide6.QtCore.QStandardPaths.StandardLocation.MusicLocation)
		if music_locations:
			self.default_directory = music_locations[0]
		else:
			self.default_directory = os.path.expanduser("~/Music")
		self._directory = ""
		self.directory_set(self.default_directory)


	def rowCount(self, parent: typing.Optional[PySide6.QtCore.QModelIndex]=PySide6.QtCore.QModelIndex()) -> int:
		"""
		Returns the number of music files and directories in this table.
		:param parent: The parent to display the child entries under. This is a plain table, so no parent should be
		provided.
		:return: The number of music files and directories.
		"""
		if parent.isValid():
			return 0
		return len(self.music)

	def columnCount(self, parent: typing.Optional[PySide6.QtCore.QModelIndex]=PySide6.QtCore.QModelIndex()) -> int:
		"""
		Returns the number of columns in this list, which is always 1.
		:param parent: The parent to display the child entries under. This is a plain table, so no parent should be
		provided.
		:return: The number of metadata entries we're displaying in the table.
		"""
		if parent.isValid():
			return 0
		return 1

	def roleNames(self) -> dict[int, bytes]:
		"""
		Gets the names of the roles as exposed to QML.

		This function is called internally by Qt to match a model field in the QML code with the roles in this model.
		:return: A mapping of roles to field names. The field names are bytes.
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

	def sort_directory(self, entries: list[str]) -> list[str]:
		"""
		Sort the entries in a directory.

		Subdirectories are put on top, supported files below. Both of these are then human-sorted.
		:param entries: The items in the directory. Provide full file paths, please!
		:return: Those same items, but reordered in correct sort order.
		"""
		subdirectories = filter(os.path.isdir, entries)
		subfiles = filter(os.path.isfile, entries)
		supported_extensions = [".mp3", ".flac", ".ogg", ".opus"]
		submusic = filter(lambda x: os.path.splitext(x)[1] in supported_extensions, subfiles)

		convert_numbers = lambda text: float(text) if text.replace(".", "", 1).isdigit() else text.lower()
		human_sort = lambda key: [convert_numbers(t) for t in re.split(r"((?:[0-9]*[.])?[0-9]+)", key)]
		subdirectories = sorted(subdirectories, key=human_sort)
		submusic = sorted(submusic, key=human_sort)
		return [".."] + list(itertools.chain(subdirectories, submusic))

	def directory_set(self, new_directory: str) -> None:
		"""
		Change the current directory that this model is looking at.
		:param new_directory: A path to a directory to look at.
		"""
		if new_directory == self._directory:  # Didn't actually change.
			return
		if not os.path.exists(new_directory):  # How could it ever be set to a non-existing directory? Oh well.
			logging.warning(f"Trying to set music directory to non-existent path: {new_directory}")
			return

		kek.music_metadata.add_directory(new_directory)

		entries = [os.path.join(new_directory, f) for f in os.listdir(new_directory)]
		entries = self.sort_directory(entries)
		new_music = []
		for filepath in entries:
			logging.debug(f"Listing directory entry: {filepath}")
			if filepath == "..":
				if new_directory != self.default_directory:  # Don't allow going above the default directory.
					new_music.append({
						"type": "directory",
						"path": os.path.abspath(os.path.join(new_directory, "..")),
						"name": "..",
						"duration": -1,
					})
				continue
			if os.path.isdir(filepath):
				duration = -1
				filetype = "directory"
			else:
				try:
					duration = kek.music_metadata.metadata.get(filepath)["duration"]
				except mutagen.MutagenError as e:
					logging.error(f"Unable to get metadata from {filepath}: {e}")
					duration = -1
				extension = os.path.splitext(filepath)[1]
				if extension in [".flac", ".wav"]:
					filetype = "uncompressed"
				else:
					filetype = "compressed"
			new_music.append({
				"type": filetype,
				"path": filepath,
				"name": os.path.basename(filepath),
				"duration": duration,
			})

		# Remove all old data from the table. We're assuming that since the directory changed, all files will be different.
		self.beginRemoveRows(PySide6.QtCore.QModelIndex(), 0, len(self.music) - 1)
		self.music.clear()
		self.endRemoveRows()
		# Add the new data.
		self.beginInsertRows(PySide6.QtCore.QModelIndex(), 0, len(new_music))
		self.music.extend(new_music)
		self.endInsertRows()

		self._directory = new_directory

	@PySide6.QtCore.Property(str, fset=directory_set)
	def directory(self) -> str:
		"""
		The current directory that this model is looking at.
		:return: The current directory that this model is looking at.
		"""
		return self._directory
