# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Defines a Qt model that lists the video files in a category.
"""

import logging
import os.path  # To list files in the video directory.
import PySide6.QtCore  # To expose this table to QML.
import re  # For human sorting.
import typing


class VideoDirectory(PySide6.QtCore.QAbstractListModel):
	"""
	A list of the videos in a certain directory.

	This is a bit more specialised than a plain directory listing, with the following modifications
	reflecting the way in which I store my videos.
	* The three "films" directories are combined as if they are one.
	* The "Shorts" directory is combined into the "Series" directory.
	* File names are parsed if they end in (####)#. This is how I store the year and my rating. The
	year and rating are stored as extra roles.
	"""

	def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject]=None) -> None:
		"""
		Construct a new video directory table.
		:param parent: The parent element to this QML element, if any.
		"""
		super().__init__(parent)

		user_role = PySide6.QtCore.Qt.UserRole
		self.role_to_field = {
			user_role + 1: "path",
			user_role + 2: "title",
			user_role + 3: "type",
			user_role + 4: "year",
			user_role + 5: "rating",
		}

		self.videos: list[dict[str, typing.Any]] = []  # The actual data contained in this table.
		self._sort_by = "rating"

		self.base_directory = "/run/user/1000/gvfs/sftp:host=192.168.1.172,user=ruben/backup/backups/Filmdisk/"
		self._default_directory = "Films"
		self._directory = ""
		self.directory_set(self.base_directory + self._default_directory)

	def rowCount(self, parent: typing.Optional[PySide6.QtCore.QModelIndex]=PySide6.QtCore.QModelIndex()) -> int:
		"""
		Returns the number of video files and directories in this table.
		:param parent: The parent to display the child entries under. This is a plain table, so no parent should be
		provided.
		:return: The number of video files and directories.
		"""
		if parent.isValid():
			return 0
		return len(self.videos)

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
		value = self.videos[index.row()].get(field, "")
		return str(value)  # Just convert to string.


	def sort_directory(self, entries: list[dict[str, typing.Any]]) -> list[dict[str, typing.Any]]:
		"""
		Sort the entries in a directory.

		Subdirectories are put on top, supported files below. Both of these are then human-sorted.
		:param entries: The items in the directory. Provide full file paths, please!
		:return: Those same items, but reordered in correct sort order.
		"""
		convert_numbers = lambda text: float(text) if text.replace(".", "", 1).isdigit() else text.lower()
		def human_sort(metadata):
			if self._sort_by == "path":
				return [metadata["type"]] + [convert_numbers(t) for t in re.split(r"((?:[0-9]*[.])?[0-9]+)\d{1,2}", metadata["title"])]
			elif self._sort_by == "year":
				return [metadata["type"], -metadata.get("year", 0)] + [convert_numbers(t) for t in re.split(r"((?:[0-9]*[.])?[0-9]+)\d{1,2}", metadata["title"])]
			elif self._sort_by == "rating":
				return [metadata["type"], -metadata.get("rating", 0)] + [convert_numbers(t) for t in re.split(r"((?:[0-9]*[.])?[0-9]+)\d{1,2}", metadata["title"])]
			else:
				logging.error(f"Unknown sorting key {self._sort_by}")
				return []
		subfilms = sorted(entries, key=human_sort)
		return list(subfilms)

	def directory_set(self, new_directory: str) -> None:
		"""
		Change the current directory that this model is looking at.
		:param new_directory: A path to a directory to look at.
		"""
		if new_directory == self._directory:  # Didn't actually change.
			return

		# Under water, we'll combine a few directories as if they are one.
		if new_directory in [os.path.join(self.base_directory, sub) for sub in ["Films", "Films (1 - 5)", "Films (6 - 7)", "Films (8 - 10)"]]:
			directories = [os.path.join(self.base_directory, subdir) for subdir in ["Films (1 - 5)", "Films (6 - 7)", "Films (8 - 10)"]]
		elif new_directory in [os.path.join(self.base_directory, sub) for sub in ["Series", "Shorts"]]:
			directories = [os.path.join(self.base_directory, subdir) for subdir in ["Series", "Shorts"]]
		else:
			directories = [new_directory]

		entries = []
		for directory in directories:
			entries.extend([os.path.join(directory, f) for f in os.listdir(directory)])
		metadata = []
		for entry in entries:
			entry_dict = {"path": entry}
			if os.path.isdir(entry):
				entry_dict["type"] = "directory"
			elif os.path.splitext(entry)[1] in [".mkv", ".mp4", ".avi", ".m2ts", ".divx", ".webm", ".wmv"]:
				entry_dict["type"] = "film"
			else:
				continue  # Unsupported / unknown file type.
			find_title = re.search(r"(.+)\(\d+(?: - \d+)?\)\d{1,2}", os.path.basename(entry))
			if find_title is not None:
				entry_dict["title"] = os.path.basename(find_title.group(1))
			else:
				entry_dict["title"] = os.path.splitext(os.path.basename(entry))[0]
			find_year = re.search(r"\((\d+)(?: - \d+)?\)", os.path.basename(entry))
			if find_year is not None:
				entry_dict["year"] = int(find_year.group(1))
			find_rating = re.search(r"\(\d+(?: - \d+)?\)(\d{1,2})", os.path.basename(entry))
			if find_rating is not None:
				entry_dict["rating"] = int(find_rating.group(1))
			metadata.append(entry_dict)
		if new_directory != self.default_directory:
			parent_path_entry = [{
				"type": "directory",
				"path": os.path.abspath(os.path.join(new_directory, "..")),
				"title": "..",
			}]
		else:
			parent_path_entry = []
		entries = parent_path_entry + self.sort_directory(metadata)

		# Remove all old data from the list. We're assuming that since the directory changed, all files will be different.
		self.beginRemoveRows(PySide6.QtCore.QModelIndex(), 0, len(self.videos) - 1)
		self.videos.clear()
		self.endRemoveRows()
		# Add the new data.
		self.beginInsertRows(PySide6.QtCore.QModelIndex(), 0, len(entries))
		self.videos.extend(entries)
		self.endInsertRows()

		self._directory = new_directory

	@PySide6.QtCore.Property(str, fset=directory_set)
	def directory(self) -> str:
		"""
		The current directory that this model is looking at.
		:return: The current directory that this model is looking at.
		"""
		return self._directory

	def default_directory_set(self, new_default_directory: str) -> None:
		"""
		Change the default directory of the model.

		The default directory is the root of the directory structure that the model can navigate
		through. Since our directory structure for videos is by category, this essentially denotes
		which category of videos this model will show.
		:param new_default_directory: The new value of the default directory.
		"""
		if self._default_directory == new_default_directory:
			return  # Nothing changed.
		self._default_directory = new_default_directory
		self.directory_set(self.base_directory + new_default_directory)

	@PySide6.QtCore.Property(str, fset=default_directory_set)
	def default_directory(self) -> str:
		"""
		The current default directory of this model.

		The default directory is the root of the directory structure that the model can navigate
		through. Since our directory structure for videos is by category, this essentially denotes
		which category of videos this model will show.
		:return: The current default directory of this model.
		"""
		return self._default_directory