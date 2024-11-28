# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Defines a Sound object, which contains the wave data of a music track.
"""

import ctypes  # For correctly converting Opus files to Numpy.
import miniaudio  # To decode wav, mp3, flac and ogg audio files.
import numpy  # For fast operations on wave data.
import os.path  # To decode audio files depending on file extension.
import pyogg  # To decode opus audio files.
import typing

class Sound:
	"""
	This class represents an audio segment.

	It contains the raw audio data (samples), as well as some metadata on how to interpret it, such as frame rate.
	"""

	@classmethod
	def decode(clscls, filepath: str) -> "Sound":
		"""
		Decode an encoded sound file, loading it as a Sound instance.
		:param filepath: The path to the file to load.
		:return: A Sound containing the audio data from that file.
		"""
		_, extension = os.path.splitext(filepath)
		extension = extension.lower()
		if extension in {".flac", ".mp3", ".ogg", ".wav"}:
			decoded = miniaudio.decode_file(filepath)
			samples = numpy.asarray(decoded.samples)
			channels = [samples[channel_num::decoded.nchannels] for channel_num in range(decoded.nchannels)]
			sample_rate = decoded.sample_rate
		elif extension in {".opus"}:
			opus_file = pyogg.OpusFile(filepath)
			# PyOgg has an as_array method but it seems to have been removed from the latest release.
			# So we re-implement it ourselves.
			bytes_per_sample = ctypes.sizeof(pyogg.opus.opus_int16)
			channels = numpy.ctypeslib.as_array(opus_file.buffer, (opus_file.buffer_length // bytes_per_sample // opus_file.channels, opus_file.channels))
			channels = channels.transpose()
			sample_rate = opus_file.frequency
		else:
			raise ValueError(f"Trying to decode unsupported file extension {extension}.")
		return Sound(channels, frame_rate=sample_rate)

	def __init__(self, channels: list[numpy.array], frame_rate: int=44100) -> None:
		"""
		Construct a new audio clip using the raw sample data.
		:param channels: Audio signal waveforms. This is a list of arrays, one array of audio data for each channel.
		Each array enumerates the audio samples for that channel. The data types of these waveforms can vary depending on
		the bit depth of the audio signal, but should always be integer-based.
		:param frame_rate: The number of frames to play per second (Hz).
		"""
		self.channels = channels
		self.frame_rate = frame_rate

	def __getitem__(self, index: typing.Union[int, float, slice]) -> "Sound":
		"""
		Get a sub-segment of this sound.

		If the segment given is partly out of range, the sound will be shorter than the desired length.

		The step element of a slice is ignored. Only the start and end of the slice is used.

		The index and slice bounds are given by the duration in the song, in seconds. They can be floats.
		:param index: Either a single number to indicate a timestamp you want to access, or a slice to indicate a
		range of time.
		:return: A part of this sound. If given a single index, the sound will last for at most 1 second. If given a
		range, the sound will be the length of that range.
		"""
		duration = self.duration()
		start = 0.0
		end = duration
		if isinstance(index, slice):
			if index.start:
				start = index.start
			if index.stop:
				end = index.stop
		else:
			start = index
			end = index + 1

		# Negative indices indicate a duration from the end of the sound.
		if start < 0:
			start += duration
		if end < 0:
			end += duration
		# Clamp to the range of duration of the sound.
		start = max(0.0, min(duration, start))
		end = max(0.0, min(duration, end))
		# Convert to positions in the sample array.
		start = round(start * self.frame_rate)
		end = round(end * self.frame_rate)
		clipped = [channel[start:end] for channel in self.channels]
		return Sound(clipped, self.frame_rate)

	def duration(self) -> float:
		"""
		Get the length of the sound, in seconds.
		:return: How long it takes to play this sound.
		"""
		return len(self.channels[0]) / self.frame_rate