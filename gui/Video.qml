//Desktop environment for a domotics hub.
//Copyright (C) 2025 Ghostkeeper
//This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
//This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
//You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

import QtQuick
import QtQuick.Controls
import Kek 1.0 as Kek
import "." as Gui

Item {
	anchors.fill: parent

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
					id: documentaries_header
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
				id: documentaries_table
				width: parent.width
				height: parent.height - documentaries_header.height - parent.spacing

				flickableDirection: Flickable.VerticalFlick
				model: Kek.VideoDirectory {
					id: documentaries_directory
					default_directory: "Documentaires"
				}
				delegate: MouseArea {
					width: parent ? parent.width : 0
					height: 50

					onClicked: {
						if(model.type === "directory") {
							documentaries_directory.directory = model.path;
						} else {
							Kek.VideoPlayer.play(model.path);
						}
					}

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
						elide: Text.ElideRight
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
					default_directory: "Films"
				}
				delegate: MouseArea {
					width: parent ? parent.width : 0
					height: 50

					onClicked: {
						if(model.type === "directory") {
							films_directory.directory = model.path;
						} else {
							Kek.VideoPlayer.play(model.path);
						}
					}

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
						elide: Text.ElideRight
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
					id: series_header
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
				id: series_table
				width: parent.width
				height: parent.height - series_header.height - parent.spacing

				flickableDirection: Flickable.VerticalFlick
				model: Kek.VideoDirectory {
					id: series_directory
					default_directory: "Series"
				}
				delegate: MouseArea {
					width: parent ? parent.width : 0
					height: 50

					onClicked: {
						if(model.type === "directory") {
							series_directory.directory = model.path;
						} else {
							Kek.VideoPlayer.play(model.path);
						}
					}

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
						elide: Text.ElideRight
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
	}

	//Player overlay on top of the headers.
	Rectangle {
		id: player
		width: parent.width
		height: films_header.height

		visible: Kek.VideoPlayer.is_playing
		color: "black"

		Column {
			anchors.fill: parent
			spacing: 50

			Row {
				anchors.horizontalCenter: parent.horizontalCenter

				spacing: 50

				Gui.Button {
					source: Kek.VideoPlayer.is_paused ? "graphics/play.svg" : "graphics/pause.svg"
					onClicked: Kek.VideoPlayer.is_paused = !Kek.VideoPlayer.is_paused;
				}

				Gui.Button {
					source: "graphics/stop.svg"
					onClicked: Kek.VideoPlayer.stop()
				}
			}

			Item {
				anchors.horizontalCenter: parent.horizontalCenter
				width: parent.width * 2 / 3
				height: 50

				Timer { //Refresh timer for the playtime text and progress bar width.
					interval: 100 //10fps
					running: player.visible
					repeat: true
					onTriggered: {
						current_playtime.text = Kek.VideoPlayer.current_playtime();
						progress_bar.width = Kek.VideoPlayer.current_playtime_float() / Kek.VideoPlayer.current_duration_float * progress_bar_background.width;
					}
				}

				Text {
					id: current_playtime
					width: 150
					height: parent.height

					text: ""
					elide: Text.ElideRight
					verticalAlignment: Text.AlignVCenter
					color: "white"
					font.pointSize: 30
				}
				Text { //Total duration.
					id: total_duration
					anchors.right: parent.right
					width: 150
					height: parent.height

					text: Kek.VideoPlayer.current_duration
					elide: Text.ElideRight
					horizontalAlignment: Text.AlignRight
					verticalAlignment: Text.AlignVCenter
					color: "white"
					font.pointSize: 30
				}
				MouseArea {
					id: progress_bar_background
					anchors {
						left: current_playtime.right
						right: total_duration.left
						top: parent.top
						bottom: parent.bottom
					}

					onClicked: Kek.VideoPlayer.seek(mouseX / width);

					Rectangle {
						id: progress_bar
						height: parent.height
						width: Kek.VideoPlayer.current_playtime_float() / Kek.VideoPlayer.current_duration_float * progress_bar_background.width

						color: "#007FFF"
					}
				}
			}
		}
	}
}
