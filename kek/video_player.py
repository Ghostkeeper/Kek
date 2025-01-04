# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Keeps track and controls the currently playing video.
"""

import logging
import PySide6.QtCore  # For exposing these controls to QML.
import typing
import vlc  # To play video files.

class VideoPlayer(PySide6.QtCore.QObject):
	"""
	Keeps track and controls the currently playing video.

	This is a singleton class in order to expose the state to QML.
	"""

	instance: typing.Optional["VideoPlayer"] = None
	"""
	This class is a singleton. This stores the one instance that is allowed to exist.
	"""

	@classmethod
	def get_instance(cls) -> "VideoPlayer":
		"""
		Gets the singleton instance. If no instance was made yet, it will be instantiated here.
		:return: The single instance of this class.
		"""
		if cls.instance is None:
			cls.instance = VideoPlayer()
		return cls.instance

	def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject]=None):
		"""
		Construct the video player instance.
		:param parent: The parent object of this QObject, if any.
		"""
		super().__init__(parent)
		self.vlc = None  # If any video is playing, a VLC instance that is playing it.
		self.is_paused = False  # Whether the video is paused (if playing).

	is_playing_changed = PySide6.QtCore.Signal()

	@PySide6.QtCore.Property(bool, notify=is_playing_changed)
	def is_playing(self) -> bool:
		"""
		Get whether any video is currently playing, or should be playing.

		If the video is paused, it is considered to be playing too. Only when it is stopped is it considered to not be
		playing.
		:return: ``True`` if the video is currently playing, or ``False`` if it is stopped.
		"""
		return self.vlc is not None

	@PySide6.QtCore.Slot(str)
	def play(self, path: str) -> None:
		"""
		Start playing a certain video.
		:param path: The path to the video to play.
		"""
		self.vlc = vlc.MediaPlayer("file://" + path)
		self.vlc.play()
		self.is_playing_changed.emit()

	is_paused_changed = PySide6.QtCore.Signal()

	def is_paused_set(self, new_is_paused: bool) -> None:
		"""
		Pause or continue the video.
		:param new_is_paused: Whether the music should be paused or running.
		"""
		if self.is_paused == new_is_paused:
			return
		logging.info(f"Toggling pause to: {new_is_paused}")
		# TODO: toggle pause
		self.is_paused_changed.emit()