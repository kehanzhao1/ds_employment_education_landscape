<script>
    import * as d3 from 'd3';
    import {onMount} from "svelte";
    import {hexbin as d3Hexbin} from "d3-hexbin";
    import {legendColor} from 'd3-svg-legend';

    export let CCPath;

    let container;
    const width = 1150;
    const height = 600;
    const USMapPath = "/us_states.json";
    const zoomLevel = 3;

    let tooltip;

    onMount(async () => {
        const data = await d3.csv(CCPath, d => ({
            latitude: +d.LATITUDE,
            longitude: +d.LONGITUDE,
            college: d["College Name"],
            city: d.City,
            state: d.State,
            hasDS: +d["Data Science degree/cert Offered"],
            hasDA: +d["Data Analytics degree/cert Offered"],
            hasDSClass: +d["Offer Data Science Course"],
            hasCert: +d["Offers Certificate"],
            hasDeg: +d["Offers AS"]
        }));

        const projection = d3.geoMercator()
            .scale(1000)
            .center([-95, 37.5])
            .translate([width / 2, height / 2]);

        const path = d3.geoPath().projection(projection);

        const us = await d3.json(USMapPath);

        const hexbin = d3Hexbin()
            .radius(5)
            .x(d => projection([d.longitude, d.latitude])[0])
            .y(d => projection([d.longitude, d.latitude])[1]);

        const bins = hexbin(data);
        bins.forEach(bin => {
            bin.numDSClass = d3.sum(bin, d => d.hasDSClass);
            bin.cities = d3.map(bin, d => d.city);
        });

        const colorScale = d3.scaleQuantize()
            .domain([Math.floor(d3.min(bins, d => d.numDSClass)), Math.ceil(d3.max(bins, d => d.numDSClass))])
            .range(d3.schemeYlOrRd[9]);

        const zoom = d3.zoom()
            .scaleExtent([1, 8])
            .on("zoom", zoomed);

        const svg = d3.select(container)
            .attr("width", width)
            .attr("height", height)
            .call(zoom);

        const mapGroup = svg.append("g");

        // state outlines
        mapGroup.append("g")
            .selectAll("path")
            .data(us.features)
            .enter().append("path")
            .attr("d", path)
            .attr("fill", "#e8e2e2")
            .attr("stroke", "#333");

        // hexagons
        mapGroup.append("g")
            .selectAll("path")
            .data(bins)
            .enter().append("path")
            .attr("d", d => `M${d.x},${d.y}${hexbin.hexagon()}`)
            .attr("fill", d => colorScale(d.numDSClass))
            .attr("stroke", "none")
            .attr("opacity", 0.8)
            .on("click", (event, d) => zoomToHexagon(d))
            .on("mouseover", (event, d) => showTooltip(event, d))
            .on("mouseleave", () => hideTooltip());

        // Legend
        const legendGroup = svg.append("g")
            .attr("class", "legend")
            .attr("transform", `translate(${width - 150}, 350)`);

        const thresholds = colorScale.thresholds();
        
        const colorLegend = legendColor()
            .scale(colorScale)
            .shape("rect")
            .shapeWidth(30)
            .cells(thresholds.length + 1) 
            .labels(({ i, genLength }) => {
                if (i === 0) {
                    return `≤ ${Math.floor(thresholds[0])}`;
                } else if (i === thresholds.length) {
                    return `≥ ${Math.ceil(thresholds[thresholds.length - 1])}`;
                } else {
                    return `${Math.ceil(thresholds[i - 1])}`;
                }
            })
            .title("Number of Schools");

        legendGroup.call(colorLegend);

        function showTooltip(event, d) {
            const tableRows = d.map(college => `
                <tr>
                    <td>${college.college}</td>
                    <td>${college.hasDSClass ? '✅' : '❌'}</td>
                </tr>
            `).join('');

            const tableHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>College</th>
                            <th>Has DS Course?</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${tableRows}
                    </tbody>
                </table>
            `;

    // tooltip near the mouse pointer
    d3.select(tooltip)
        .style("left", `${event.pageX + 10}px`) 
        .style("top", `${event.pageY + 10}px`)
        .style("opacity", 1)
        .html(`
            <b>Total Number of Schools:</b> ${d.length}
            <br><b>Number of Schools with DS Course:</b> ${d.numDSClass}
            ${tableHTML}
        `);
}


        function hideTooltip() {
            d3.select(tooltip).style("opacity", 0);
        }

        function zoomed(event) {
            mapGroup.attr("transform", event.transform);  
        }

        function zoomToHexagon(hex) {
            const [x, y] = [hex.x, hex.y];
            svg.transition().duration(750).call(
                zoom.transform,  
                d3.zoomIdentity.translate(width / 2, height / 2).scale(zoomLevel).translate(-x, -y)
            );
        }

    });
</script>

<main>
    <svg bind:this={container}></svg>
    <div bind:this={tooltip} class="tooltip"></div>
</main>

<style>
    svg {
        border: 1px solid #ccc;
    }

    .tooltip {
        position: absolute;
        background-color: white;
        color: black;
        border: 1px solid #ccc;
        padding: 8px;
        border-radius: 4px;
        font-size: 12px;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.2s ease;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    .tooltip table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 8px;
    }

    .tooltip th, .tooltip td {
        border: 1px solid #ccc;
        padding: 4px 8px;
        text-align: left;
    }

    .tooltip th {
        background-color: #f9f9f9;
        font-weight: bold;
    }

    .tooltip td {
        font-size: 12px;
    }

</style>
