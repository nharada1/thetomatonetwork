var t;
var histogram_formats = [
            {
				fillColor : "rgba(99,123,133,0.4)",
				strokeColor : "rgba(220,220,220,1)",
				pointColor : "rgba(220,220,220,1)",
				pointStrokeColor : "#fff",
                name : "",
				data : []
			},
    	    {
				fillColor : "rgba(219,186,52,0.4)",
				strokeColor : "rgba(220,220,220,1)",
				pointColor : "rgba(220,220,220,1)",
				pointStrokeColor : "#fff",
                name : "",
				data :[]
            },
        	{
				fillColor : "rgba(239,146,34,0.4)",
				strokeColor : "rgba(220,220,220,1)",
				pointColor : "rgba(220,220,220,1)",
				pointStrokeColor : "#fff",
                name : "",
				data :[]
			},
            {
				fillColor : "rgba(45,98,234,0.4)",
				strokeColor : "rgba(220,220,220,1)",
				pointColor : "rgba(220,220,220,1)",
				pointStrokeColor : "#fff",
                name : "",
				data :[]
			}
];
function size(animate, hist_data){
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
		redraw(animate, hist_data);
		var m = 0;
		$(".widget").height("");
		$(".widget").each(function(i,el){ m = Math.max(m,$(el).height()); });
		$(".widget").height(m);
	}, 30);
}

function redraw(animation, hist_data){
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

    // graph hist data
    var data = hist_data;
	var canvas = document.getElementById("plant_health");
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

function collateHistData(raw_plant_data){
        // Assemble plot data
    var keys = Object.keys(raw_plant_data);
    var hist_labels = [];
    var plant_datasets = [];

    // Create histogram datasets for each plant
    for (var i in keys)
    {
        // if it has datapoints
        if (raw_plant_data[keys[i]].length)
        {
            // map to different histogram color schemes
            // parse - stringify is the fastest deep copy for simple json objects
            var plant_data_object = JSON.parse(JSON.stringify(histogram_formats[i % histogram_formats.length]));

            plant_data_object['name'] = keys[i];
            for (var j in raw_plant_data[keys[i]])
            {
                // histogram y labels
                var state = raw_plant_data[keys[i]][j];
                plant_data_object['data'].push(state['fields']['performance_value']);

                // histogram x labels
                if(hist_labels.length < raw_plant_data[keys[i]].length)
                {
                    hist_labels.push(raw_plant_data[keys[i]][j]['fields']['timestep']);
                }
            }
            plant_datasets.push(plant_data_object);
        }
    }

    // create histogram data
	var data = {
		labels : hist_labels,
		datasets : plant_datasets
	}
    return data;
}

function loadPage(hist_data){

    // construct histogram legend
    generateHistLegend(hist_data);

    // render
    size(true, hist_data);
}

function generateHistLegend(hist_data){
    var html_str = "";
    var plant_datasets = hist_data['datasets'];

    // Add plant name to inner html
    for (var i in plant_datasets)
    {
         html_str += '<span id="' + 'hist_legend_' + i + '"> ' + plant_datasets[i]['name'] + ' </span>';
    }
    document.getElementById('hist_legend').innerHTML = html_str;

    // Select each plant by id and edit its color
    for (var i in plant_datasets)
    {
         document.getElementById('hist_legend_'+i).style.color = plant_datasets[i]['fillColor'];
    }
}
