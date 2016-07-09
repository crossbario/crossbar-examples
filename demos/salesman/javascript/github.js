// from https://raw.githubusercontent.com/abdulfatir/SimulatedAnnealing-TSP/master/scripts/anneal.js

var temprature = 0.1;
var ABSOLUTE_ZERO = 1e-4;
var COOLING_RATE = 0.999999;
var CITIES = 50;
var current = [];
var best = [];
var best_cost = 0;

$(document).ready(function()
	{
		$("#solve").click(function()
			{
				temperature = parseFloat($("#temperature").val());
				ABSOLUTE_ZERO = parseFloat($("#abszero").val());
				COOLING_RATE = parseFloat($("#coolrate").val());
				CITIES = parseInt($("#cities").val());
				init();
			});
	});

var tsp_canvas = document.getElementById('tsp-canvas');
var tsp_ctx = tsp_canvas.getContext("2d");

//init();

function randomFloat(n)
{
	return (Math.random()*n);
}

function randomInt(n)
{
	return Math.floor(Math.random()*(n));
}

function randomInteger(a,b)
{
	return Math.floor(Math.random()*(b-a)+a);
}

function deep_copy(array, to)
{
	var i = array.length;
	while(i--)
	{
		to[i] = [array[i][0],array[i][1]];
	}
}

function getCost(route)
{
	var cost = 0;
	for(var i=0; i< CITIES-1;i++)
	{
		cost = cost + getDistance(route[i], route[i+1]);
	}
	cost = cost + getDistance(route[0],route[CITIES-1]);
	return cost;
}

function getDistance(p1, p2)
{
	del_x = p1[0] - p2[0];
	del_y = p1[1] - p2[1];
	return Math.sqrt((del_x*del_x) + (del_y*del_y));
}

function mutate2Opt(route, i, j)
{
	var neighbor = [];
	deep_copy(route, neighbor);
	while(i != j)
	{
		var t = neighbor[j];
		neighbor[j] = neighbor[i];
		neighbor[i] = t;

		i = (i+1) % CITIES;
		if (i == j)
			break;
		j = (j-1+CITIES) % CITIES;
	}
	return neighbor;
}

function acceptanceProbability(current_cost, neighbor_cost)
{
	if(neighbor_cost < current_cost)
		return 1;
	return Math.exp((current_cost - neighbor_cost)/temperature);
}

function init()
{
	for(var i=0;i<CITIES;i++)
	{
		current[i] = [randomInteger(10,tsp_canvas.width-10),randomInteger(10,tsp_canvas.height-10)];
	}

	deep_copy(current, best);
	best_cost = getCost(best);
	setInterval(solve, 10);
}

function solve()
{
	if(temperature>ABSOLUTE_ZERO)
	{
		var current_cost = getCost(current);
		var k = randomInt(CITIES);
		var l = (k+1+ randomInt(CITIES - 2)) % CITIES;
		if(k > l)
		{
			var tmp = k;
			k = l;
			l = tmp;
		}
		var neighbor = mutate2Opt(current, k, l);
		var neighbor_cost = getCost(neighbor);
		if(Math.random() < acceptanceProbability(current_cost, neighbor_cost))
		{
			deep_copy(neighbor, current);
			current_cost = getCost(current);
		}
		if(current_cost < best_cost)
		{
			deep_copy(current, best);
			best_cost = current_cost;
			paint();
		}
		temperature *= COOLING_RATE;
	}
}

function paint()
{
	tsp_ctx.clearRect(0,0, tsp_canvas.width, tsp_canvas.height);
	// Cities
	for(var i=0; i<CITIES; i++)
	{
		tsp_ctx.beginPath();
		tsp_ctx.arc(best[i][0], best[i][1], 4, 0, 2*Math.PI);
		tsp_ctx.fillStyle = "#0000ff";
		tsp_ctx.strokeStyle = "#000";
		tsp_ctx.closePath();
		tsp_ctx.fill();
		tsp_ctx.lineWidth=1;
		tsp_ctx.stroke();
	}
	// Links
	tsp_ctx.strokeStyle = "#ff0000";
	tsp_ctx.lineWidth=2;
	tsp_ctx.moveTo(best[0][0], best[0][1]);
	for(var i=0; i<CITIES-1; i++)
	{
		tsp_ctx.lineTo(best[i+1][0], best[i+1][1]);
	}
	tsp_ctx.lineTo(best[0][0], best[0][1]);
	tsp_ctx.stroke();
	tsp_ctx.closePath();
}
