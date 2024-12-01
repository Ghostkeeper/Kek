//Desktop environment for a domotics hub.
//Copyright (C) 2024 Ghostkeeper
//This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
//This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
//You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

import QtQuick
import QtQuick.Controls
import Kek 1.0 as Kek
import "." as Gui

Row {
	anchors.fill: parent

	spacing: 20

	Column { //Documentaries column.
		width: (parent.width - 40) / 3
		height: parent.height

		Image {
			anchors.horizontalCenter: parent.horizontalCenter

			source: "graphics/documentaries.jpg"

			Image {
				anchors {
					left: parent.left
					right: parent.right
					bottom: parent.bottom
				}
				height: 200

				source: "graphics/fade_black.svg"
			}
		}
	}

	Column { //Films column.
		width: (parent.width - 40) / 3
		height: parent.height

		Image {
			anchors.horizontalCenter: parent.horizontalCenter

			source: "graphics/films.jpg"

			Image {
				anchors {
					left: parent.left
					right: parent.right
					bottom: parent.bottom
				}
				height: 200

				source: "graphics/fade_black.svg"
			}
		}
	}

	Column { //Series column.
		width: (parent.width - 40) / 3
		height: parent.height

		Image {
			anchors.horizontalCenter: parent.horizontalCenter

			source: "graphics/series.jpg"

			Image {
				anchors {
					left: parent.left
					right: parent.right
					bottom: parent.bottom
				}
				height: 200

				source: "graphics/fade_black.svg"
			}
		}
	}
}
