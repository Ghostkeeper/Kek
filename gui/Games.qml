//Desktop environment for a domotics hub.
//Copyright (C) 2025 Ghostkeeper
//This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
//This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
//You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

import QtQuick

ListView {
	id: gallery
	anchors.fill: parent

	snapMode: ListView.SnapToItem
	delegate: Image {
		width: gallery.width
		height: gallery.height

		fillMode: Image.PreserveAspectFit
		source: model.source
	}

	model: ListModel {
		ListElement { source: "../games/ganzenbord.png" }
		ListElement { source: "../games/chess.png" }
		ListElement { source: "../games/checkers.png" }
		ListElement { source: "../games/halma.svg" }
		ListElement { source: "../games/risk.jpg" }
		ListElement { source: "../games/snakes-and-ladders.svg" }
	}
}