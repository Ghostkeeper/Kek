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
			right: parent.horizontalCenter
		}

		flickableDirection: Flickable.VerticalFlick
		clip: true
		model: Kek.MusicDirectory {
			id: music_directory
		}
		delegate: MouseArea {
			width: parent ? parent.width : 0
			height: 50

			onClicked: {
				if(model.type === "directory") {
					music_directory.directory = model.path;
				} else {
					//TODO: Add to playlist.
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

				text: model.name
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

                text: model.duration
                elide: Text.ElideRight
                verticalAlignment: Text.AlignVCenter
                color: "white"
                font.pointSize: 30
            }
		}

		ScrollBar.vertical: Gui.ScrollBar {}
	}
}
