# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
This module provides some functions to get directories where to store certain types of files for
this application.
"""

import logging
import os  # To get and create OS-specific paths.
import os.path  # To construct new paths.

def data() -> str:
	"""
	Get the location where data files should be stored.
	:return: A path to a directory where data for the application is stored.
	"""
	try:
		path = os.environ["XDG_DATA_HOME"]  # XDG standard storage location.
	except KeyError:
		path = os.path.join(os.path.expanduser("~"), ".local", "share")  # Most Linux machines.
	return os.path.join(path, "kek")


def cache() -> str:
	"""
	Get the location where cache files should be stored.
	:return: A path to a directory where the cache of the application is stored.
	"""
	try:
		path = os.environ["XDG_CACHE_HOME"]  # XDG standard storage location.
	except KeyError:
		path = os.path.join(os.path.expanduser("~"), ".cache")  # Most Linux machines.
	return os.path.join(path, "kek")


def ensure_exists() -> None:
	"""
	Ensure that the storage locations all exist.

	This is usually only necessary for the first run.
	"""
	data_path = data()
	if not os.path.exists(data_path):
		logging.info(f"Creating data directory in {data_path}")
		os.makedirs(data_path)
	cache_path = cache()
	if not os.path.exists(cache_path):
		logging.info(f"Creating cache directory in {cache_path}")
		os.makedirs(cache_path)
		covers_dir = os.path.join(cache_path, "covers")
		if not os.path.exists(covers_dir):
			os.makedirs(covers_dir)