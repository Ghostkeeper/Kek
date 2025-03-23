What Is This?
====
This is a project made by Ghostkeeper for his own coffee table build, which has a touch screen built-in. It is designed to turn the table into some sort of media centre or home control. It runs when the table is turned on and effectively becomes the operating system.

I consider this a personal project. I'm documenting the process mostly for myself. Feel free to use the software or take inspiration from it according to its license, but don't expect that I would make any attempt to make it easier for others to use it. I'm taking all sorts of shortcuts to make it easier for myself which may not be applicable to other (or even similar) uses of the software.

Installation
====
In order to install this program on the table (or indeed any Debian-based Linux distribution), you have to install the following packages:

```
sudo apt install libportaudio2 libxcb-cursor0
```

Configurations Outside of the Program
====
Other than this application, a few modifications have to be made to the rest of the computer for the correct experience.

Autostart
----
Start the application on start-up, by triggering the following script:

```
/home/mouse/Kek/venv/bin/python3 /home/mouse/Kek
```

It works to put this in a script in the home directory and call that shell script by adding the following header to `~/.config/wayfire.ini`:

```
[autostart]
kek = /home/mouse/kek.sh
```

Desktop background
----
Change the desktop background to the `wallpaper.png` file provided with this repository.

Browser modifications
----
This application starts a Firefox process for certain parts of its operation. For the proper experience, make the following modifications to your Firefox installation:
* In about:config, change the `dom.allow_scripts_to_close_windows` setting to `true`. This is because we'll add a script to certain pages which adds a button to close the page (the browser), which lets the user go back to the main menu.
* Install the Greasemonkey extension.
* In Greasemonkey, add the contents of the `greasemonkey-map.js` script as a new user script, to modify openstreetmap.org to display the map in dark mode, removing some menus, and to add a button to return to the main menu.

Film and music disk mounting
----
To access the films on my server, we need to add this line to `/etc/fstab`:

```
192.168.1.172:/backup/backups/Filmdisk /films nfs rw 0 0
192.168.1.172:/backup/backups/Music /music nfs rw 0 0
```