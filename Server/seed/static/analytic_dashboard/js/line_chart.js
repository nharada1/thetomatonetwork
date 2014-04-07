var lineChart = function() {
    var self = {};

    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        containerWidth = $("#left_panel").width() - 100,
        containerHeight = 400,
        lineChart_width = containerWidth - margin.left - margin.right,
        lineChart_height = containerHeight - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y-%-m-%-d").parse;

    var x = d3.time.scale()
        .range([0, lineChart_width]);

    var y = d3.scale.linear()
        .range([lineChart_height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var line_color = d3.scale.category10();

    var line_color = d3.scale.ordinal()
        .range(['#666','#00CC66','#FF6600','#CC0000','#006600']);

    var area = d3.svg.area()
        .interpolate('basis')
        .x(function(d) { return x(d.date); })
        .y0(lineChart_height)
        .y1(function(d) { return y(d.performance); })

    var areaStart = d3.svg.area()
        .interpolate('basis')
        .x(function(d) { return x(d.date); })
        .y0(lineChart_height)
        .y1(function(d) { return y(0); })

    var line = d3.svg.line()
        .interpolate('basis')
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.performance); });

    var lineStart = d3.svg.line()
        .interpolate('basis')
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(0);      });

    var svg = d3.select("#line_chart").append("svg")
        .attr("width", lineChart_width + margin.left + margin.right)
        .attr("height", lineChart_height + margin.top + margin.bottom)
        .attr("perserveAspectRatio", "xMinYMid")
        .attr("viewBox", "0 0 " + containerWidth + " " + containerHeight)
        .attr("id", "line_svg")
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    var legend = d3.select('#legend')
        .append('ul')
        .attr('class', 'list-inline');

    self.render = function() {    
        d3.csv('csv', function(error, data) {
            line_color.domain(d3.keys(data[0]).filter(function(key) { return (key !== "Date" || key !== "timestep"); }));
            data.forEach(function(d) {
                d.date = parseDate(d.Date);
            });
            var plants = line_color.domain().map(function(name) {
                return {
                    name: name,
                    values: data.map(function(d) {
                        return {date: d.date, performance: +d[name]}
                    })
                }
            });
            
            x.domain(d3.extent(data, function(d) { return d.date; }));
            y.domain([
                d3.min(plants, function(c) { return d3.min(c.values, function(v) { return v.performance; }); }),
                d3.max(plants, function(c) { return d3.max(c.values, function(v) { return v.performance; }); })
            ]);

            var keys = legend.selectAll('li.key')
                .data(plants);

            keys.enter().append('li')
                .attr('class', 'key');

            keys.append('a')
                .style('border-color', function(d) { return line_color(d.name) })
                .attr('href', function(d) {
                    return "javascript: lineChart.onLineChange(\'" + d.name.replace(/\s/g, '_') + "\');";
                })
                .attr("class", function(d) { return d.name.replace(/\s/g, '_'); })
                .text(function(d) {
                    return d.name;
                });

            var plant = svg.selectAll(".plant")
                .data(plants)
              .enter().append("g")
                .attr("class", "plant");
                    
            plant.append("path")
                .attr("class", "line_chart_line")
                .style("stroke", function(d) { return line_color(d.name) })
                .attr("d", function(d) {return lineStart(d.values); })
              .transition().delay(function(d, i) { return i * 100; }).duration(300)
                .attr("d", function(d) { return line(d.values); });
                
            plant.append("path")
                .attr("class", function(d) { return "line_area " + d.name.replace(/\s/g, '_'); })
                .style("fill", function(d) { return line_color(d.name) })
                .style("fill-opacity", "0.15")
                .attr("d", function(d) { return areaStart(d.values); })
              .transition().delay(function(d, i) { return i * 100; }).duration(300)
                .attr("d", function(d) { return area(d.values); });
              
            svg.append("g")
                .attr("class", "line_chart_x line_chart_axis")
                .attr("transform", "translate(0," + lineChart_height + ")")
                .call(xAxis);

            svg.append("g")
                .attr("class", "line_chart_y line_chart_axis")
                .call(yAxis)
              .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", ".71em")
                .style("text-anchor", "end")
                .text("Performance");

            var startPlant = "control";

            svg.selectAll(".line_area")
                .style("fill-opacity", "0.0");

            svg.selectAll("." + startPlant)
                .style("fill-opacity", "0.6");

            legend.selectAll("li.key a")
                .style("color", "#333")
                .style("background-color", "#efefef");

            legend.selectAll("a." + startPlant)
                .style("color", "#FFF")
                .style("background-color", function(d) { return line_color(startPlant.replace(/_/g, ' ')) });

        });
    
        /*** Resize Triggers ***/
        var linegraph = $("#line_svg"),
            aspect = linegraph.width() / linegraph.height(),
            container = linegraph.parent();
            
        $(window).on("resize", function() {
            var targetWidth = container.width();
            linegraph.attr("width", targetWidth);
            linegraph.attr("height", Math.round(targetWidth / aspect));
        }).trigger("resize");

    }, 

    self.onLineChange = function(name) {
        svg.selectAll(".line_area")
            .style("fill-opacity", "0.0");

        svg.selectAll("." + name)
            .transition()
            .style("fill-opacity", "0.6");

        legend.selectAll("li.key a")
            .style("color", "#333")
            .style("background-color", "#efefef");

        legend.selectAll("a." + name)
            .transition()
            .style("color", "#FFF")
            .style("background-color", function(d) { return line_color(name.replace(/_/g, ' ')) });
        }

    return self;
}();