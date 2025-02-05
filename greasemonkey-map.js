// ==UserScript==
// @name     Salontafel kaart
// @version  1
// @grant    none
// @require  http://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js
// @match    https://www.openstreetmap.org/*
// ==/UserScript==

//Only works if Firefox's about:config has dom.allow_scripts_to_close_windows is set to true.

$('<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><g stroke="#007FFF" stroke-width="5"><line x1="90" y1="5" x2="110" y2="5" /><line x1="80" y1="15" x2="120" y2="15" /><line x1="70" y1="25" x2="130" y2="25" /><line x1="60" y1="35" x2="140" y2="35" /><line x1="50" y1="45" x2="150" y2="45" /><line x1="40" y1="55" x2="160" y2="55" /><line x1="30" y1="65" x2="170" y2="65" /><line x1="20" y1="75" x2="180" y2="75" /><line x1="10" y1="85" x2="190" y2="85" /><line x1="0" y1="95" x2="200" y2="95" /><line x1="30" y1="105" x2="170" y2="105" /><line x1="30" y1="115" x2="170" y2="115" /><line x1="30" y1="125" x2="170" y2="125" /><line x1="30" y1="135" x2="170" y2="135" /><line x1="30" y1="145" x2="170" y2="145" /><line x1="30" y1="155" x2="80" y2="155" /><line x1="120" y1="155" x2="170" y2="155" /><line x1="30" y1="165" x2="80" y2="165" /><line x1="120" y1="165" x2="170" y2="165" /><line x1="30" y1="175" x2="80" y2="175" /><line x1="120" y1="175" x2="170" y2="175" /><line x1="30" y1="185" x2="80" y2="185" /><line x1="120" y1="185" x2="170" y2="185" /><line x1="30" y1="195" x2="80" y2="195" /><line x1="120" y1="195" x2="170" y2="195" /></g></svg>')
	.css("position", "absolute")
	.css("bottom", 0)
	.css("right", 0)
	.css("z", -4)
	.click(function() {
		window.close()
})
	.appendTo("#content");

$(".welcome").remove();
$("header").remove();
$("#content")
	.css("top", 0)
	.css("filter", "invert(100%)");
