# Desktop environment for a domotics hub.
# Copyright (C) 2025 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Keeps track and controls the currently playing video.
"""

import math  # To format time durations.
import PySide6.QtCore  # For exposing these controls to QML.
import PySide6.QtQml  # To instantiate the VideoWindow component.
import time  # To wait for VLC to start up.
import typing
import vlc  # To play video files.

import kek.application


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
		self._is_paused = False  # Whether the video is paused (if playing).

		self.window_component = None
		self.window = None

		self.video_end_timer = PySide6.QtCore.QTimer()
		self.video_end_timer.setSingleShot(True)
		self.video_end_timer.timeout.connect(self.stop)

	def get_window(self):
		if self.window_component is None:  # Lazy load the component.
			engine = kek.application.instance.engine
			self.window_component = PySide6.QtQml.QQmlComponent(engine, PySide6.QtCore.QUrl.fromLocalFile("gui/VideoWindow.qml"))
		if self.window is None:
			self.window = self.window_component.create()
			# Move the window to the second monitor.
			first_screen_width = kek.application.instance.screens()[0].size().width()
			print(first_screen_width)
			self.window.setFramePosition(PySide6.QtCore.QPoint(first_screen_width, 0))
			self.window.showFullScreen()
		return self.window

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
		if self.vlc is not None:
			self.vlc.stop()

		self.vlc = vlc.MediaPlayer("file://" + path)
		self.window = self.get_window()
		self.vlc.set_xwindow(self.window.winId())
		time.sleep(1)
		self.vlc.play()
		while not self.vlc.is_playing():
			time.sleep(0.1)
		self.video_end_timer.setInterval(self.current_duration_float * 1000)
		self.video_end_timer.start()
		self.is_playing_changed.emit()

	@PySide6.QtCore.Slot()
	def stop(self) -> None:
		"""
		Stop playing any video.
		"""
		if self.vlc is not None:
			self.vlc.stop()
		self.vlc = None
		self.video_end_timer.stop()
		self.is_playing_changed.emit()

	is_paused_changed = PySide6.QtCore.Signal()

	def is_paused_set(self, new_is_paused: bool) -> None:
		"""
		Pause or continue the video.
		:param new_is_paused: Whether the music should be paused or running.
		"""
		if self._is_paused == new_is_paused:
			return
		if self.vlc is None:  # No video? Shouldn't happen.
			return
		if new_is_paused:
			self.video_end_timer.stop()
		else:
			self.video_end_timer.setInterval((self.current_duration_float - self.current_playtime_float()) * 1000)
			self.video_end_timer.start()
		self.vlc.set_pause(new_is_paused)
		self._is_paused = new_is_paused
		self.is_paused_changed.emit()

	@PySide6.QtCore.Property(bool, notify=is_paused_changed, fset=is_paused_set)
	def is_paused(self) -> bool:
		"""
		Get whether the currently playing video is currently paused.
		:return: ``True`` if the video is paused, or ``False`` if it is playing.
		"""
		return self._is_paused

	@PySide6.QtCore.Property(str, notify=is_playing_changed)
	def current_duration(self) -> str:
		"""
		Gives the duration of the currently playing video, if any, as human-readable text.

		The duration gets formatted for display.

		If no video is playing, an empty string will be returned.
		:return: The duration of the currently playing track.
		"""
		if self.vlc is None:
			return ""
		seconds = round(self.vlc.get_length() / 1000)
		return str(math.floor(seconds / 60)) + ":" + ("0" if (seconds % 60 < 10) else "") + str(seconds % 60)

	@PySide6.QtCore.Property(float, notify=is_playing_changed)
	def current_duration_float(self) -> float:
		"""
		Get the length of the currently playing video, if any, in seconds.

		If no video is playing, this will return 0. Best not use that value then.
		:return: The duration of the currently playing video, if any.
		"""
		if self.vlc is None:
			return 0
		return self.vlc.get_length() / 1000

	@PySide6.QtCore.Slot(result=str)
	def current_playtime(self) -> str:
		"""
		Read the current time since the video started playing.

		The duration gets formatted for display.

		This does not have an automatic update mechanism since it continuously updates.
		:return: The position in the current video where we are playing.
		"""
		if self.vlc is None:
			return ""
		seconds = round(self.vlc.get_position() * self.vlc.get_length() / 1000)
		return str(math.floor(seconds / 60)) + ":" + ("0" if (seconds % 60 < 10) else "") + str(seconds % 60)

	@PySide6.QtCore.Slot(result=float)
	def current_playtime_float(self) -> float:
		"""
		Read the current time since the video started playing, in seconds as a float.

		This version does not format it. It returns a number for use of seeking.
		:return: The position in the current video where we are playing.
		"""
		if self.vlc is None:
			return 0
		return self.vlc.get_position() * self.vlc.get_length() / 1000

	@PySide6.QtCore.Slot(float)
	def seek(self, fraction: float) -> None:
		"""
		Change the current position in the song.
		:param fraction: A number between 0 and 1, determining where to seek to.
		"""
		if self.vlc is None:
			return
		self.vlc.set_position(fraction)
		if not self.is_paused:
			self.video_end_timer.stop()
			self.video_end_timer.setInterval((self.current_duration_float - self.current_playtime_float()) * 1000)
			self.video_end_timer.start()