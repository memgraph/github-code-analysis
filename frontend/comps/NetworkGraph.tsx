import {Box, Grid, Typography} from "@mui/material";
import React from "react";
import { useRef, useEffect } from "react";
import * as d3 from "d3";
import useD3 from "./useD3";


const NetworkGraph = ({data}: {data: any}) => {
    const graph = useD3({"funct": (svg: any) => {
        const drag = (simulation: any) => {
            function dragstarted(d) {
                if (!d3.event.active) simulation.alphaTarget(0.5).restart();
                d.fx = d.x;
                d.fy = d.y;
            }

            function dragged(d) {
                d.fx = d3.event.x;
                d.fy = d3.event.y;
            }

            function dragended(d) {
                if (!d3.event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }

            return d3
                .drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended);
        };

        const edges = data.links.map((d) => d.index);

        svg.selectAll("*").remove();

        var e = document.querySelector("div.dependency_graph");
        var width = 0
        var height = 0
        if (e) {
            width = e.clientWidth;
            height = e.clientHeight;
            console.log(width, height);
        }


        const simulation = d3
            .forceSimulation(data.nodes)
            .force(
                "line",
                d3
                    .forceLink(data.links)
                    .distance(300)
                    .strength(0)
                    .iterations(1)
                    .id((d) => d.id)
            )
            .force("charge",
                d3.forceManyBody()
                    .strength(-200)
                    .distanceMin(50)
                    .distanceMax(150)
            )
            .force("collide",
                d3.forceCollide()
                    .radius(20)
                    .iterations(1)
                    .strength(2)
            )
            .force("center", d3.forceCenter(width / 2, height / 2))

        svg.append('defs').selectAll('marker')
            .data(edges)
            .enter().append("marker")
            .attr('id', (d) => `arrowhead-${d}`)
            .attr('viewBox', '-0 -5 10 10')
            .attr('refX', 10)
            .attr('refY', 0)
            .attr('markerWidth', 10)
            .attr('markerHeight', 10)
            .attr('orient', 'auto')
            .append('path')
            .attr("d", "M0,-5L10,0L0,5")
            .attr('fill', '#999')
            .style('stroke','none');

        const link = svg
            .append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
            .attr("stroke-width", 1)
            .selectAll("line")
            .data(data.links)
            .enter()
            .append("line")
            .attr("class", "link")
            .attr('marker-end', (d) => {
                return `url(#arrowhead-${d.index})`
            })

        const node = svg
            .append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")
            .data(data.nodes)
            .join("circle")
            .attr("r", (d) => d.size)
            .attr("class", "node")
            .attr("fill", function (d: any) {
                return d.color
            })
            .call(drag(simulation));

        var label = svg
            .selectAll(null)
            .data(data.nodes)
            .enter()
            .append("text")
            .text(function (d: any) {
                return d.name;
            })
            .style("text-anchor", "middle")
            .style("fill", "black")
            .style("font-family", "Arial")
            .style("font-size", "12px")
            .attr("x", 0)
            .attr("y", 0)
            .attr("dy", (d) => (-1) * (d.size / 2));

        node.on('mouseover', function(d) {

            link.style('stroke-width', function(l) {
                if (d === l.source || d === l.target) {
                    return 2
                } else {
                    return 1
                }
            });

            node.style('opacity', function(l) {
                for (let i = 0; i < data.links.length; i++) {
                    if ((data.links[i].source === d || data.links[i].target === d) && (data.links[i].source === l || data.links[i].target === l)) {
                        return 1
                    }
                }
                if (d === l) {
                    return 1
                } else {
                    return 0.2
                }
            });

            link.style('opacity', function(l) {
                if (d === l.source || d === l.target) {
                    return 1
                } else {
                    return 0.2
                }
            })

            label.style('opacity', function(l) {
                for (let i = 0; i < data.links.length; i++) {
                    if ((data.links[i].source === d || data.links[i].target === d) && (data.links[i].source === l || data.links[i].target === l)) {
                        return 1
                    }
                }
                if (d === l) {
                    return 1
                } else {
                    return 0.2
                }
            })
        });

        node.on('mouseout', function() {
            link.style('stroke', "#999");
            link.style('stroke-width', 1);
            link.style('opacity', 1);
            label.style('opacity', 1);
            node.style('opacity', 1);
        });

        const zoom = d3.zoom()
            .on('zoom', function() {
                const { transform } = d3.event;
                link.attr('transform', transform);
                node.attr('transform', transform);
                label.attr('transform', transform);
            });

        svg.call(zoom);

        simulation.on("tick", () => {
            link.attr("x1", function (d) { return d.source.x; })
                .attr("y1", function (d) { return d.source.y; })
                .attr("x2", function (d) {
                    return calculateX(d.target.x, d.target.y, d.source.x, d.source.y, d.target.size);
                })
                .attr("y2", function (d) {
                    return calculateY(d.target.x, d.target.y, d.source.x, d.source.y, d.target.size);
                });

            node.attr("cx", (d: any) => d.x).attr("cy", (d: any) => d.y);
            label
                .attr("x", function (d: any) {
                    return d.x;
                })
                .attr("y", function (d: any) {
                    return d.y - 15;
                });
        });

        function calculateX(tx, ty, sx, sy, radius){
            if(tx == sx) return tx;
            var xLength = Math.abs(tx - sx);
            var yLength = Math.abs(ty - sy);

            var ratio = radius / Math.sqrt(xLength * xLength + yLength * yLength);
            if(tx > sx)  return tx - xLength * ratio;
            if(tx < sx) return  tx + xLength * ratio;
        }
        function calculateY(tx, ty, sx, sy, radius){
            if(ty == sy) return ty;
            var xLength = Math.abs(tx - sx);
            var yLength = Math.abs(ty - sy);

            var ratio = radius / Math.sqrt(xLength * xLength + yLength * yLength);
            if(ty > sy) return ty - yLength * ratio;
            if(ty < sy) return ty + yLength * ratio;
        }

        simulation.tick(300)

    }, "graph_data": data});

    return (
        <Box className={"dependency_graph"} sx={{width:"100%", minHeight: "50vh", height: "100%", backgroundColor: "white"}}>
            <svg style={{width: "100%", height: "100%"}} ref={graph}></svg>
        </Box>
    )
}

export default NetworkGraph;