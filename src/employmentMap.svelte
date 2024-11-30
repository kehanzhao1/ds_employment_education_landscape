<script>
    import * as d3 from 'd3';
    import {legendColor} from 'd3-svg-legend';
    import { onMount } from 'svelte';

    let data = [];
    let fullData = [];

     let width = 800;
    let height = 800;

    let proj = d3.geoMercator()
        .scale(850)
        .center([-98.35, 39.50]) //us center
        .translate([width /2, height/2]);

    let path = d3.geoPath().projection(proj);
    let customColors = [

    "#8c2d04", "#b73f06",  "#f86f2f", "#ff9765", "#ffbb98", "#ffdbc9", "#fafafa"
    ];
    let scale = d3.scaleThreshold()
    .domain([90, 3000,7000, 14000, 20000, 27000, 34000])
    .range(customColors.reverse());

    //let scale = d3.scaleSequential(d3.interpolateBlues);

    let legend; 
    let tooltip;
    const formatComma = d3.format(",");
    
    onMount(async function () {
    let geoData = await d3.json('merged_us_ds_employment.geojson');
    geoData.features.forEach(feature => {
        const employmentPerThousand = feature.properties["Employment per 1,000 jobs"];
        if (employmentPerThousand !== "-" && employmentPerThousand !== null) {
          feature.properties["Employment per 1,000 jobs"] = parseFloat(employmentPerThousand);
        } else {
          feature.properties["Employment per 1,000 jobs"] = null; // Handle cases where the value is "-" or null
        }
      });
    data = geoData.features;
    fullData = [...data];
    tooltip = d3.select(tooltip)
        .style("position", "absolute")
        .style("opacity", 1)
        .style("background", "#e8e2e2")
        .style("border", "0px")
        .style("border-radius", "8px")
        .style("padding", "8px")
        .style("pointer-events", "none");
});

    $: if (data.length > 0) {
    const customLabels = [
          `< ${formatComma(90)}`,
          `${formatComma(90)} - 3k`,
          `3k - 7k`,
          `7k - 14k`,
          `14k - 20k`,
          `20k - 27k`,
          `>33k`
      ];
      const colorLegend = legendColor()
                  .orient('horizontal')
                  .shapeWidth(70)
                  .labelFormat(d3.format(","))
                  .labels(customLabels) 
                  .cells(7)
                  .scale(scale);
      d3.select(legend)
                  .call(colorLegend);
    }
     function getFillColor(d) {
    if (d.properties["Area Name"] == "Wyoming" || d.properties["Area Name"] == "Kansas") {return 'lightgrey';}     
      else if (isNaN(+d.properties.Employment)) {
          return 'black';
        } else {
          return scale(+d.properties.Employment);
        }
    }

  function showTooltip(event, d) {
    tooltip.style("opacity", 1)
      .html(`
        <strong>State:</strong> ${d.properties["Area Name"]}<br>
        <strong>Employment:</strong> ${formatComma(d.properties.Employment)}<br>
        <strong>Mean Annual Wage:</strong> ${formatComma(d.properties["Annual mean wage"])}<br>
        <strong>Employment per 1,000 jobs:</strong> ${d.properties["Employment per 1,000 jobs"]}
      `)
      .style("left", (event.pageX + 10) + "px")
      .style("top", (event.pageY - 28) + "px");
  }

  function hideTooltip() {
    tooltip.style("opacity", 0);
  }



</script>

<main>
    <svg {width} {height}>

      {#each data as d (d.properties["Area Name"])}
        <!-- svelte-ignore a11y-mouse-events-have-key-events -->
        <path
          d={path(d)}
          style="fill: {getFillColor(d)};"
          class = "state-path"
          on:mouseover={(event)=>showTooltip(event, d)}
          on:mouseout={hideTooltip}
          role="region"
          aria-label={`State: ${d.properties["Area Name"]}
          , Employment: ${d.properties.Employment}, Median Annual Wage: ${d.properties["Annual mean wage"]}`}
      />
      
                {/each}
                {#each fullData as d}
                <path 
                  class="geooverlay" 
                  d={path(d)} 
                />
                 {/each}

        <g transform="translate(50, 115)" bind:this={legend} >
              <text x="10" y="-10" class="legend-title">DS employment estimates 2023</text>
        </g>
      </svg>
       <!-- Tooltip element -->
  <div bind:this={tooltip} class="tooltip"></div>
</main>

<style>
    .geooverlay {
      stroke: grey;
      stroke-width: 2px;
      fill: none;
    }

    .state-path {
  stroke: #fff;
  stroke-width: 0.5;
}

    .legend-title {
    font-size: 22px;
    font-weight: bold;
    fill: #271103;
    font-family: Lato, sans-serif;
  }
  
  .tooltip {
    position: absolute;
    text-align: left;
    width: auto;
    height: auto;
    padding: 8px;
    font: 12px sans-serif;
    background: rgb(228, 207, 204);
    border: 0px;
    border-radius: 8px;
    pointer-events: none;
    opacity: 0;
  }
  </style>