//Desktop environment for a domotics hub.
//Copyright (C) 2024 Ghostkeeper
//This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
//This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
//You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

import QtQuick
import QtQuick.Controls
import Kek 1.0 as Kek
import "." as Gui

Item {
	anchors.fill: parent

	TableView {
		id: files_table
		anchors {
			top: parent.top
			bottom: parent.bottom
			left: parent.left
			right: parent.horizontalCenter
		}

		flickableDirection: Flickable.VerticalFlick
		clip: true
		model: Kek.MusicDirectory {
			id: music_directory
		}
		delegate: MouseArea {
			implicitWidth: {
				const field = music_directory.headerData(column, Qt.Horizontal, Qt.DisplayRole);
				if(field === "type") return 50;
				if(field === "name") return files_table.width - 200;
				return 150; //Duration.
			}
			implicitHeight: 50

			onClicked: {
				if(music_directory.entry_type(row) === "directory") {
					music_directory.directory = music_directory.headerData(row, Qt.Vertical, Qt.DisplayRole);
				} else {
					//TODO: Add to playlist.
				}
			}

			Text {
				anchors.fill: parent
				visible: music_directory.headerData(column, Qt.Horizontal, Qt.DisplayRole) !== "type"

				text: display
				elide: Text.ElideRight
				color: "white"
				font.pointSize: 35
			}

			Image {
				width: 50
				height: 50

				visible: music_directory.headerData(column, Qt.Horizontal, Qt.DisplayRole) === "type"
				source: {
					if(display === "directory") return "graphics/home.svg";
					if(display === "uncompressed") return "graphics/home.svg";
					if(display === "compressed") return "graphics/home.svg";
					return "";
				}
			}
		}
		ScrollBar.vertical: Gui.ScrollBar {}
	}
}