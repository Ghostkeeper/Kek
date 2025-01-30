//Desktop environment for a domotics hub.
//Copyright (C) 2025 Ghostkeeper
//This application is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
//This application is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
//You should have received a copy of the GNU Affero General Public License along with this application. If not, see <https://gnu.org/licenses/>.

import QtQuick
import QtQuick.Controls

Item {
    signal clicked

    MouseArea {
        anchors.fill: parent

        propagateComposedEvents: true
        onClicked: mouse => {
            let middle_x = width / 2;
            let middle_y = height / 2;
            let quadrant_x = Math.abs(mouseX - middle_x);
            let quadrant_y = Math.abs(mouseY - middle_y);
            if(middle_x * middle_y - middle_y / 2 * quadrant_y - middle_x * quadrant_x >= 0) {
                parent.clicked(); //Is within the hexagon.
            } else {
                mouse.accepted = false;
            }
        }
        onPressed: mouse => {
            let middle_x = width / 2;
            let middle_y = height / 2;
            let quadrant_x = Math.abs(mouseX - middle_x);
            let quadrant_y = Math.abs(mouseY - middle_y);
            if(middle_x * middle_y - middle_y / 2 * quadrant_y - middle_x * quadrant_x < 0) {
                mouse.accepted = false; //Not in the hexagon.
            }
        }
    }
}