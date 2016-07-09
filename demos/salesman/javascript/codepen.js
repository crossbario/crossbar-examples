// from https://codepen.io/nicoptere/pen/Ejwpgq

var canvas = document.createElement( 'canvas' );
document.body.appendChild( canvas );
var w = canvas.width = window.innerWidth;
var h = canvas.height = window.innerHeight;
var ctx = canvas.getContext("2d");

///TSP
var TSP = function() {

    function TSP( vertices, temperature, coolingRate, maxIteration, ctx ){

        this.vertices = vertices;
        this.temperature = temperature||10;
        this.coolingRate = coolingRate||.5;
        maxIteration = maxIteration||5;

        this.count = vertices.length;

        this.order = vertices.map( function( o, i ){return i;});
        this.minimalorder = this.order.concat();
        this.pathlength = this.minimallength = this.length();

        var sameCount = 0, cycle = 0;
        var i2, j2, i1, j1, k1, k2, d;

        while (sameCount < maxIteration) {

            a = false;
            for (j2 = 0; j2 < this.count * this.count; j2++) {

                i1 = parseInt( this.count * Math.random());
                j1 = parseInt( this.count * Math.random());

                d = this.distance(i1, i1 + 1) + this.distance(j1, j1 + 1) - this.distance(i1, j1) - this.distance(i1 + 1, j1 + 1);

                if ( this.anneal(d) ) {
                    if (j1 < i1) {
                        k1 = i1;
                        i1 = j1;
                        j1 = k1;
                    }
                    var l = j1;
                    for (l = j1; l > i1; l--) {
                        i2 = this.order[i1 + 1];
                        this.order[i1 + 1] = this.order[l];
                        this.order[l] = i2;
                        i1++;
                    }
                }
            }

            this.pathlength = this.length();
            //console.log( a, this.pathlength );

            if ( this.pathlength < this.minimallength){

                this.minimallength = this.pathlength;

                for (k2 = 0; k2 < this.count; k2++){
                    this.minimalorder[k2] = this.order[k2];
                }
                sameCount = 0;
            }else{
                sameCount++;
            }

            this.temperature *= this.coolingRate;
            cycle++;
          if( ctx ) this.draw(ctx );
        }
        //console.log( this.length(), this.minimalorder )
    }

    //Called to determine if annealing should take place.
    function anneal(d) {
        if (this.temperature < 0.0 )return d > 0.0;
        return Math.random() < Math.exp( d / this.temperature );
    }

    function length() {
        var d = 0;
        for (var i = 1; i <= this.count; i++) {
            d += this.distance(i, i - 1);
        }
        return d;
    }

    function distance(i, j) {
        var p1 = this.vertices[this.order[i % this.count]];
        var p2 = this.vertices[this.order[j % this.count]];
        var dx = p1.x - p2.x;
        var dy = p1.y - p2.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    function getSortedArray() {
        var tmp  =[];
        for (var i = 0; i < this.count; i++){

            tmp.push( this.vertices[this.minimalorder[i]] );
        }
        return tmp;
    }

    function draw(ctx) {

        ctx.beginPath();
        ctx.moveTo(this.vertices[0].x, this.vertices[0].y);
        for (var i = 0; i < this.count; i++){
            var p0 = this.vertices[this.minimalorder[i]];
            ctx.lineTo(p0.x, p0.y);
        }
        ctx.closePath();
        ctx.stroke();

    }

    var _p = TSP.prototype;
    _p.anneal = anneal;
    _p.length = length;
    _p.distance = distance;
    _p.getSortedArray = getSortedArray;
    _p.draw = draw;

    return TSP;

}();
///////////////////////////////////////////

var Point = function( x, y){
  this.x = x||0;
  this.y = y||0;
};

var points = [];
var total = 200;
function reset(){
  ctx.clearRect(0,0,w,h);
  points = [];
  var i = total;
  while( i-- )
  {
    points.push( new Point( Math.random() * w, Math.random() * h ) );
  }
  ctx.strokeStyle = "#000000";
  ctx.globalAlpha = .05;
  var tsp = new TSP( points, 10, 0.95, 3, ctx  );

  ctx.strokeStyle = "#ff0000";
  ctx.lineWidth = 2;
  ctx.globalAlpha = 1;
  tsp.draw(ctx);
}
reset();
window.onmousedown = reset;
