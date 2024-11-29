# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Keeps track and controls the currently playing music.
"""

import logging
import math  # For correctly formatting the duration of the track.
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

	current_track_changed = PySide6.QtCore.Signal()

	is_playing_changed = PySide6.QtCore.Signal()

	def is_playing_set(self, new_is_playing: bool) -> None:
		"""
		Start or stop the music.
		:param new_is_playing: Whether the music should be playing or not.
		"""
		if self.current_sound is None and new_is_playing:
			self.play()
		elif self.current_sound is not None and not new_is_playing:
			self.stop()

	@PySide6.QtCore.Property(bool, fset=is_playing_set, notify=is_playing_changed)
	def is_playing(self) -> bool:
		"""
		Get whether any music is currently playing, or should be playing.

		If the music is paused, it is considered to be playing too. Only when it is stopped is it considered to not be
		playing.
		:return: ``True`` if the music is currently playing, or ``False`` if it is stopped.
		"""
		return self.current_sound is not None

	is_paused_changed = PySide6.QtCore.Signal()

	def is_paused_set(self, new_is_paused: bool) -> None:
		"""
		Pause or resume the music.
		:param new_is_paused: Whether the music should be paused or running.
		"""
		if kek.music_playback.is_paused == new_is_paused:
			return
		logging.info(f"Toggling pause to: {new_is_paused}")
		kek.music_playback.toggle_pause()
		self.is_paused_changed.emit()

	@PySide6.QtCore.Property(bool, fset=is_paused_set, notify=is_paused_changed)
	def is_paused(self) -> bool:
		"""
		Get whether the music playback is paused.

		If the music is stopped, it cannot be paused as well.
		:return: ``True`` is the music is currently paused, or ``False`` if it is playing or stopped.
		"""
		return kek.music_playback.is_paused

	def play(self) -> None:
		"""
		Play the current song.
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
		self.is_playing_changed.emit()

	def stop(self) -> None:
		"""
		Stop playing any music.
		"""
		logging.info("Stopping playback.")
		kek.music_playback.stop()
		self.current_sound = None
		self.start_time = None
		self.is_playing_changed.emit()

	def current_track_nr_set(self, new_current_track: int) -> None:
		"""
		Changes the current track.

		This doesn't automatically start playing the newly selected track.
		:param new_current_track: The track to select.
		"""
		self.stop()
		self.current_track = new_current_track
		self.current_track_changed.emit()
		self.play()

	@PySide6.QtCore.Property(int, fset=current_track_nr_set, notify=current_track_changed)
	def current_track_nr(self) -> int:
		"""
		Returns the current track index in the playlist.
		:return: The index in the playlist that is being played, or would be played if we press play.
		"""
		return self.current_track

	@PySide6.QtCore.Property(str, notify=current_track_changed)
	def current_cover(self) -> str:
		"""
		Gives the path to the cover image of the currently playing song.

		If no song is currently playing, gives an empty string.
		:return: A path to an image file.
		"""
		current_playlist = kek.playlist.Playlist.get_instance().music
		if self.current_track < 0 or self.current_track >= len(current_playlist):
			return ""
		return current_playlist[self.current_track]["cover"]

	@PySide6.QtCore.Property(str, notify=current_track_changed)
	def current_duration(self) -> str:
		"""
		Gives the duration of the currently playing track.

		The duration gets formatted for display.
		:return: The duration of the currently playing track.
		"""
		current_playlist = kek.playlist.Playlist.get_instance().music
		if self.current_track < 0 or self.current_track >= len(current_playlist):
			return ""
		seconds = round(current_playlist[self.current_track]["duration"])
		return str(math.floor(seconds / 60)) + ":" + ("0" if (seconds % 60 < 10) else "") + str(seconds % 60)