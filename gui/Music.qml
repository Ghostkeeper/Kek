//Desktop environment for a domotics hub.
//Copyright (C) 2024 Ghostkeeper
//This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
//This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
//You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

import QtQuick
import QtQuick.Controls
import Kek 1.0 as Kek

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
		model: Kek.MusicDirectory { }
		delegate: Rectangle {
			color: "grey"
			border.width: 2
			border.color: "red"
			width: 30
			height: 30
		}
	}
}