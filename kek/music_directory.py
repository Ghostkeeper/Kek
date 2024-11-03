# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Defines a Qt model that lists the music files in a directory.
"""

import logging
import math  # To format track duration.
import mutagen  # To read metadata from music files.
import os.path  # To list files in the music directory.
import PySide6.QtCore  # To expose this table to QML.
import typing

class MusicDirectory(PySide6.QtCore.QAbstractTableModel):
	"""
	A list of the tracks contained within a certain directory, and their metadata.
	"""

	def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject]=None) -> None:
		"""
		Construct a new music directory table.
		:param parent: The parent element to this QML element, if any.
		"""
		super().__init__(parent)

		self.column_fields = ["type", "title", "duration"]
		self.music: list[dict[str, typing.Any]] = []  # The actual data contained in this table.

		music_locations = PySide6.QtCore.QStandardPaths.standardLocations(PySide6.QtCore.QStandardPaths.StandardLocation.MusicLocation)
		if music_locations:
			directory = music_locations[0]
		else:
			directory = os.path.expanduser("~/Music")
		self._directory = ""
		self.directory_set(directory)


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
		Returns the number of metadata entries we're displaying in the table.
		:param parent: The parent to display the child entries under. This is a plain table, so no parent should be
		provided.
		:return: The number of metadata entries we're displaying in the table.
		"""
		if parent.isValid():
			return 0
		return len(self.column_fields)

	def data(self, index: PySide6.QtCore.QModelIndex, role: int=PySide6.QtCore.Qt.DisplayRole) -> typing.Any:
		"""
		Returns one cell of the table.
		:param index: The row and column index of the cell to give the data from.
		:param role: Which data to return for this cell. Defaults to the data displayed, which is the only data we
		store for a cell.
		:return: The data contained in that cell, as a string.
		"""
		if not index.isValid():
			return None  # Only valid indices return data.
		if role != PySide6.QtCore.Qt.DisplayRole:
			return None  # Only return for the display role.
		field = self.column_fields[index.column()]
		value = self.music[index.row()][field]
		if field == "duration":
			if value < 0:
				return ""
			seconds = round(value)
			return str(math.floor(seconds / 60)) + ":" + ("0" if (seconds % 60 < 10) else "") + str(seconds % 60)
		return str(value)  # Default, just convert to string.

	def flags(self, index: PySide6.QtCore.QModelIndex) -> int:
		"""
		Returns metadata properties of a cell.
		:param index: The cell to get metadata of.
		:return: The metadata flags for that cell.
		"""
		return PySide6.QtCore.Qt.ItemFlag.ItemIsEnabled

	@PySide6.QtCore.Slot(int, int, int, result=str)
	def headerData(self, section: int, orientation: int, role: int=PySide6.QtCore.Qt.DisplayRole) -> typing.Optional[str]:
		"""
		Returns the row or column labels for the table.

		This table doesn't really use any row labels. We'll return the row index, but it shouldn't get displayed.
		:param section: The row or column index.
		:param orientation: Whether to get the row labels or the column labels.
		:param role: Which data to return for the headers. Defaults to the data displayed, which is the only data we
		can return.
		:return: The header for the row or column, as a string.
		"""
		if role != PySide6.QtCore.Qt.DisplayRole:
			return None
		if orientation == 1:  # PySide6.QtCore.Qt.Orientation.Horizontal is an enum, but the QML doesn't give us that.
			return self.column_fields[section]
		elif orientation == 2:
			return self.music[section]["name"]
		else:
			return None

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

		new_music = []
		for filename in os.listdir(new_directory):
			filepath = os.path.join(new_directory, filename)
			logging.debug(f"Listing directory entry: {filepath}")
			if os.path.isdir(filepath):
				duration = -1
				filetype = "directory"
			else:
				try:
					duration = mutagen.File(filepath).info.length
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
				"name": filename,
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
