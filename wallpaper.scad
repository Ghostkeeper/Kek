$fn = 6;

//Walls.
difference() {
    translate([-1, 0, -1]) {
        cube([1002, 2001, 702]);
    }
    translate([0, -1, 0]) {
        cube([1000, 2001, 700]);
    }
}

//Table in the centre.
translate([500, 1000, 0]) {
    translate([0, 0, 90]) {
        cylinder(h=10, r=200);
        translate([0, 0, 10]) {
            cylinder(h=1, r1=200, r2=0);
        }
    }
    difference() {
        cylinder(h=200, r1=30, r2=0);
        translate([0, 0, 90]) {
            cylinder(h=200, r=40);
        }
    }
}

//Lines along the wall to emphasise perspective.
translate([0, 0, 100]) {
    cube([1, 2000, 100]);
}
translate([0, 0, 300]) {
    cube([1, 2000, 100]);
}
translate([0, 0, 500]) {
    cube([1, 2000, 100]);
}
translate([999, 0, 100]) {
    cube([1, 2000, 100]);
}
translate([999, 0, 300]) {
    cube([1, 2000, 100]);
}
translate([999, 0, 500]) {
    cube([1, 2000, 100]);
}

//"Sidewalks".
cube([150, 2000, 30]);
translate([850, 0, 0]) {
    cube([150, 2000, 30]);
}

//Benches.
module bench() {
    cube([100, 500, 100]);
    for(y = [10 : 20 : 500]) {
        translate([0, y, 0]) {
            cube([101, 10, 101]);
        }
    }
    for(x = [10 : 20 : 100]) {
        translate([x, -1, 0]) {
            cube([10, 1, 100]);
        }
    }
    difference() { //Bands behind benches.
        cube([10, 500, 670]);
        translate([10, 0, 0]) {
            scale([10/250, 1, 1]) {
                cylinder(h=670, r=250, $fn=60);
            }
        }
        translate([10, 500, 0]) {
            scale([10/250, 1, 1]) {
                cylinder(h=670, r=250, $fn=60);
            }
        }
    }
}
translate([0, 250, 30]) {
    bench();
}
translate([0, 1250, 30]) {
    bench();
}
translate([1000, 250, 30]) {
    mirror([1, 0, 0]) {
        bench();
    }
}
translate([1000, 1250, 30]) {
    mirror([1, 0, 0]) {
        bench();
    }
}

//TV table.
translate([0, 1900, 0]) {
    cube([249, 100, 80]);
}
translate([251, 1900, 0]) {
    cube([248, 100, 80]);
}
translate([501, 1900, 0]) {
    cube([248, 100, 80]);
}
translate([751, 1900, 0]) {
    cube([249, 100, 80]);
}

//TV.
translate([250, 1980, 200]) {
    difference() {
        cube([500, 20, 300]);
        translate([30, -1, 30]) {
            cube([440, 2, 240]);
        }
    }
}
translate([0, 1990, 200]) { //Bands behind TV.
    difference() {
        cube([1000, 10, 300]);
        scale([1, 10/250, 1]) {
            rotate([0, 90, 0]) {
                cylinder(h=1000, r=150, $fn=60);
                translate([-300, 0, 0]) {
                    cylinder(h=1000, r=150, $fn=60);
                }
            }
        }
    }
}

//Tiles on ceiling and floor.
module tiles() {
    intersection() {
        union() {
            for(x = [0:150:1100]) {
                for(y = [0:sin(60)*300:2100]) {
                    translate([x, y, 0]) {
                        cylinder(h=0.2, r=50);
                    }
                }
            }
            for(x = [cos(60)*150:150:1100]) {
                for(y = [sin(60)*150:sin(60)*300:2100]) {
                    translate([x, y, 0]) {
                        cylinder(h=0.2, r=50);
                    }
                }
            }
            for(x = [0:150:1100]) {
                for(y = [sin(60)*100:sin(60)*300:2100]) {
                    translate([x, y, 0]) {
                        cylinder(h=0.1, r=50);
                    }
                }
            }
            for(x = [cos(60)*150:150:1100]) {
                for(y = [sin(60)*250:sin(60)*300:2100]) {
                    translate([x, y, 0]) {
                        cylinder(h=0.1, r=50);
                    }
                }
            }
        }
        cube([1000, 2000, 2]);
    }
}
tiles();
translate([0, 0, 700]) {
    mirror([0, 0, 1]) {
        tiles();
    }
}

//Big hexagon on the ceiling.
translate([500, 1000, 697]) {
    cylinder(h=3, r=400);
}