# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Defines a dictionary of metadata about music files, and some functions to edit it.
"""

import logging
import mutagen  # To read metadata from music files.
import mutagen.easyid3
import mutagen.flac
import mutagen.id3
import mutagen.mp3
import mutagen.ogg
import mutagen.wave
import os.path  # To find the database file.
import sqlite3  # To store metadata in a database.
import time  # To store the database after a certain amount of time.
import threading  # To store the database after a certain amount of time.
import typing
import uuid  # To store the cover in a randomly named cache file.

import kek.storage  # To find the database file.

metadata: dict[str, typing.Any] = {}
"""
Cache for metadata about music files.
"""


metadata_lock = threading.Lock()
"""
While the metadata dictionary is modified or iterated over, this lock has to be obtained.
"""


def load() -> None:
	"""
	Reads the metadata from the database file into memory.

	All of the metadata in the database file will get stored in the ``metadata`` dict.
	"""
	db_file = os.path.join(kek.storage.cache(), "music.db")
	logging.info(f"Reading music metadata from: {db_file}")
	if not os.path.exists(db_file):
		return  # No metadata to read.
	connection = sqlite3.connect(db_file)
	logging.debug("Reading metadata from music database.")

	new_metadata = {}  # First store it in a local variable (faster). Merge afterwards.
	for path, duration, title, artist, album, cover, cachetime in connection.execute("SELECT * FROM metadata"):
		new_metadata[path] = {
			"path": path,
			"duration": duration,
			"title": title,
			"artist": artist,
			"album": album,
			"cover": cover,
			"cachetime": cachetime,
		}
	with metadata_lock:
		metadata.update(new_metadata)


# When we change the database, save the database to disk after a short delay.
# If there's multiple changes in short succession, those will be combined into a single write.
def store_after() -> None:
	"""
	Waits a certain amount of time, then stores the metadata to disk.

	This function should be run on a thread, so as to not freeze the application.
	"""
	time.sleep(0.25)
	store()
	global store_thread
	store_thread = None


store_thread: typing.Optional[threading.Thread] = None
"""
Thread that waits a moment, and then stores the database.

The wait is to coalesce more changes into a single write, if many metadata entries change at once.

If this thread is None, no thread is running and a new thread should be started if there is more metadata to write. If
the thread is still running, the database is not yet saved.

Note that this is imperfect. If the metadata changes while the database is still writing (after the sleep), the latest
changes will not be written to disk. As such, it is wise to also save the database at application closing. 
"""


def trigger_store() -> None:
	"""
	After a set amount of time, triggers the serialisation of metadata to disk.
	"""
	global store_thread
	if store_thread is None:
		store_thread = threading.Thread(target=store_after)
	if not store_thread.is_alive():
		store_thread.start()


def store() -> None:
	"""
	Serialises the metadata on disk in a database file.
	"""
	db_file = os.path.join(kek.storage.cache(), "music.db")
	if not os.path.exists(db_file):
		# Create the database anew.
		logging.info("Creating music database.")
		connection = sqlite3.connect(db_file)
		connection.execute("""CREATE TABLE metadata(
			path text PRIMARY KEY,
			duration real,
			title text,
			artist text,
			album text,
			cover text,
			cachetime real
		)""")
	else:
		connection = sqlite3.connect(db_file)

	local_metadata = metadata  # Cache locally for performance.
	with metadata_lock:
		for path, entry in local_metadata.items():
			connection.execute("INSERT OR REPLACE INTO metadata (path, duration, title, artist, album, cover, cachetime) VALUES (?, ?, ?, ?, ?, ?, ?)",
				(path, entry["duration"], entry["title"], entry["artist"], entry["album"], entry["cover"], entry["cachetime"]))
	connection.commit()


def has(path: str) -> bool:
	"""
	Get whether we have any metadata entry about a file.

	If we don't have any metadata, getting metadata would raise a ``KeyError``.
	:param path: The path to test for.
	:return: ``True`` if we have a metadata entry about the file, or ``False`` if we don't.
	"""
	return path in metadata


def get(path: str, field: str) -> typing.Any:
	"""
	Get a metadata field from the cache about a certain file.
	:param path: The file to get the metadata field from.
	:param field: The name of the metadata field to get. Must be one of the known metadata fields in the database!
	:return: The value of the metadata entry for that field. Will be ``None`` if there is no cached information about
	that field.
	"""
	if path not in metadata:
		add_file(path)
	return metadata[path][field]


def add(path: str, entry: typing.Dict[str, typing.Any]) -> None:
	"""
	Add or override a metadata entry for a certain file.
	:param path: The path to the file that the metadata is for.
	:param entry: A dictionary containing metadata.
	"""
	with metadata_lock:
		metadata[path] = entry
	trigger_store()


def add_file(path: str) -> None:
	"""
	Read the metadata from a given file and store it in our database.

	This will check if the file has been modified since it was last stored in the database. If the database is still up
	to date, nothing is changed. If the entry is not present in the database or outdated, it will add or update the
	entry respectively.
	:param path: The path to the file to read the metadata from.
	"""
	local_metadata = metadata  # Cache locally for performance.
	last_modified = os.path.getmtime(path)
	if path in local_metadata and local_metadata[path]["cachetime"] >= last_modified:
		return  # Already up to date.
	if path in local_metadata:
		logging.debug(f"Updating metadata for {path} because {local_metadata[path]['cachetime']} is earlier than {last_modified}")
	else:
		logging.debug(f"Updating metadata for {path} because we don''t have an entry for it yet.")

	cover = ""
	mime_to_extension = {
		"image/jpeg": ".jpg",
		"image/png": ".png",
		"image/gif": ".gif",
	}
	try:
		f = mutagen.File(path)
		if type(f) in {mutagen.mp3.MP3, mutagen.wave.WAVE}:  # Uses ID3 tags.
			id3 = mutagen.easyid3.EasyID3(path)
			title = id3.get("title", [os.path.splitext(os.path.basename(path))[0]])[0]
			artist = id3.get("artist", [""])[0]
			album = id3.get("album", [""])[0]
			apic_keys = list(filter(lambda t: t.startswith("APIC:"), f.keys()))
			apics = list(filter(lambda a: len(a.data) > 0, [f[key] for key in apic_keys]))
			if len(apics) > 0:
				mime = apics[0].mime
				if mime in mime_to_extension:
					extension = mime_to_extension[mime]
					cover_fname = os.path.join(kek.storage.cache(), "covers", str(uuid.uuid4()) + extension)
					with open(cover_fname, "wb") as cover_fstream:
						cover_fstream.write(apics[0].data)
						cover = cover_fname
		elif type(f) == mutagen.flac.FLAC:
			title = f.get("title", [os.path.splitext(os.path.basename(path))[0]])[0]
			artist = f.get("artist", [""])[0]
			album = f.get("album", [""])[0]
			if len(f.pictures) > 0:
				extension = mime_to_extension[f.pictures[0].mime]
				cover_fname = os.path.join(kek.storage.cache(), "covers", str(uuid.uuid4()) + extension)
				with open(cover_fname, "wb") as cover_fstream:
					cover_fstream.write(f.pictures[0].data)
					cover = cover_fname
		elif isinstance(f, mutagen.ogg.OggFileType):  # Vorbis Comment
			title = f.get("title", [os.path.splitext(os.path.basename(path))[0]])[0]
			artist = f.get("artist", [""])[0]
			album = f.get("album", [""])[0]
			# TODO: Don't know yet how to get album covers from these and have no files to test with.
		else:  # Unknown file type.
			title = os.path.splitext(os.path.basename(path))[0]
			artist = ""
			album = ""
		duration = f.info.length
	except Exception as e:
		logging.warning(f"{type(e)}: Unable to get metadata from {path}: {e}")
		title = ""
		artist = ""
		album = ""
		duration = -1
	# We tend to store the album cover as a separate file in the same directory.
	if cover == "":
		dir_name = os.path.basename(os.path.dirname(path))
		for maybe_cover in {dir_name + ".jpg", dir_name + ".png", dir_name + ".gif"}:
			maybe_cover = os.path.join(os.path.dirname(path), maybe_cover)
			if os.path.exists(maybe_cover):
				cover = maybe_cover
				break

	add(path, {
		"path": path,
		"duration": duration,
		"title": title,
		"artist": artist,
		"album": album,
		"cover": cover,
		"cachetime": last_modified,
	})


def is_music_file(path: str) -> bool:
	"""
	Returns whether the given file is a music file that we can read.
	:param path: The file to check.
	:return: ``True`` if it is a music track, or ``False`` if it isn't.
	"""
	if not os.path.isfile(path):
		return False  # Only read files.
	ext = os.path.splitext(path)[1]
	ext = ext.lower()
	return ext in [".mp3", ".flac", ".ogg", ".opus", ".wav"]  # Supported file formats.


def add_directory(path: str) -> None:
	"""
	Read the metadata from all music files in a directory (not its subdirectories) and store them in our database.

	This will update all metadata in the database about the files in this directory so that it's all up to date again.
	:param path: The path to the directory to read the files from.
	"""
	files = set(filter(is_music_file, [os.path.join(path, filename) for filename in os.listdir(path)]))
	for filepath in files:
		add_file(filepath)