# Desktop environment for a domotics hub.
# Copyright (C) 2025 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Since our media is on a NFS drive, it's rather slow to index files. This module tries to speed this
up by storing a local database file containing for each directory, the list of files inside.

This information is gathered in the background.
"""

import csv  # The file format of our cached metadata.
import logging
import os  # To get environment variables for finding the cache directory.
import os.path  # To find the cache and explore the cached files.

import kek.storage  # To find the cache file.

directory_cache = {}

def load() -> None:
	"""
	Load the cache from what's currently stored in the files.

	This should be executed on start-up. The act of scanning the directories will edit the caches,
	and that result would get overridden by what's currently in the cache files.
	"""
	directory_cache = {}
	directory_path = os.path.join(kek.storage.cache(), "directory.csv")
	with open(directory_path, newline="") as directory_file:
		directory_reader = csv.reader(directory_file)
		for row in directory_reader:
			path = row[0]
			files = row[1:]
			directory_cache[path] = list(files)

def store() -> None:
	"""
	Store the caches to disk so that it can get loaded again in the next run.
	"""
	directory_path = os.path.join(kek.storage.cache(), "directory.csv")
	with open(directory_path, "w", newline="") as directory_file:
		directory_writer = csv.writer(directory_file)
		for path in sorted(directory_cache):
			row = [path] + directory_cache[path]
			directory_writer.writerow(row)

def scan() -> None:
	"""
	Updates the cache in the background. This actually does the caching. Run it in a thread!
	"""
	logging.info("Starting scan for updating the cache.")

	# Directories.
	for root, dirs, files in os.walk("/music"):
		directory_cache[root] = files
	logging.info("Finished scan for directories in music.")
	for root, dirs, files in os.walk("/films"):
		directory_cache[root] = files
	logging.info("Finished scan for directories in videos.")

	store()
