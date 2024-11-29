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
					dragged.path = model.path;
					dragged.Drag.active = true;
				} else {
					dragged.Drag.drop();
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

			onClicked: {
				Kek.MusicPlayer.current_track_nr = index;
				Kek.MusicPlayer.is_playing = true;
			}
		}

		ScrollBar.vertical: Gui.ScrollBar {}

		DropArea {
			id: drop_in_playlist
			anchors.fill: parent
			onEntered: drop_place_indicator.visible = true
			onExited: drop_place_indicator.visible = false
			onDropped: {
				drop_place_indicator.visible = false;
				let dropindex = Math.round((drop_place_indicator.y + 2 + parent.contentY) / 50);
				playlist.model.add(dragged.path, dropindex);
			}
		}

		Rectangle {
			id: drop_place_indicator
			width: parent.width
			height: 4

			color: "#007FFF"
			visible: false
			y: Math.min(Math.round((dragged.y + 25 + (parent.contentY % 50)) / 50) * 50 - (parent.contentY % 50) - height / 2, playlist.model.rowCount() * 50 - 2 - parent.contentY)
		}

		//Current track highlight.
		Rectangle {
			width: parent.width
			height: 50
			y: Kek.MusicPlayer.current_track_nr * 50 - parent.contentY

			color: "#007FFF"
			opacity: 0.5
			visible: playlist.model.count > 0
		}
	}

	Column {
		id: player
		anchors {
			top: parent.top
			bottom: parent.bottom
			left: files_table.right
			right: playlist.left
		}

		visible: Kek.MusicPlayer.current_duration !== ""
		spacing: 50

		Image {
			id: cover_image
			anchors {
				horizontalCenter: parent.horizontalCenter
			}
			width: 500
			height: width

			source: Kek.MusicPlayer.current_cover
		}

		Text {
			width: parent.width
			height: 50

			text: Kek.MusicPlayer.current_title
			elide: Text.ElideRight
			horizontalAlignment: Text.AlignHCenter
			verticalAlignment: Text.AlignVCenter
			color: "white"
			font.pointSize: 30
		}

		Row {
			anchors.horizontalCenter: parent.horizontalCenter

			spacing: 50

			Gui.Button {
				source: (Kek.MusicPlayer.is_playing && !Kek.MusicPlayer.is_paused) ? "graphics/pause.svg" : "graphics/play.svg";
				onClicked: {
					if(Kek.MusicPlayer.is_playing) {
						Kek.MusicPlayer.is_paused = !Kek.MusicPlayer.is_paused;
					} else {
						Kek.MusicPlayer.is_playing = true;
					}
				}
			}
			Gui.Button {
				source: "graphics/stop.svg"
				onClicked: Kek.MusicPlayer.is_playing = false;
			}
		}

		Row {
			Text { //Total duration.
				text: Kek.MusicPlayer.current_duration
				elide: Text.ElideRight
				verticalAlignment: Text.AlignVCenter
				color: "white"
				font.pointSize: 30
			}
		}
	}

	Rectangle {
		id: dragged
		width: files_table.width
		height: 50

		color: "#800080FF"
		visible: Drag.active
		property string path: ""

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
