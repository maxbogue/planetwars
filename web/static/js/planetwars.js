var FPS = 30;

var PLAYER_COLORS = [
    ["#CCCCCC", "#666666"],
    ["#CCFF00", "#99BF00"],
    ["#00CCFF", "#0099BF"],
    ["#FF00CC", "#BF0099"],
    ["#FFCC00", "#BF9900"],
    ["#00FFCC", "#00BF99"],
    ["#CC00FF", "#9900BF"],
];

var planetLocs = null;

function dist(p1, p2) {
    var dx = p2.x - p1.x;
    var dy = p2.y - p1.y;
    return Math.sqrt(dx * dx + dy * dy);
}

function planetRadius(ctx, planet) {
    return Math.ceil((14 + planet.growth * 4) * (ctx.canvas.width / 800));
}

function fleetRadius(ctx, fleet) {
    return Math.ceil((10 + fleet.ships * 0.25) * (ctx.canvas.width / 800));
}

function planetFontSize(ctx, planet) {
    return Math.ceil((14 + planet.growth * 3) * (ctx.canvas.width / 800));
}

function fleetFontSize(ctx, fleet) {
    return Math.ceil((8 + fleet.ships * 0.1) * (ctx.canvas.width / 800));
}

function makePlanetLocs(ctx, planets) {
    planetLocs = [];
    var top = Infinity,
        left = Infinity,
        right = -Infinity,
        bottom = -Infinity;
    for (var i = 0; i < planets.length; i++) {
        var p = planets[i];
        if (p.x < left) left = p.x;
        if (p.x > right) right = p.x;
        if (p.y < top) top = p.y;
        if (p.y > bottom) bottom = p.y;
    }
    var xRange = right - left,
        yRange = bottom - top,
        paddingFactor = 0.1;
    left -= xRange * paddingFactor;
    right += xRange * paddingFactor;
    top -= yRange * paddingFactor;
    bottom += yRange * paddingFactor;
    var width = ctx.canvas.width;
    var height = Math.floor(width * yRange / xRange);
    ctx.canvas.height = height;
    for (var i = 0; i < planets.length; i++) {
        var p = planets[i];
        var x = Math.floor((p.x - left) / (right - left) * width);
        var y = height - Math.floor((p.y - top) / (bottom - top) * height);
        planetLocs.push({
            "x": x,
            "y": y,
            "growth": p.growth,
            "radius": planetRadius(ctx, p),
        });
    }
}

function drawTriangle(ctx, x, y, r, theta) {
    var A = Math.PI * 2 / 3;
    var x1 = x + 1.5 * r * Math.cos(theta),
        y1 = y + 1.5 * r * Math.sin(theta),
        x2 = x + r * Math.cos(theta + A),
        y2 = y + r * Math.sin(theta + A),
        x3 = x + r * Math.cos(theta - A),
        y3 = y + r * Math.sin(theta - A);
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.lineTo(x3, y3);
    ctx.lineTo(x1, y1);
    ctx.closePath();
}

function drawPlanet(ctx, planet) {
    var p = planetLocs[planet.id];
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2, false);
    ctx.closePath();
    ctx.fillStyle = PLAYER_COLORS[planet.owner][0];
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = PLAYER_COLORS[planet.owner][1];
    ctx.stroke();
    ctx.font = planetFontSize(ctx, planet) + "px Helvetica";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = "#000000";
    ctx.fillText(Math.floor(planet.ships), p.x, p.y);
}

function drawFleet(ctx, fleet) {
    var source = planetLocs[fleet.source];
    var destination = planetLocs[fleet.destination];
    var d = dist(source, destination) - source.radius - destination.radius;
    var traveled = source.radius + d * (1 - (fleet.remaining_turns) / (fleet.total_turns - 1));
    var theta = Math.atan2(destination.y - source.y, destination.x - source.x);
    var x = source.x + Math.cos(theta) * traveled;
    var y = source.y + Math.sin(theta) * traveled;
    var r = fleetRadius(ctx, fleet);
    if (r > 30) r = 30;
    drawTriangle(ctx, x, y, r, theta);
    ctx.fillStyle = "#000000";
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = PLAYER_COLORS[fleet.owner][0];
    ctx.stroke();
    ctx.font = fleetFontSize(ctx, fleet) + "px Helvetica";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = "#FFFFFF";
    var fx = x + 0.1 * r * Math.cos(theta),
        fy = y + 0.1 * r * Math.sin(theta);
    ctx.fillText(Math.floor(fleet.ships), fx, fy);
}

function drawGame(ctx, planets, fleets) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    for (var i = 0; i < planets.length; i++) {
        drawPlanet(ctx, planets[i]);
    }
    for (var i = 0; i < fleets.length; i++) {
        drawFleet(ctx, fleets[i]);
    }
}

function PlanetWars(ctx, tps) {
    this.ctx = ctx;
    // turns per second
    this.tps = tps;
    // frames per turn
    this.fpt = Math.ceil(FPS / tps);
    // turns per frame
    this.tpf = 1.0 / this.fpt;
    // frames per second (real)
    this.fps = this.fpt * tps;
    // milliseconds per frame
    this.mspf = 1000 / this.fps;
    this.planets = [];
    this.fleets = [];
    this.queue = [];
    this.interpolatedFrames = 0;
    this.nextFrameAt = 0;
    this.interpolate = true;
}

PlanetWars.prototype.addData = function(data) {
    this.queue.push(data);
    if (!this.nextFrameAt && this.queue.length / this.tps > 1.0) {
        this.nextFrameAt = Date.now();
        this.renderFrame();
    }
}

PlanetWars.prototype.renderFrame = function() {
    console.log(this.queue.length);
    if (this.interpolatedFrames % this.fpt == 0) {
        var data = this.queue.shift();
        this.planets = data[0];
        this.fleets = data[1];
    } else if (this.interpolate) {
        for (var i = 0; i < this.planets.length; i++) {
            if (this.planets[i].owner > 0) {
                this.planets[i].ships += this.planets[i].growth * this.tpf;
            }
        }
        for (var i = 0; i < this.fleets.length; i++) {
            this.fleets[i].remaining_turns -= this.tpf;
        }
    }
    this.interpolatedFrames++;
    drawGame(this.ctx, this.planets, this.fleets);
    if (this.queue.length > 0) {
        this.nextFrameAt += this.mspf;
        var that = this;
        setTimeout(function() {
            that.renderFrame();
        }, this.nextFrameAt - Date.now());
    }
}
