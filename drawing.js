
var canvas = null;
var context = null;
var mapSprite = null;

function startDraw() {
    canvas = document.getElementById('Canvas');
    canvas.width = WIDTH_D;
    canvas.height = HEIGHT_D;
    context = canvas.getContext("2d");

    // Map sprite
    mapSprite = new Image();
    mapSprite.src = "./"+FILENAME;
    firstLoad();
    canvas.addEventListener("mousedown", mouseClicked, false);
    setInterval(main, (1000 / 60));
    }

var Marker = function () {
    this.Sprite = new Image();
    this.Sprite.src = "http://www.clker.com/cliparts/w/O/e/P/x/i/map-marker-hi.png"
    this.Width = 12;
    this.Height = 20;
    this.XPos = 0;
    this.YPos = 0;
    this.TextXPos = 0;
    this.TextYPos = 0;
    this.markerText = "MARKER";
}

var Markers = new Array();
Markers.push(new Marker());
Markers.push(new Marker());
Markers[0].XPos = -25;
Markers[0].YPos = -25;
Markers[1].XPos = -25;
Markers[1].YPos = -25;

var mouseXPos = 0;
var mouseYPos = 0;

var mouseClicked = function (mouse) {
    // Get current mouse coords
    var rect = canvas.getBoundingClientRect();
    mouseXPos = (mouse.x - rect.left);
    mouseYPos = (mouse.y - rect.top);

    console.log("Marker added");

    // Move the marker when placed to a better location
    var marker = new Marker();
    marker.XPos = mouseXPos - (marker.Width / 2);
    marker.YPos = mouseYPos - marker.Height;
    marker.TextXPos = mouseXPos;
    marker.TextYPos = mouseYPos;

    if (modeStart) {
        marker.markerText = "START";
        Markers[0] = marker;
    } else {
        marker.markerText = "END";
        Markers[1] = marker;
    }
    calculate(mouseXPos, mouseYPos);
}

// Add mouse click event listener to canvas

var firstLoad = function () {
    context.font = "15px Georgia";
    context.textAlign = "center";
}



var main = function () {
    draw();
};

var draw = function () {
    // Clear Canvas
    context.fillStyle = "#000";
    context.fillRect(0, 0, canvas.width, canvas.height);

    // Draw map
    // Sprite, X location, Y location, Image width, Image height
    // You can leave the image height and width off, if you do it will draw the image at default size
    context.drawImage(mapSprite, 0, 0, WIDTH_D, HEIGHT_D);

    // Draw markers
    for (var i = 0; i < Markers.length; i++) {
        var tempMarker = Markers[i];
        // Draw marker
        context.drawImage(tempMarker.Sprite, tempMarker.XPos, tempMarker.YPos, tempMarker.Width, tempMarker.Height);
        markerText = tempMarker.markerText;

        // Calculate postion text
        //var markerText = "Position (X:" + tempMarker.TextXPos + ", Y:" + tempMarker.TextYPos + ")";

        // Draw a simple box so you can see the position
        var textMeasurements = context.measureText(markerText);
        context.fillStyle = "#666";
        context.globalAlpha = 0.7;
        context.fillRect(tempMarker.XPos - (textMeasurements.width / 2), tempMarker.YPos - 15, textMeasurements.width, 20);
        context.globalAlpha = 1;

        // Draw position above
        context.fillStyle = "#000";
        context.fillText(markerText, tempMarker.XPos, tempMarker.YPos);
    }
};
