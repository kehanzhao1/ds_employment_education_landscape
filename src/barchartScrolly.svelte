<script>
  import * as d3 from 'd3';
  import { onMount } from 'svelte';
  export let value;
  
  let margin = { top: 80, right: 50, bottom: 90, left: 100 };
 let width = 500 - margin.left - margin.right;
 let height = 600 - margin.top - margin.bottom;


  let svgElement;
  
  let datab = [
    { industry: "Technology", percent: 0.11, wage: 118400 },
    { industry: "Insurance", percent: 0.10, wage: 104390 },
    { industry: "Management", percent: 0.09, wage: 114780 },
    { industry: "Consulting", percent: 0.06, wage: 103000 },
    { industry: "R&D", percent: 0.05, wage: 126430 }
  ];

  // Debugging the data
  console.log("Processed data:", datab);
  function clearGraph() {
    if (svgElement) {
      svgElement.selectAll("*").remove();
      
    }
  }
  $: if (value === 2) {
    console.log('Value is 2, rendering 3rd graph')// Debug value
    //clearGraph();
    svgElement = d3.select('#chart');
    //svgElement.selectAll(".lenged").remove();  
    drawBarChart('#BarchartScrolly', datab, 'industry', 'percent', 'darksalmon', 'Top employing sectors');
   
      } else if (value === 3) {
       // clearGraph();
    console.log('Value is 3, rendering 4th graph'); // Debug value
    clearGraph();
    //clearChart(selector);
    svgElement = d3.select('#chart');
    drawBarChart('#BarchartScrolly', datab, 'industry', 'wage','steelblue','Top paying sectors');
  }

  function drawBarChart(selector, data, xField, yField, barColor, title) {
    //clearGraph(); 
    if (!Array.isArray(data)) {
      console.error('Data is not an array:', data);
      return;
    }

    data = data.sort((a, b) => d3.descending(a[yField], b[yField]));

    const svg = d3.select(selector)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .html('')
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

      svg.append('text')
      .attr('x', (width / 2))             
      .attr('y', 0 - (margin.top / 2))
      .attr('text-anchor', 'middle')  
      .style('font-size', '24px') 
      .style('font-family', 'Lato, sans-serif')
      .text(title);

    const x = d3.scaleBand()
      .domain(data.map(d => d[xField]))
      .range([0, width])
      .paddingInner(0.1)
      .paddingOuter(0.1);

      const yMax = d3.max(data, d => d[yField]);
     const y = d3.scaleLinear()
    .domain([0, yMax]) // Dynamic domain based on the data field
    .nice()
    .range([height, 0]);

    svg.append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).tickSizeOuter(0))
      .selectAll('path, line')
      .attr('stroke', 'darkgray')
      .attr('stroke-width', 2);

      svg.selectAll('.x-axis text')
      .attr('transform', 'rotate(315)')
      .style('text-anchor', 'end');
      

      const yAxis = svg.append('g')
    .attr('class', 'y-axis')
    .call(d3.axisLeft(y).ticks(5)
      .tickFormat(yField === 'percent' 
        ? d3.format(".0%") 
        : d3.format(",") // Comma formatting for thousands
      ))
    .selectAll('path, line')
    .attr('stroke', 'darkgray')
    .attr('stroke-width', 2);
     
    const bars = svg.selectAll('.bar')
    .data(data, d => d[xField]);

  bars.enter()
    .append('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d[xField]))
    .attr('y', height)
    .attr('width', x.bandwidth())
    .attr('height', 0)
    .attr('fill', barColor)
    .merge(bars) // Merge to handle updates
    .transition() // Add smooth transition
    .duration(500)
    .attr('x', d => x(d[xField]))
    .attr('y', d => y(d[yField]))
    .attr('height', d => height - y(d[yField]));

  bars.exit().remove();


      svg.selectAll('.x-axis text, .y-axis text')
      .style('font-family', 'Lato, sans-serif')
      .style('font-size', '14px');

    svg.selectAll('.bar')
      .data(data)
      .enter().append('rect')
      .attr('class', 'bar')
      .attr('x', d => x(d[xField]))
      .attr('y', height)
      .attr('width', x.bandwidth())
      .attr('height',0)
      .attr('fill', barColor)
      .transition() // Add transition
      .duration(500) // Duration of the animation
      .attr('y', d => y(d[yField])) // Transition to the final y position
      .attr('height', d => height - y(d[yField])); // Transition to the final height
  const labels = svg.selectAll('.label')
      .data(data, d => d[xField]);

    labels.enter()
    .append('text')
    .attr('class', 'label')
    .attr('x', d => x(d[xField]) + x.bandwidth() / 2)
    .attr('y', height)
    .attr('text-anchor', 'middle')
    .style('font-family', 'Lato, sans-serif')
    .style('font-size', '16px')
    .style('fill', barColor)
    .style('font-weight', 'bold')
    .merge(labels) // Merge to handle updates
    .transition() // Add smooth transition
    .duration(1000)
    .attr('x', d => x(d[xField]) + x.bandwidth() / 2)
    .attr('y', d => y(d[yField]) - 8)
    .text(d => yField === 'percent' 
      ? d3.format(".1%")(d[yField]) 
      : d3.format(",")(d[yField]));

  labels.exit().remove(); 
       // Transition to the final height
  }
</script>

<style>
 

  .x-axis path,
  .x-axis line,
  .y-axis path,
  .y-axis  {
    stroke: darkgray;
    stroke-width: 2px;
  }

  svg.x-axis text,
  svg.y-axis text {
    font-family: 'Lato', sans-serif; /* Set font to Lato */
    font-size: 14px; /* Make text bigger */
  }
</style>

<svg id="BarchartScrolly"></svg>