# Desktop environment for a domotics hub.
# Copyright (C) 2024 Ghostkeeper
# This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

"""
Entry point for the application. This starts a QtApplication.
"""

import os.path  # To store the logging in the correct place, and change the working directory.
os.chdir(os.path.dirname(__file__))  # Make sure that imports can't load untrusted code.

import logging.handlers  # To configure logging.
import signal  # To catch interrupts that need to stop the application.
import sys  # Give the correct exit code.'

import kek.application
import kek.storage

if __name__ == "__main__":
	# Configure logging.
	kek.storage.ensure_exists()
	file_handler = logging.handlers.RotatingFileHandler(os.path.join(kek.storage.data(), "kek.log"), maxBytes=1024 * 1024 * 10, backupCount=2, encoding="utf-8")  # Limit log file size to 10MB.
	console_handler = logging.StreamHandler()
	logging.basicConfig(
		level=logging.INFO,
		format="%(levelname)s:%(asctime)s | %(message)s",
		handlers=[file_handler, console_handler]
	)

	signal.signal(signal.SIGINT, signal.SIG_DFL)  # Python is not handling SIGINT, so let the kernel do that.
	app = kek.application.Application(sys.argv)
	sys.exit(app.exec())
