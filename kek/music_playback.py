# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
A collection of functions to actually play audio on the system.
"""

import numpy  # To export Sound objects to a playback buffer.
import pyaudio  # Used to actually play audio through the operating system.
import time  # To sleep the thread when there is no audio to play.
import threading  # The audio is played on a different thread.
import typing

if typing.TYPE_CHECKING:
	import kek.sound

audio_source: typing.Optional["kek.sound.Sound"] = None
"""
The audio track that is currently being played.
"""

current_position = 0.0
"""
The location in the track where we are currently playing (in seconds).
"""

end_position = 0.0
"""
The location in the track where the song ends (in seconds).
"""

is_paused = False
"""
Whether the playback is ongoing, but paused.

While paused the playback thread will not play chunks, but keeps the playback position.
"""

def play(new_audio: "kek.sound.Sound") -> None:
	"""
	Start the playback of a new audio source.
	:param new_audio: The new audio source to play.
	"""
	global audio_source
	global end_position
	end_position = new_audio.duration()
	audio_source = new_audio

def toggle_pause() -> None:
	global is_paused
	is_paused = not is_paused

def stop() -> None:
	"""
	Stop playing any audio.
	"""
	global audio_source
	audio_source = None
	global current_position
	current_position = 0.0
	global is_paused
	is_paused = False

def seek(new_position: float) -> None:
	"""
	Change the current position in the song.
	:param new_position: The new position, in seconds since the start of the song.
	"""
	global current_position
	current_position = new_position

def play_loop() -> None:
	"""
	Main loop of the playback server.

	This function runs indefinitely. It should be ran on a different thread than the main GUI thread.
	It will continuously look for the current position in the current audio source and play it.
	"""
	global current_position
	global audio_source
	audio_server = None
	stream = None

	try:
		audio_server = pyaudio.PyAudio()
		current_sample_width = 0
		current_channels = 0
		current_rate = 0
		while True:
			if audio_source is None or is_paused:
				time.sleep(0.2)
				continue
			chunk_size = 0.2
			chunk = audio_source[current_position:current_position + chunk_size]
			if chunk.channels[0].itemsize != current_sample_width or chunk.frame_rate != current_rate or len(chunk.channels) != current_channels:
				# New audio source, so re-generate the stream.
				if stream:
					stream.stop_stream()
					stream.close()
				current_sample_width = chunk.channels[0].itemsize
				current_rate = chunk.frame_rate
				current_channels = len(chunk.channels)
				stream = audio_server.open(format=audio_server.get_format_from_width(current_sample_width), rate=current_rate, channels=current_channels, output=True)
			if current_position >= end_position:  # Playback completed. Stop taking the GIL and go into stand-by.
				current_position = 0
				audio_source = None
				continue
			samples = numpy.empty(chunk.channels[0].size * len(chunk.channels), dtype=chunk.channels[0].dtype)
			for channel_num, channel in enumerate(chunk.channels):
				samples[channel_num::len(chunk.channels)] = channel
			stream.write(samples.tobytes())
			current_position += chunk_size
	finally:
		if stream:
			stream.stop_stream()
			stream.close()
		if audio_server:
			audio_server.terminate()

play_thread = threading.Thread(target=play_loop, daemon=True)
"""
A thread that continuously sends audio to the operating system to play.
"""
play_thread.start()  # Start that thread to feed audio to the operating system.