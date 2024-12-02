<script>
    import * as d3 from 'd3';
    import { onMount } from "svelte";

    let container;
    const width = 1150;
    const height = 600;
    const USMapPath = "/us_states.json";

    let tooltip;

    onMount(async () => {
        // Load data files
        const cityData = await d3.csv('/median_salary.csv', d => ({
            city: d.city,
            latitude: +d.latitude,
            longitude: +d.longitude
        }));

        const collegeData = await d3.csv('/cc_with_coor.csv', d => ({
            college: d["College Name"],
            latitude: +d.LATITUDE,
            longitude: +d.LONGITUDE,
            hasDS: +d["Data Science degree/cert Offered"],
            hasDeg: +d["Offers AS"] 
        }));

        const us = await d3.json(USMapPath);

        const projection = d3.geoMercator()
            .center([-95, 37.5])
            .scale(1000)
            .translate([width / 2, height / 2]);

        const pathGenerator = d3.geoPath().projection(projection);

        const points = cityData.map(d => ({
            city: d.city,
            coords: projection([d.longitude, d.latitude])
        }));

        const delaunay = d3.Delaunay.from(points.map(d => d.coords));
        const voronoi = delaunay.voronoi([-900, -900, 1200, 800]);

        const findCollegesInPolygon = (polygon) =>
            collegeData.filter(college =>
                d3.polygonContains(polygon, projection([college.longitude, college.latitude]))
            );

        const polygons = points.map((point, i) => ({
            polygon: voronoi.cellPolygon(i),
            city: point.city,
            colleges: findCollegesInPolygon(voronoi.cellPolygon(i))
        }));

        const zoom = d3.zoom()
            .scaleExtent([1, 32])
            .on("zoom", zoomed);

        const svg = d3.select(container)
            .attr("width", width)
            .attr("height", height)
            .call(zoom);

        const mapGroup = svg.append("g");

        // Draw US state outlines
        const stateGroup = mapGroup.append("g")
            .selectAll("path")
            .data(us.features) // Assuming the JSON has a `features` array with GeoJSON format
            .enter().append("path")
            .attr("d", pathGenerator)
            .attr("fill", "none")
            .attr("stroke", "#999") // Light gray stroke for state outlines
            .attr("stroke-width", 1);

        // Draw Voronoi polygons
        const voronoiGroups = mapGroup.append("g")
            .selectAll("path")
            .data(polygons)
            .enter().append("path")
            .attr("d", d => d ? `M${d.polygon.join('L')}Z` : null)
            .attr("fill", "#e8e2e2")
            .attr("stroke", "#6b6060d2")
            .attr("opacity", 0.5)
            .on("mouseleave", () => hideTooltip())
            .on("mouseover", function (event, d) {
                // const collegesInPolygon = findCollegesInPolygon(d.polygon);
                d3.selectAll(".college")
                    //.attr("fill", college => d.colleges.includes(college) ? "#feb388" : "#ed5701");
                    .attr("fill", college => {
                        if (d.colleges.includes(college)) {
                            return college.hasDS === 1 && college.hasDeg === 1 ? "#39FF14" : "#feb388";
                        }
                        return "#ed5701"; 
                    });
                showTooltip(event, d)

            })
            .on("mouseout", function () {
                d3.selectAll(".college")
                    .attr("fill", "#ed5701");
            })
            .attr("stroke-width", 2);
        
        const cityPoints = mapGroup.append("g")
            .selectAll("circle")
            .data(points)
            .enter().append("circle")
            .attr("cx", d => d.coords[0])
            .attr("cy", d => d.coords[1])
            .attr("opacity", 0.7)
            .attr("r", 8)
            .attr("fill", "#00008B");

        // college points
        const collegePoints = mapGroup.append("g")
            .selectAll(".college")
            .data(collegeData)
            .enter().append("circle")
            .attr("opacity", 0.5)
            .attr("class", "college")
            .attr("cx", d => projection([d.longitude, d.latitude])[0])
            .attr("cy", d => projection([d.longitude, d.latitude])[1])
            .attr("r", 4)
            .attr("fill", "#ed5701");
        
        function zoomed(event) {
            mapGroup.attr("transform", event.transform);  
            const scale = event.transform.k;
            cityPoints.attr("r", 8 / scale); 
            collegePoints.attr("r", 4 / scale);
            voronoiGroups.attr("stroke-width", 2 / scale);
            stateGroup.attr("stroke-width", 1 / scale);
        }

        function showTooltip(event, d) {
            const collegesWithDS = d.colleges.filter(c => c.hasDS === 1 && c.hasDeg === 1);

            console.log(collegesWithDS);

            d3.select(tooltip)
                .style("left", `${event.pageX + 10}px`) 
                .style("top", `${event.pageY + 10}px`)
                .style("opacity", 1)
                .html(`
                    <strong>City:</strong> ${d.city}
                    <br><strong>Colleges with a DS degree:</strong> ${collegesWithDS.length > 0 ? collegesWithDS.map(c => c.college).join(", ") : "None"}
                `);
        }

        function hideTooltip() {
            d3.select(tooltip).style("opacity", 0);
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
        text-align: left;
        max-width: 200px;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
</style>