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
			id: films_header
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

		ListView {
			id: films_table
			width: parent.width
			height: parent.height - films_header.height - parent.spacing

			flickableDirection: Flickable.VerticalFlick
			model: Kek.VideoDirectory {
				id: films_directory
			}
			delegate: MouseArea {
				width: parent ? parent.width : 0
				height: 50

				Image {
					id: type_icon
					width: 50
					height: 50
					source: {
						if(model.type === "directory") return "graphics/directory.svg";
						if(model.type === "film") return "graphics/video.svg";
						return "";
					}
				}

				Text {
					anchors {
						left: type_icon.right
						right: year.right
						top: parent.top
						bottom: parent.bottom
					}

					text: model.title
					elide: Text.ElideLeft
					verticalAlignment: Text.AlignVCenter
					color: "white"
					font.pointSize: 30
				}
				Text {
					id: year
					anchors {
						right: rating.left
						top: parent.top
						bottom: parent.bottom
					}
					width: 100

					text: model.year ? "" + model.year : ""
					verticalAlignment: Text.AlignVCenter
					color: "white"
					font.pointSize: 30
				}
				Text {
					id: rating
					anchors {
						right: parent.right
						top: parent.top
						bottom: parent.bottom
					}
					width: 50

					text: model.rating ? "" + model.rating : ""
					verticalAlignment: Text.AlignVCenter
					color: "white"
					font.pointSize: 30
				}
			}

			ScrollBar.vertical: Gui.ScrollBar {}
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
