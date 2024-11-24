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

	ListView {
		id: files_table
		anchors {
			top: parent.top
			bottom: parent.bottom
			left: parent.left
		}
		width: Math.floor(parent.width / 3)

		flickableDirection: Flickable.VerticalFlick
		clip: true
		model: Kek.MusicDirectory {
			id: music_directory
		}
		delegate: MouseArea {
			width: parent ? parent.width : 0
			height: 50

			drag.target: dragged
			property bool dragActive: drag.active //To be able to listen to drag.active changes.
			property string filename: model.name ? model.name : ""

			onPressed: {
				//Prepare for dragging in case we're going to drag it.
				dragged.x = 0;
				dragged.y = y;
			}
			onClicked: {
				if(model.type === "directory") {
					music_directory.directory = model.path;
				} else {
					playlist.model.add(model.path, playlist.model.rowCount());
				}
			}
			onDragActiveChanged: {
				if(drag.active) {
					dragged_text.text = filename;
					dragged.visible = true;
				} else {
					dragged.visible = false;
				}
			}

			Image {
				id: type_icon
				width: 50
				height: 50
				source: {
					if(model.type === "directory") return "graphics/directory.svg";
					if(model.type === "uncompressed") return "graphics/music_lossless.svg";
					if(model.type === "compressed") return "graphics/music_lossy.svg";
					return "";
				}
			}

			Text {
				anchors {
					left: type_icon.right
					right: duration.left
					top: parent.top
					bottom: parent.bottom
				}

				text: filename
				elide: Text.ElideRight
				verticalAlignment: Text.AlignVCenter
				color: "white"
				font.pointSize: 30
			}

			Text {
				id: duration
				anchors {
					right: parent.right
					top: parent.top
					bottom: parent.bottom
				}
				width: 130

				text: model.duration ? model.duration : ""
				elide: Text.ElideRight
				verticalAlignment: Text.AlignVCenter
				color: "white"
				font.pointSize: 30
			}
		}

		ScrollBar.vertical: Gui.ScrollBar {}
	}

	ListView {
		id: playlist
		anchors {
			top: parent.top
			bottom: parent.bottom
			right: parent.right
		}
		width: Math.floor(parent.width / 3)

		flickableDirection: Flickable.VerticalFlick
		clip: true
		model: Kek.Playlist
		delegate: MouseArea {
			width: parent ? parent.width : 0
			height: 50

			Text {
				anchors.fill: parent

				text: model.title
				elide: Text.ElideRight
				verticalAlignment: Text.AlignVCenter
				color: "white"
				font.pointSize: 30
			}
		}

		ScrollBar.vertical: Gui.ScrollBar {}
	}

	Rectangle {
		id: dragged
		width: files_table.width
		height: 50

		color: "#800080FF"
		visible: false

		Text {
			id: dragged_text
			anchors {
				left: parent.left
				leftMargin: 50
				right: parent.right
				rightMargin: 130
				top: parent.top
				bottom: parent.bottom
			}

			text: ""
			elide: Text.ElideRight
			verticalAlignment: Text.AlignVCenter
			color: "white"
			font.pointSize: 30
		}
	}
}
