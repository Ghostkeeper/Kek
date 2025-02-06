# Desktop environment for a domotics hub.
# Copyright (C) 2025 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Defines a Qt object that controls the display of the map.
"""

import PySide6.QtCore  # For exposing these controls to QML.
import subprocess  # To start Firefox showing the map.
import typing

class Map(PySide6.QtCore.QObject):
	"""
	Controls the display of the map.

	This is a singleton class in order to expose the state and the slots to QML.
	"""

	instance: typing.Optional["Map"] = None
	"""
	This class is a singleton. This stores the one instance that is allowed to exist.
	"""

	@classmethod
	def get_instance(cls) -> "Map":
		"""
		Gets the singleton instance. If no instance was made yet, it will be instantiated here.
		:return: The single instance of this class.
		"""
		if cls.instance is None:
			cls.instance = Map()
		return cls.instance

	@PySide6.QtCore.Slot()
	def show(self) -> None:
		"""
		Show the map.
		"""
		subprocess.run(["firefox", "--kiosk", "https://www.openstreetmap.org/#map=14/52.08552/5.09452"])