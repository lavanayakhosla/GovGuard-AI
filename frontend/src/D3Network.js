import * as d3 from "d3";
import { useEffect } from "react";
import api from "./api";

export default function D3Network() {
  useEffect(() => {
    d3.select("#network").selectAll("*").remove();

    Promise.all([
      api.get("/fraud"),
      api.get("/collusion")
    ]).then(([fraudRes, collRes]) => {
      const txns = fraudRes.data;
      const colluding = new Set(collRes.data.map(d => d.vendor));

      const nodes = {};
      const links = [];

      // ---- build nodes & links ----
      txns.forEach(t => {
        if (!nodes[t.vendor])
          nodes[t.vendor] = { id: t.vendor, type: "vendor" };

        if (!nodes[t.scheme])
          nodes[t.scheme] = { id: t.scheme, type: "scheme" };

        links.push({
          source: t.vendor,
          target: t.scheme,
          amount: t.amount
        });
      });

      const nodeList = Object.values(nodes);

      // ---- SVG ----
      const width = 700, height = 450;
      const svg = d3.select("#network")
        .attr("width", width)
        .attr("height", height);

      const tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("background", "#333")
        .style("color", "#fff")
        .style("padding", "6px")
        .style("border-radius", "4px")
        .style("display", "none");

      // ---- simulation ----
      const simulation = d3.forceSimulation(nodeList)
        .force("link", d3.forceLink(links).id(d => d.id).distance(120))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2));

      // ---- links ----
      const link = svg.append("g")
        .selectAll("line")
        .data(links)
        .enter()
        .append("line")
        .attr("stroke", "#aaa")
        .attr("stroke-width", d => d.amount > 200000 ? 3 : 1);

      // ---- nodes ----
      const node = svg.append("g")
        .selectAll("circle")
        .data(nodeList)
        .enter()
        .append("circle")
        .attr("r", d => d.type === "vendor" ? 10 : 8)
        .attr("fill", d => {
          if (colluding.has(d.id)) return "red";
          return d.type === "vendor" ? "#1f77b4" : "#2ca02c";
        })
        .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
        )
        .on("mouseover", (e, d) => {
          tooltip.style("display", "block")
            .html(`<b>${d.id}</b><br/>Type: ${d.type}`);
        })
        .on("mousemove", e => {
          tooltip
            .style("left", e.pageX + 10 + "px")
            .style("top", e.pageY + 10 + "px");
        })
        .on("mouseout", () => tooltip.style("display", "none"));

      simulation.on("tick", () => {
        link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

        node
          .attr("cx", d => d.x)
          .attr("cy", d => d.y);
      });

      function dragstarted(e) {
        if (!e.active) simulation.alphaTarget(0.3).restart();
        e.subject.fx = e.subject.x;
        e.subject.fy = e.subject.y;
      }

      function dragged(e) {
        e.subject.fx = e.x;
        e.subject.fy = e.y;
      }

      function dragended(e) {
        if (!e.active) simulation.alphaTarget(0);
        e.subject.fx = null;
        e.subject.fy = null;
      }

      return () => tooltip.remove();
    });
  }, []);

  return <svg id="network"></svg>;
}