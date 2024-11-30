<script>
 import * as d3 from 'd3';
 import { onMount} from 'svelte';
 import App from './App.svelte';
 export let value;

 let linemargin = { top: 40, right: 50, bottom: 40, left: 100 };
 let linewidth = 500 - linemargin.left - linemargin.right;
 let lineheight = 550 - linemargin.top - linemargin.bottom;
    //let chartW = width - margin.left - margin.right;
   // let chartH = height - margin.top - margin.bottom;

let datal  = []
let professions = [];
let visibleProfessions = new Set();

    // Scale
let xScale, yScale, colorScale;
let svgElement;
const formatComma = d3.format(",");

onMount(async () => {

const rawData = await d3.csv('ass2_data2.csv', d=> ({
            ...d,
            'Year': +d['Year'],
            'Total employment estimates DS': +d['Total employment estimates DS'],
            'Total employment estimates SWE': +d['Total employment estimates SWE'],
            'Total employment estimates ST': +d['Total employment estimates ST'],
            'DS growth rate emp': String(d['DS growth rate emp']),
            'ST growth rate emp': String(d['ST growth rate emp']),
            'SWE growth rate emp':String(d['SWE growth rate emp']),
            'Mean Wage DS': +d['Mean Wage DS'],
            'Mean Wage SWE': +d['Mean Wage SWE'],
            'Mean Wage ST': +d['Mean Wage ST']

        }));
        datal = [];
        rawData.forEach(d => {
            datal.push({ year: d['Year'], wage: d['Mean Wage DS'], employment: d['Total employment estimates DS'], growthRate:d['DS growth rate emp'],profession: 'Data Scientist' });
            datal.push({ year: d['Year'], wage: d['Mean Wage SWE'], employment: d['Total employment estimates SWE'], growthRate:d['SWE growth rate emp'], profession:'Sofware Developer' });
            datal.push({ year: d['Year'], wage: d['Mean Wage ST'], employment: d['Total employment estimates ST'], growthRate:d['ST growth rate emp'], profession:'Statistician' });
        });

        // Extract unique professions
  professions = Array.from(new Set(datal.map(d => d.profession)));
  //console.log("professions",professions);
  visibleProfessions = new Set(professions); // Initially, all professions are visible
   // console.log("visibleProfessions",visibleProfessions)
    //console.log("rawData", rawData)
    //console.log("datal", datal) 
    renderLineGraph();
      });

    
  function clearGraph() {
    if (svgElement) {
      svgElement.selectAll("*").remove();
    }}

 function renderLineGraph() {
    clearGraph();
    const svg = d3.select('svg');
    svg.selectAll("*").remove();
            const mainGroup = svg
        .attr("width", linewidth + linemargin.left + linemargin.right)
        .attr("height", lineheight + linemargin.top + linemargin.bottom)
        .append("g")
        .attr("transform", `translate(${linemargin.left},${linemargin.top})`);
     console.log('linemargin left',linemargin.left)

    const visibleData = datal.filter(d => visibleProfessions.has(d.profession));

        const xScale = d3.scaleLinear()
            .domain(d3.extent(datal, d => d.year))
            .range([0, linewidth]);

        const yScale = d3.scaleLinear()
            .domain([0, d3.max(visibleData, d => d.employment)])
            .nice()
            .range([lineheight,0]);

        const colorScale = d3.scaleOrdinal()
            .domain(professions)
            .range(['steelBlue', 'darkSalmon', 'darkSeaGreen']);

        // Create the x and y axes
        mainGroup.append("g")
            .attr("transform", `translate(0,${lineheight})`)
            .call(d3.axisBottom(xScale)
            .ticks(5)
            .tickFormat(d3.format("d")))
            .selectAll("text")
            .style("font-size", "16px");
            
        //const yAxis = svg.append("g").call(d3.axisLeft(yScale));
        mainGroup.append("g")
            .call(d3.axisLeft(yScale))
            .selectAll("text")
            .style("font-size", "14px");
        

         // Add x-axis label
         mainGroup.append("text")
            .attr("class","axis-label")
            .attr("text-anchor", "middle")
            .attr("x", linewidth / 2)
            .attr("y", lineheight + linemargin.bottom + 20) // Position slightly below the x-axis
            .style("font-size", "20px")
            .text("Year");
    // Add y-axis label
    mainGroup.append("text")
       .attr("class","axis-label")
       .attr("text-anchor", "middle")
       .attr("transform", `rotate(-90)`)
       .attr("x", -lineheight / 2)
       .attr("y", -linemargin.left + 15) // Position slightly left of the y-axis
       .style("font-size", "20px")
       .text("Employment Estimates");


        // Line generator function
        const line = d3.line()
            .x(d => xScale(d.year))
            .y(d => yScale(d.employment));

        // Draw a line for each profession
        const tooltip = d3.select("#tooltip")
        .style("position", "absolute")
        .style("opacity", 0) // Initially hidden
        .style("background", "lightsteelblue")
        .style("border", "0px")
        .style("border-radius", "8px")
        .style("padding", "6px 6px")
        .style("font-size", "18px")
        .style("pointer-events", "none")
        .style("color", "black");

        const professionGroups = d3.groups(datal, d => d.profession);
        professionGroups.forEach(([profession, values]) => {
            if (visibleProfessions.has(profession)) {
                const path = mainGroup.append("path")
                .datum(values)
                .attr("class", profession.replace(/\s+/g, '_')) // Class name for each line
                .attr("fill", "none")
                .attr("stroke", colorScale(profession))
                .attr("stroke-width", 4)
                .attr("d", line);
                const totalLength = path.node().getTotalLength();
                path
                    .attr("stroke-dasharray", `${totalLength} ${totalLength}`) // Set up dasharray to hide the line
                    .attr("stroke-dashoffset", totalLength) // Start the line completely hidden
                    .transition() // Animate the dashoffset
                    .duration(500) // Duration of the animation
                    .ease(d3.easeLinear) // Linear easing for smooth animation
                    .attr("stroke-dashoffset", 0); 
            // Draw points for each data point
            mainGroup.selectAll(`.dot-${profession}`)
                .data(values)
                .enter()
                .append("circle")
                .attr("class", profession.replace(/\s+/g, '_')) // Same class for points
                .attr("cx", d => xScale(d.year))
                .attr("cy", d => yScale(d.employment))
                .attr("r", 5)
                .attr("fill", colorScale(profession))
                .on("mouseover", (event, d) => {
                    const lineColor = colorScale(d.profession);
                    const rgbaColor = d3.color(lineColor).copy({opacity:0.7}).formatRgb();
                        tooltip.transition().duration(50).style("opacity", 1).style("background",rgbaColor);
                        tooltip.html(`<strong>Employment</strong>: ${formatComma(d.employment)}<br><strong>Growth Rate</strong>: ${d.growthRate}`)
                            .style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 28) + "px");
                    })
                    .on("mousemove", (event) => {
                        tooltip.style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 28) + "px");
                    })
                    .on("mouseout", () => {
                        tooltip.transition().duration(100).style("opacity", 0);
                    });   
            }  //Profession: ${d.profession}<br>Year: ${d.year}<br>

        });

    
       const legend = mainGroup.append("g")
        .attr("transform", `translate(10, -30)`); // Position legend

    const legendItems = legend.selectAll(".legend")
        .data(professions)
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", (d, i) => `translate(${i * 150}, 30)`)
        .style("cursor", "pointer") 
        .on("click", function(event, d) {
            const isVisible = visibleProfessions.has(d);
            // Toggle visibility in the visibleProfessions set
            if (isVisible) {
                visibleProfessions.delete(d);
            } else {
                visibleProfessions.add(d);
            }
            renderLineGraph();         
                }); // Add click event for toggling

    legendItems.append("circle")
        .attr("cx", 0)
        .attr("cy", 2)
        .attr("r", 8)
        .attr("radius", 8)
        .style("fill", d => colorScale(d))
        .style("opacity", d => visibleProfessions.has(d) ? 1 : 0.2); // Dim if not visible

    legendItems.append("text")
        .attr("x", 15)
        .attr("y", 0)
        .attr("dy", "0.7em")
        .attr("d", "0.7em")
        .style("text-anchor", "start")
        .style("font-size", "15px")
        .text(d => d);
  }
  function renderWageGraph() {
    clearGraph();

    const svg = d3.select('svg');
    svg.selectAll("*").remove();

    const mainGroup = svg
      .attr("width", linewidth + linemargin.left + linemargin.right)
      .attr("height", lineheight + linemargin.top + linemargin.bottom)
      .append("g")
      .attr("transform", `translate(${linemargin.left},${linemargin.top})`);
    const visibleData = datal.filter(d => visibleProfessions.has(d.profession));

    const xScale = d3.scaleLinear()
      .domain(d3.extent(datal, d => d.year))
      .range([0, linewidth]);

    const yScale = d3.scaleLinear()
      .domain([80000, d3.max(visibleData, d => d.wage)])
      .nice()
      .range([lineheight, 0]);

    const colorScale = d3.scaleOrdinal()
      .domain(professions)
      .range(['steelBlue', 'darkSalmon', 'darkSeaGreen']);

    // Create the x and y axes
    mainGroup.append("g")
      .attr("transform", `translate(0,${lineheight})`)
      .call(d3.axisBottom(xScale).ticks(5).tickFormat(d3.format("d")))
      .selectAll("text")
      .style("font-size", "16px");

    mainGroup.append("g")
      .call(d3.axisLeft(yScale))
      .selectAll("text")
      .style("font-size", "14px");

    // Add x-axis label
    mainGroup.append("text")
      .attr("class", "axis-label")
      .attr("text-anchor", "middle")
      .attr("x", linewidth / 2)
      .attr("y", lineheight + linemargin.bottom + 20) // Adjust position to avoid cutting off
      .style("font-size", "20px")
      .text("Year");

    // Add y-axis label
    mainGroup.append("text")
      .attr("class", "axis-label")
      .attr("text-anchor", "middle")
      .attr("transform", `rotate(-90)`)
      .attr("x", -lineheight / 2)
      .attr("y", -linemargin.left + 15)
      .style("font-size", "20px")
      .text("Annual Average Wage (USD)");

    // Line generator function
    const line = d3.line()
      .x(d => xScale(d.year))
      .y(d => yScale(d.wage));


      const tooltip = d3.select("#tooltip")
        .style("position", "absolute")
        .style("opacity", 0) // Initially hidden
        .style("background", "lightsteelblue")
        .style("border", "0px")
        .style("border-radius", "8px")
        .style("padding", "6px 6px")
        .style("font-size", "18px")
        .style("pointer-events", "none")
        .style("color", "black");

      const professionGroups = d3.groups(datal, d => d.profession);
        professionGroups.forEach(([profession, values]) => {
            if (visibleProfessions.has(profession)) {
                const path = mainGroup.append("path")
                .datum(values)
                .attr("class", profession.replace(/\s+/g, '_')) // Class name for each line
                .attr("fill", "none")
                .attr("stroke", colorScale(profession))
                .attr("stroke-width", 4)
                .attr("d", line);
                const totalLength = path.node().getTotalLength();
                path
                    .attr("stroke-dasharray", `${totalLength} ${totalLength}`) // Set up dasharray to hide the line
                    .attr("stroke-dashoffset", totalLength) // Start the line completely hidden
                    .transition() // Animate the dashoffset
                    .duration(500) // Duration of the animation
                    .ease(d3.easeLinear) // Linear easing for smooth animation
                    .attr("stroke-dashoffset", 0); // End with the line fully drawn
            // Draw points for each data point
            mainGroup.selectAll(`.dot-${profession}`)
                .data(values)
                .enter()
                .append("circle")
                .attr("class", profession.replace(/\s+/g, '_')) // Same class for points
                .attr("cx", d => xScale(d.year))
                .attr("cy", d => yScale(d.wage))
                .attr("r", 5)
                .attr("fill", colorScale(profession))
                .on("mouseover", (event, d) => {
                    const lineColor = colorScale(d.profession);
                    const rgbaColor = d3.color(lineColor).copy({opacity:0.7}).formatRgb();
                        tooltip.transition().duration(50).style("opacity", 1).style("background",rgbaColor);
                        tooltip.html(`<strong>Employment</strong>: ${formatComma(d.employment)}<br><strong>Growth Rate</strong>: ${d.growthRate}`)
                            .style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 28) + "px");
                    })
                    .on("mousemove", (event) => {
                        tooltip.style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 28) + "px");
                    })
                    .on("mouseout", () => {
                        tooltip.transition().duration(100).style("opacity", 0);
                    });   
            }  //Profession: ${d.profession}<br>Year: ${d.year}<br>

        });
    // Add legend
    const legend = mainGroup.append("g")
      .attr("transform", `translate(10, -30)`);

      const legendItems = legend.selectAll(".legend")
        .data(professions)
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", (d, i) => `translate(${i * 150}, 30)`)
        .style("cursor", "pointer") 
        .on("click", function(event, d) {
            const isVisible = visibleProfessions.has(d);
            // Toggle visibility in the visibleProfessions set
            if (isVisible) {
                visibleProfessions.delete(d);
            } else {
                visibleProfessions.add(d);
            }

            renderWageGraph();
            
                }); // Add click event for toggling
 // Position each item on a new line

    legendItems.append("circle")
      .attr("cx", 0)
      .attr("cy", 2)
      .attr("r", 8)
      .style("fill", d => colorScale(d))
      .style("opacity", d => visibleProfessions.has(d) ? 1 : 0.2); // Dim if not visible

    legendItems.append("text")
      .attr("x", 15)
      .attr("y", 0)
      .attr("dy", "0.35em")
      .style("text-anchor", "start")
      .style("font-size", "15px")
      .text(d => d);
  }


  $: {
  if (value === 0 ) {renderLineGraph()} else if (value === 1) {
   renderWageGraph()
  }
}

</script>


<svg id="lineCompare"></svg>


<style>
    .text {
        font-size: 12px;
        fill: black;
    }
    svg text, svg line {
        font-family: Arial, sans-serif;
    }
    .axis-label {
     font-size: 10px; /* Reduce the text size of the axis labels */
    }
</style>
