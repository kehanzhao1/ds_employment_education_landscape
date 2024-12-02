<script>
    import * as d3 from 'd3';
    import {onMount} from 'svelte';

    const jobskillsPath = '/counts.csv';
    const margin = {top: 50, right: 50, bottom: 120, left: 120};
    const width = 600
    const height = 400;
    const chartW = width - margin.left - margin.right;
    const chartH = height - margin.top - margin.bottom;
    let data = [];

    onMount(async () => {
        data = await d3.csv(jobskillsPath, d => ({
            skill: d.skill,
            cc_count: +d.cc_count,
            job_count: +d.job_count
        }));
        initialRender();
    })

    let xScale;
    let xAxis;
    let yScale;
    let yAxis;
    let marks;

    function initialRender() {
        data.sort((a, b) => b.cc_count - a.cc_count); // change

      xScale = d3.scaleBand()
        .range([0, chartW])
        .padding(0.1)
        .domain(data.map(d => d.skill));

      d3.select(xAxis)
        .call(d3.axisBottom(xScale));
      d3.select(xAxis)
        .selectAll(".tick text")
        .style("fill", "black")
        .attr("transform", `translate(6, 1)rotate(45)`)
        .attr("text-anchor", "start");
      d3.select(xAxis)
        .append("text")
        .style("font-family", "sans-serif")
        .style("font-size", "11px")
        .style("font-weight", "bold")
        .style("fill", "black")
        .style("transform", `translate(${chartW / 2}px, ${90}px)`)
        .text("Skill");

      yScale = d3.scaleLinear()
        .range([chartH, 0])
        .domain([0, d3.max(data, (d) => d.cc_count)]);

      d3.select(yAxis)
        .call(d3.axisLeft(yScale)
        .ticks(4, ".1f"));
      d3.select(yAxis)
        .selectAll(".tick text")
        .style("fill", "black")
      d3.select(yAxis)
        .append("text")
        .attr("class", "title")
        .style("font-family", "sans-serif")
        .style("font-size", "11px")
        .style("font-weight", "bold")
        .style("fill", "black")
        .style("text-anchor", "middle")
        .style("transform", `translate(${-margin.left / 2}px, ${chartH / 2}px) rotate(-90deg)`)
        .text("Community College Count"); // change

      d3.select(marks)
        .selectAll("rect")
        .data(data, (d) => d.skill).enter()
        .append("rect")
        .style("fill", "#feb388")
        .attr("x", (d) => xScale(d.skill)) // change
        .attr("width", (d) => xScale.bandwidth())
        .attr("y", (d) => yScale(d.cc_count)) // change
        .attr("height", (d) => yScale(0) - yScale(d.cc_count)); // change
  }

  function update2jr() {
    // resort data based on jr_count
    data.sort((a,b) => b.cc_count - a.cc_count);

    // update array used to ser x-axis domain to reflect new order
    xScale.domain(data.map(d => d.skill));

    // change y-axis scale to represent jr_count
    yScale.domain([0, d3.max(data, (d) => d.cc_count)]);

    // update y-axis scale
    d3.select(yAxis)
      .transition()
      .duration(750)
      .delay(500)
      .call(d3.axisLeft(yScale)
      .ticks(4, ".1f"))
      .on("end", () => {
        // change y-axis title
    d3.select(yAxis)
      .select(".title")
      .text("Community College Count");
      });
    d3.select(yAxis)
      .selectAll(".tick text")
      .style("fill", "black")

    // update data mapping for bars
    d3.select(marks)
      .selectAll("rect")
      .transition()
      .duration(750)
      .delay(500)
      .attr("y", d => yScale(d.cc_count))
      .attr("height", d => yScale(0) - yScale(d.cc_count))
      // transition x order after bar height
      .transition()
      .duration(750)
      // .delay((d, i) => i * 50)
      .attr("x", (d) => xScale(d.skill));

    // update x-axis labels
    d3.select(xAxis)
      // .selectAll(".tick")
      // .data(data)
      .transition()
      .duration(750)
      .delay(1250)
      .call(d3.axisBottom(xScale));
      // .delay((d, i) => 1250 + i * 50)
      // .attr("transform", (d) => `translate(${xScale(d.title)}px, 0px)`);
  }

  function update() {
    // resort data based on sr_count
    data.sort((a,b) => b.job_count - a.job_count);

    // update array used to ser x-axis domain to reflect new order
    xScale.domain(data.map(d => d.skill));

    // change y-axis scale to represent sr_count
    yScale.domain([0, d3.max(data, (d) => d.job_count)]);

    // update y-axis scale
    d3.select(yAxis)
      .transition()
      .duration(750)
      .delay(500)
      .call(d3.axisLeft(yScale)
      .ticks(4, ".1f"))
      .on("end", () => {
        // change y-axis title
        d3.select(yAxis)
          .select(".title")
          .text("Job Positions Count");
      });
    d3.select(yAxis)
      .selectAll(".tick text")
      .style("fill", "black")

    // update data mapping for bars
    d3.select(marks)
      .selectAll("rect")
      .transition()
      .duration(750)
      .delay(500)
      .attr("y", d => yScale(d.job_count))
      .attr("height", d => yScale(0) - yScale(d.job_count))
      // transition x order after bar height
      .transition()
      .duration(750)
      // .delay((d, i) => i * 50)
      .attr("x", (d) => xScale(d.skill));

    // update x-axis labels
    d3.select(xAxis)
      // .selectAll(".tick")
      // .data(data)
      .transition()
      .duration(750)
      .delay(1250)
      .call(d3.axisBottom(xScale));
      // .delay((d, i) => 1250 + i * 50)
      // .attr("transform", (d) => `translate(${xScale(d.title)}px, 0px)`);
  }

  function reset() {
    d3.select(marks)
      .selectAll("*")
      .remove();
    d3.select(xAxis)
      .selectAll("*")
      .remove();
    d3.select(yAxis)
      .selectAll("*")
      .remove();
    
    initialRender();
  }

   
</script>

<main>
  
    <svg {width} {height}>
      <g 
        style="transform: translate({margin.left}px, {margin.top}px)" 
        bind:this={marks}></g>
      <g 
        style="transform: translate({margin.left}px, {height - margin.bottom}px)" 
        bind:this={xAxis}></g>
      <g 
        style="transform: translate({margin.left}px, {margin.top}px)" 
        bind:this={yAxis}></g>
    </svg>

    <br/>
    <button on:click={update}>Job Positions</button>
    <button on:click={update2jr}>Community Colleges</button>

</main>

<style>
    button {
        border: none;
        padding: 0.5rem 2rem;
        color: slategrey;
        font-size: 1.5rem;
        border-radius: 1rem;
        transition: all 250ms;
        transform-origin: center;
        box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.25),
        inset 0px -2px 3px rgba(0, 0, 0, 0.25);
    }
    button:hover {
        cursor: pointer;
        transform: scale(0.975);
        box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.25);
    }
  </style>