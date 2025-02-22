/* reference article 
https://www.williamrchase.com/writing/2019-10-13-animated-waffle-charts-with-d3-and-gsap
*/

document.addEventListener("DOMContentLoaded", function () {
  const btnPlay = document.getElementById("btnPlay");
  const btnReverse = document.getElementById("btnReverse");

  fetch("./js/dashboard-data.json")
    .then(response => response.json())
    .then(rawData => {
      // Since the data is nested under "recipes", we extract it
      let data = rawData.recipes;

      // Sort data by role
      data.sort((a, b) => a.role.localeCompare(b.role));

      // Setup colors, mapping each unique role to a color
      const roles = [...new Set(data.map(d => d.role))]; // Get unique roles
      const scaleColor = d3.scaleOrdinal()
        .domain(roles)
        .range(["#FF8E79", "#FF6B5B", "#FF4941", "#DB1D25"]);

      // Select the chart container
      const graph = d3.select(".chart");

      // Create a container for each recipe
      const boxes = graph.selectAll(".box")
        .data(data)
        .join("div")
        .attr("class", "box")
        .style("background-color", d => scaleColor(d.role))
        .attr("title", d => d.recipe); // Set the title attribute for mouseover text

      // Initiate paused animation
      let anim = gsap.timeline({ paused: true });
      anim.to(".box", {
        duration: 1,
        scale: 1,
        ease: "back.out(1.7)",
        stagger: {
          grid: "auto",
          from: "start",
          axis: "y",
          amount: 0.5
        }
      });

      // Play animation
      btnPlay.addEventListener("click", function (e) {
        e.preventDefault();
        if (!anim.isActive()) {
          anim.play();
        }
      });

      // Reverse animation
      btnReverse.addEventListener("click", function (e) {
        e.preventDefault();
        anim.reverse();
      });
    })
    .catch(error => console.error("Error loading the data:", error));
});
