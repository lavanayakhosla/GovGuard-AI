import * as d3 from "d3";
import { useEffect } from "react";

export default function IndiaMap({ data }) {
  useEffect(() => {
    d3.select("#map").selectAll("*").remove();

    const width = 600, height = 600;
    const svg = d3.select("#map")
      .attr("width", width)
      .attr("height", height);

    const tooltip = d3.select("body")
      .append("div")
      .style("position", "absolute")
      .style("padding", "6px")
      .style("background", "#333")
      .style("color", "#fff")
      .style("border-radius", "4px")
      .style("display", "none");

    fetch("/india_states.geojson")
      .then(res => res.json())
      .then(geo => {
        const projection = d3.geoMercator().fitSize([width, height], geo);
        const path = d3.geoPath().projection(projection);

        svg.selectAll("path")
          .data(geo.features)
          .join("path")
          .attr("d", path)
          .attr("fill", d => {
            const v = data[d.properties.NAME_1] || 0;
            return d3.interpolateReds(v / 20);
          })
          .attr("stroke", "#000")
          .on("mouseover", (e, d) => {
            const v = data[d.properties.NAME_1] || 0;
            tooltip
              .style("display", "block")
              .html(`${d.properties.NAME_1}<br/>Frauds: ${v}`);
          })
          .on("mousemove", e => {
            tooltip
              .style("left", e.pageX + 10 + "px")
              .style("top", e.pageY + 10 + "px");
          })
          .on("mouseout", () => tooltip.style("display", "none"));
      });

    return () => tooltip.remove();
  }, [data]);

  return <svg id="map"></svg>;
}