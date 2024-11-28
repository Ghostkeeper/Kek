# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Keeps track and controls the currently playing music.
"""

import logging
import PySide6.QtCore  # For exposing these controls to QML.
import time  # Tracking the time played.
import typing

import kek.music_playback  # To actually play the music.
import kek.playlist  # To find which songs we have to be playing.
import kek.sound  # To store the audio we're playing.

class MusicPlayer(PySide6.QtCore.QObject):
	"""
	Keeps track and controls the currently playing music.

	This is a singleton class in order to expose the state to QML.
	"""

	instance: typing.Optional["MusicPlayer"] = None
	"""
	This class is a singleton. This stores the one instance that is allowed to exist.
	"""

	@classmethod
	def get_instance(cls) -> "MusicPlayer":
		"""
		Gets the singleton instance. If no instance was made yet, it will be instantiated here.
		:return: The single instance of this class.
		"""
		if cls.instance is None:
			cls.instance = MusicPlayer()
		return cls.instance

	def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject]=None):
		"""
		Construct the music player instance.
		"""
		super().__init__(parent)
		self.current_track = 0  # The index in the playlist that we're currently playing.
		self.start_time = None  # The start time (float) if any track is playing, or None if not.
		self.current_sound = None  # If playing, the decoded wave data (Sound object).

	is_playing_changed = PySide6.QtCore.Signal()

	def is_playing_set(self, new_is_playing: bool) -> None:
		"""
		Start or stop the music.
		:param new_is_playing: Whether the music should be playing or not.
		"""
		if self.current_sound is None and new_is_playing:
			self.play_next()
		elif self.current_sound is not None and not new_is_playing:
			logging.info("Stopping playback.")
			kek.music_playback.stop()
			self.current_sound = None
			self.start_time = None
			self.is_playing_changed.emit()

	@PySide6.QtCore.Property(bool, fset=is_playing_set, notify=is_playing_changed)
	def is_playing(self) -> bool:
		"""
		Get whether any music is currently playing, or should be playing.

		If the music is paused, it is considered to be playing too. Only when it is stopped is it considered to not be
		playing.
		:return: ``True`` if the music is currently playing, or ``False`` if it is stopped.
		"""
		return self.start_time is not None

	def play_next(self) -> None:
		"""
		Play the next song in the playlist.
		"""
		current_playlist = kek.playlist.Playlist.get_instance().music
		if len(current_playlist) == 0:  # Nothing in the playlist.
			self.is_playing_set(False)
			return

		next_song = current_playlist[self.current_track]
		logging.info(f"Starting playback of track: {next_song['path']}")
		self.current_sound = kek.sound.Sound.decode(next_song["path"])
		self.start_time = time.time()
		kek.music_playback.play(self.current_sound)


instance = MusicPlayer()