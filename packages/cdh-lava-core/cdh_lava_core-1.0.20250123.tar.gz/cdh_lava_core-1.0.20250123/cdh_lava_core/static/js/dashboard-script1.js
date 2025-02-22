// General settings in relation to window size
const padding = 2;
const margin = { top: 10, right: 5, bottom: 10, left: 5 };
const width = d3.select(".chart").node().getBoundingClientRect().width;
const height = d3.select(".chart").node().getBoundingClientRect().width;

// From colorbrewer Dark2 + 2
var colour = d3.scaleOrdinal()
  .range(["#1b9e77", "#d95f02", "#6a3d9a", "#e7298a", "#66a61e", "#e6ab02", "#a6761d", "#666666", "#4682b4", "#ef2f32"]);

// Invisible tooltip to call in each chart
const tooltip = d3.select("body").append("div")
  .style("opacity", 0);

//Chart 1: Waffle chart coloured by category
var chartcolours = function (d3) {

  //Load in grants data
  d3.json("/static/js/dashboard-data1.json", function (data) {

    //Sort data by frequency of category (so squares appear ordered in relation to their category colour and frequency)
    data.sort(function (a, b) { return d3.descending(a.ThemeFreq, b.ThemeFreq); });

    grid = d3.select("#chart-colours")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .selectAll("rect")
      .data(data)
      .enter()
      .append("div")
      .attr("class", "block")
      .style("width", 8 + "px")
      .style("height", 8 + "px")
      .style("background-color", function (d) {
        return colour(d.Theme);
      })
      .on("mousemove", function (d) {
        d3.select(this)
          .style("opacity", 0.5);
        tooltip.transition()
          .duration(100)
          .style("opacity", .9)
          .attr("class", "tooltip")
          .style("left", (d3.event.pageX - 5) + "px")
          .style("top", (d3.event.pageY + 5) + "px");
        tooltip.html("<b>" + d.RecipientOrgName + "</b> (" + d.OrgType + ") received <b>" + d.AmountAwarded + "</b> pounds from <b>" + d.FundingOrgName +
                    "</b> in " + d.Year + " to fund a <b>" + d.Theme + "</b> programme. </br></br>" +
                    "Description of the '<b>" + d.Title + "' grant</b>: " + d.Description.substring(0, 380) + "...");
      })
      .on("mouseout", function (d) {
        d3.select(this)
          .style("opacity", 1);
        tooltip.transition()
          .duration(200)
          .style("opacity", 0);
      });

    // Set legend values
    legendValues = d3.set(data.map(function (d) { return d.Theme; })).values();

    // Add legend as if was a new chart
    var legend = d3.select(".legend")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("class", "legend-flex")
      .selectAll(".legends")
      .data(legendValues)
      .enter()
      .append("rect")
      .attr("class", "legends")
      .style("background-color", function (d) { return colour(d); })
      .append("text")
      .text(function (d, i) { return d; })
      .attr("class", "legend-text");

  });
}(d3);