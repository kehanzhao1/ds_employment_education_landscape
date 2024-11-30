<script>
  import * as d3 from "d3";
  import { onMount } from "svelte";


  let svgWidth = 850;
  let svgHeight = 500;
  let margin = { top: 20, right: 50, bottom: 40, left: 150 };
  let width = svgWidth - margin.left - margin.right;
  let height = svgHeight - margin.top - margin.bottom;

  let datasets = {}; // Object to store both datasets
  let currentDataset = "hardSkills"; // Track which dataset is active
  let chartData = []; // Data for the current chart
  let svgRef;

  // Load data on mount
  onMount(async () => {
    const skillsData = await d3.csv("skills_counts_clean.csv");
    const softSkillsData = await d3.csv("soft_skills_counts.csv");

    datasets = {
      hardSkills: processData(skillsData),
      softSkills: processData(softSkillsData),
    };
      // Set the initial chart data
    drawChart(datasets[currentDataset],"steelblue");
  });

  // Process the data
  const processData = (data) =>
    data
      .map((d) => ({
        skill: d.skill,
        count: +d.count,
      }))
      .sort((a, b) => b.count - a.count);

  const drawChart = (data, barColor) => {
    
     // Clear the SVG
     const svg = d3.select(svgRef);
    svg.selectAll("*").remove();

    // Define the inner dimensions of the chart
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // Create the chart group
    const chartGroup = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);
    
      // Scales
    const xScale = d3
      .scaleLinear()
      .domain([0, d3.max(data, (d) => d.count)])
      .range([0, innerWidth]);

    const yScale = d3
      .scaleBand()
      .domain(data.map((d) => d.skill))
      .range([0, innerHeight])
      .padding(0.4);

    // Axes
    const yAxis = chartGroup
      .append("g")
      .attr("class", "y-axis")
      .call(d3.axisLeft(yScale)).selectAll("text")
      .style("font-size", "20px")
      .style('font-family','Lato') // Increase skill axis label size
      .style("fill", "grey"); // Set axis text color to grey

     yAxis
     .selectAll("text")
     .style("text-anchor", "end") // Align end for better readability
     .attr("dx", "-0.8em") // Offset horizontally
     .attr("dy", "0.15em") // Offset vertically
     .attr("transform", "rotate(-45)") // Rotate text

    chartGroup
      .append("g")
      .attr("class", "x-axis")
      .attr("transform", `translate(0, ${innerHeight})`)
      .call(d3.axisBottom(xScale).ticks(5))
      .selectAll("text")
      .style("fill", "grey")
      .style("font-size", "16px")
      .style('font-family','Lato');

    // Bars
    chartGroup
      .selectAll(".bar")
      .data(data)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .attr("y", (d) => yScale(d.skill))
      .attr("x", 0)
      .attr("height", yScale.bandwidth())
      .attr("width", (d) => xScale(d.count))
      .style("fill", barColor); 

      svg
      .append("image")
      .attr("xlink:href",currentDataset == "hardSkills" ? "/hardskill.png": "softskill.png") // Replace with your image URL
      .attr("x", width - margin.right - 150) // Position near the right side
      .attr("y", height / 2 + 3) // Center vertically
      .attr("width", 200) // Set image width
      .attr("height", 200); // Set image height
  };
  const switchDataset = (dataset) => {
    currentDataset = dataset;
    const barColor = dataset === "hardSkills" ? "steelblue" : "darkseagreen";
    drawChart(datasets[dataset], barColor);
  };
</script>

<style>
  .buttons {
    display: flex;
    gap: 40px;
    margin-bottom: 20px;
    margin-top:60px ;
  }

  button {
    padding: 10px 15px;
    font-size: 16px;
    cursor: pointer;
    background-color: #e8e2e2;
    color: white;
    border: none;
    border-radius: 5px;
    font-family: Lato, sans-serif;
    font-size: 18px;
  }

  button.active {
    background-color: #cf5029b7;
  }

  .bar:hover {
    fill: orange;
  }
  svg {
    overflow: visible; /* Allow overflow of content beyond the SVG container */
  }
  .x-axis path,
  .y-axis path,
  .x-axis line,
  .y-axis line {
    stroke: grey; /* Set axis line color to grey */
  }

</style>

<main>
  <div class="buttons">
    <button
      class="{currentDataset === 'hardSkills' ? 'active' : ''}"
      on:click={() => switchDataset("hardSkills")}
    >
      Hard Skills
    </button>
    <button
      class="{currentDataset === 'softSkills' ? 'active' : ''}"
      on:click={() => switchDataset("softSkills")}
    >
      Soft Skills
    </button>
  </div>
  <svg bind:this={svgRef} width={width} height={height}></svg>
</main>