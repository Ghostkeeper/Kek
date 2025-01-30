//Desktop environment for a domotics hub.
//Copyright (C) 2024 Ghostkeeper
//This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
//This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
//You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

import QtQuick
import QtQuick.Controls
import QtMultimedia
import "." as Gui

Item {
	anchors.fill: parent

	ShaderEffect {
		id: pulse
		anchors.fill: parent

		property var animationFinished: function() {}
		property point centre: Qt.point(width / 2, height / 2)
		property point size: Qt.point(width, height)
		property real radius: height

		fragmentShader: "graphics/pulse.frag.qsb"

		property real time: 0
		NumberAnimation on time {
			id: timeAnimation

			from: 0
			to: 1
			duration: 1000
			running: false
			loops: 1
			onFinished: pulse.animationFinished()
		}
	}

	//The distance from the centre of each hexagon to each vertex is 250.
	//This makes the smallest radius of the hexagon 250*cos(30).
	//We create 30px spacing between the hexagons.

	Image {
		id: centre_hex
		anchors.centerIn: parent

		source: "graphics/tile_logo.svg"
	}

	//Circle of 6 hexagons surrounding the centre.
	Gui.HexagonButton {
		x: parent.width / 2 + 400.981 - width / 2 //cos(30) * (cos(30)*250*2 + 30) = 400.981
		y: parent.height / 2 + 231.506 - height / 2 //sin(30) * (cos(30)*250*2 + 30) = 231.506

		source: "graphics/tile_music.svg"
		onClickedHandler: function click() {
			pulse.centre = Qt.point(x + width / 2, y + height / 2);
			pulse.animationFinished = function() {
				pageSwapper.source = "Music.qml";
			};
			timeAnimation.restart();
		}
	}
	Gui.HexagonButton {
		x: parent.width / 2 - width / 2
		y: parent.height / 2 + 463.013 - height / 2 //cos(30)*250*2 + 30 = 463.013

		source: "graphics/tile_video.svg"
		onClickedHandler: function click() {
			pulse.centre = Qt.point(x + width / 2, y + height / 2);
			pulse.animationFinished = function() {
				pageSwapper.source = "Video.qml";
			}
			timeAnimation.restart();
		}
	}
	Image {
		x: parent.width / 2 - 400.981 - width / 2
		y: parent.height / 2 + 231.506 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 400.981 - width / 2
		y: parent.height / 2 - 231.506 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - width / 2
		y: parent.height / 2 - 463.013 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 + 400.981 - width / 2
		y: parent.height / 2 - 231.506 - height / 2

		source: "graphics/hexagon.svg"
	}

	//Circle of 12 hexagons in the second ring.
	Image {
		x: parent.width / 2 + 801.962 - width / 2 //cos(30) * (cos(30)*250*2 + 30) * 2 = 801.962
		y: parent.height / 2 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 + 801.962 - width / 2 //cos(30) * (cos(30)*250*2 + 30) * 2 = 801.962
		y: parent.height / 2 + 463.013 - height / 2 //sin(30) * (cos(30)*250*2 + 30) * 2 = 463.013

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 + 400.981 - width / 2
		y: parent.height / 2 + 694.519 - height / 2 //sin(30) * (cos(30)*250*2 + 30) + cos(30)*250*2+30 = 694.519

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - width / 2
		y: parent.height / 2 + 926.025 - height / 2 //cos(30)*250*4 + 30*2 = 926.025

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 400.981 - width / 2
		y: parent.height / 2 + 694.519 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 801.962 - width / 2
		y: parent.height / 2 + 463.013 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 801.962 - width / 2
		y: parent.height / 2 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 801.962 - width / 2
		y: parent.height / 2 - 463.013 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 400.981 - width / 2
		y: parent.height / 2 - 694.519 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - width / 2
		y: parent.height / 2 - 926.025 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 + 400.981 - width / 2
		y: parent.height / 2 - 694.519 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 + 801.962 - width / 2
		y: parent.height / 2 - 463.013 - height / 2

		source: "graphics/hexagon.svg"
	}

	//Far right side.
	Image {
		x: parent.width / 2 + 801.962 - width / 2
		y: parent.height / 2 - 926.025 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 + 1202.942 - width / 2 //cos(30) * (cos(30)*250*2 + 30) * 3 = 1202.942
		y: parent.height / 2 - 694.519 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 + 1202.942 - width / 2
		y: parent.height / 2 - 231.506 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 + 1202.942 - width / 2
		y: parent.height / 2 + 231.506 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 + 1202.942 - width / 2
		y: parent.height / 2 + 694.519 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 + 801.962 - width / 2
		y: parent.height / 2 + 926.025 - height / 2

		source: "graphics/hexagon.svg"
	}

	//Far left side.
	Image {
		x: parent.width / 2 - 801.962 - width / 2
		y: parent.height / 2 + 926.025 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 1202.942 - width / 2
		y: parent.height / 2 + 694.519 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 1202.942 - width / 2
		y: parent.height / 2 + 231.506 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 1202.942 - width / 2
		y: parent.height / 2 - 231.506 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 1202.942 - width / 2
		y: parent.height / 2 - 694.519 - height / 2

		source: "graphics/hexagon.svg"
	}
	Image {
		x: parent.width / 2 - 801.962 - width / 2
		y: parent.height / 2 - 926.025 - height / 2

		source: "graphics/hexagon.svg"
	}
}