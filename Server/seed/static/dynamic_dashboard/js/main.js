
var t;
var hist_labels = [];
    var plant_datasets = [];
function size(animate, data){
	if (animate == undefined){
		animate = false;
	}
	clearTimeout(t);
	t = setTimeout(function(){
		$("canvas").each(function(i,el){
			$(el).attr({
				"width":$(el).parent().width(),
				"height":$(el).parent().outerHeight()
			});
		});
		redraw(animate, data);
		var m = 0;
		$(".widget").height("");
		$(".widget").each(function(i,el){ m = Math.max(m,$(el).height()); });
		$(".widget").height(m);
	}, 30);
}

function redraw(animation, plant_data){
	var options = {};
	if (!animation){
		options.animation = false;
	} else {
		options.animation = true;
	}

	var data = [
		{
			value: 30,
			color:"#637b85"
		},
		{
			value : 30,
			color : "#2c9c69"
		},
		{
			value : 26,
			color : "#dbba34"
		},
		{
			value : 24,
			color : "#c62f29"
		}

	];
	var canvas = document.getElementById("hours");
	var ctx = canvas.getContext("2d");
	new Chart(ctx).Doughnut(data, options);

    var keys = Object.keys(plant_data);
    var plant = keys[0];

    // Create histogram datasets for each plant
    for (var i in keys)
    {
        // if it has datapoints
        if (plant_data[keys[i]].length)
        {

            plant_datasets[i] = [];
            for (var j in plant_data[keys[i]])
            {
                // histogram y labels
                var state = plant_data[keys[i]][j];
                plant_datasets[i].push(state['fields']['performance_value']);

                // histogram x labels
                if(hist_labels.length < plant_data[keys[i]].length)
                {
                    hist_labels.push(plant_data[plant][i]['fields']['timestep']);
                }
            }
        }
    }

	var data = {
		labels : hist_labels,
		datasets : [
			{
				fillColor : "rgba(99,123,133,0.4)",
				strokeColor : "rgba(220,220,220,1)",
				pointColor : "rgba(220,220,220,1)",
				pointStrokeColor : "#fff",
				data : plant_datasets[0]
			},
			{
				fillColor : "rgba(219,186,52,0.4)",
				strokeColor : "rgba(220,220,220,1)",
				pointColor : "rgba(220,220,220,1)",
				pointStrokeColor : "#fff",
				data : plant_datasets[1]
			},
		]
	}
	var canvas = document.getElementById("shipments");
	var ctx = canvas.getContext("2d");
	new Chart(ctx).Line(data, options);



	var data = {
		labels : ["Water","Nutrients","Light","Sound","Temperature","pH"],
		datasets : [
			{
				fillColor : "rgba(220,220,220,0.5)",
				strokeColor : "#637b85",
				pointColor : "#dbba34",
				pointStrokeColor : "#637b85",
				data : [95,87,90,25,67,40]
			}
		]
	}
	var canvas = document.getElementById("departments");
	var ctx = canvas.getContext("2d");
	new Chart(ctx).Radar(data, options);
}

