var smallCalendar = function() {
    var width = 176,
        height = 960,
        cellSize = 17; // cell size

    var day = d3.time.format("%w"),
        week = d3.time.format("%U"),
        percent = d3.format(".1%"),
        format = d3.time.format("%Y-%-m-%-d");

    var color = d3.scale.quantize()
        .domain([0, 100])
        .range(d3.range(11).map(function(d) { return "q" + d + "-11"; }));

    var svg = d3.select("#small_calendar").selectAll("svg")
        .data(d3.range(2013, 2015))
      .enter().append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("class", "RdYlGn")
      .append("g")
        .attr("transform", "translate(" + ((height - cellSize * 53) / 2) + "," + (width - cellSize * 7 - 1) + ")");

    var rect = svg.selectAll(".day")
        .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
      .enter().append("rect")
        .attr("class", "day")
        .attr("width", cellSize)
        .attr("height", cellSize)
        .attr("y", function(d) { return week(d) * cellSize; })
        .attr("x", function(d) { return day(d) * cellSize; })
        .datum(format);


    function monthPath(t0) {
      var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
          d0 = +day(t0), w0 = +week(t0),
          d1 = +day(t1), w1 = +week(t1);
      return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
          + "H" + w0 * cellSize + "V" + 7 * cellSize
          + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
          + "H" + (w1 + 1) * cellSize + "V" + 0
          + "H" + (w0 + 1) * cellSize + "Z";
    }
    
    return {
        render: function() {
            svg.append("text")
                .attr("transform", "translate(" + cellSize * 3.5 + ",-6)")
                .style("text-anchor", "middle")
                .text(function(d) { return d; });
                
            rect.append("title")
                .text(function(d) { return d; });

            svg.selectAll(".month")
                .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
              .enter().append("path")
                .attr("class", "month")
                .attr("d", monthPath)
                .attr("transform", "rotate(90)scale(1,-1)");

            d3.csv('csv', function(error, csv) {
                var scale = d3.scale.ordinal()
                    .domain(d3.keys(csv[0]).filter(function(key) { return (key !== "Date" && key !== "timestep"); }));
                var data = d3.nest()
                    .key(function(d) { return d.Date; })
                    .rollup(function(d) { 
                        perVals = scale.domain().map(function(name) {
                            return d[0][name];                            
                        });
                        return d3.sum(perVals);
                    }).map(csv);

                color.domain(d3.extent(d3.values(data)));

                rect.filter(function(d) { return d in data; })
                    .attr("class", function(d) { return "day " + color(data[d]); })
                  .select("title")
                    .text(function(d) { return d + ": " + percent(data[d]); });
            });

            d3.select(self.frameElement).style("height", "2910px");
        }
    }
}();