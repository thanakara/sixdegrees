/**
 * Renders shortest path graph using vis-network.
 * Fetches data from /api/path — no direct Bolt connection.
 */

document.addEventListener("DOMContentLoaded", () => {
    const _el = document.getElementById("neovis-graph");
    if (!_el) return;

    const NAME_A = _el.dataset.nameA;
    const NAME_B = _el.dataset.nameB;

    const PERSON_COLOR = { background: "#1a1a2e", border: "#a0a8d4", highlight: { background: "#20203e", border: "#f5c518" } };
    const MOVIE_COLOR = { background: "#2a1a00", border: "#f5c518", highlight: { background: "#3d2800", border: "#ffffff" } };

    const options = {
        nodes: {
            font: { color: "#efefef", face: "DM Sans", size: 14, strokeWidth: 0 },
            borderWidth: 1.5,
        },
        edges: {
            color: { color: "#555", highlight: "#f5c518" },
            font: { color: "#888", face: "DM Mono", size: 10, align: "middle", strokeWidth: 0 },
            width: 1.5,
            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
            smooth: { type: "curvedCW", roundness: 0.1 },
        },
        physics: {
            solver: "forceAtlas2Based",
            forceAtlas2Based: {
                gravitationalConstant: -40,
                springLength: 140,
                springConstant: 0.08,
            },
            stabilization: { iterations: 150 },
        },
        interaction: { hover: true },
    };

    async function renderPathGraph() {
        const res = await fetch(`/api/path?a=${encodeURIComponent(NAME_A)}&b=${encodeURIComponent(NAME_B)}`);
        const data = await res.json();

        if (!data.nodes.length) {
            document.getElementById("graph-loading").textContent = "No path found.";
            return;
        }

        // Style nodes by group
        data.nodes.forEach(node => {
            if (node.group === "person") {
                node.shape = "dot";
                node.size = 24;
                node.color = PERSON_COLOR;
                node.font = { color: "#a0a8d4", face: "DM Sans", size: 14, strokeWidth: 0 };
            } else {
                node.shape = "box";
                node.size = 18;
                node.color = MOVIE_COLOR;
                node.font = { color: "#f5c518", face: "DM Sans", size: 14, strokeWidth: 0 };
            }
        });

        const container = document.getElementById("neovis-graph");
        const network = new vis.Network(
            container,
            { nodes: new vis.DataSet(data.nodes), edges: new vis.DataSet(data.edges) },
            options
        );

        network.once("stabilized", () => {
            document.getElementById("graph-loading").style.display = "none";
            container.style.display = "block";
        });
    }

    renderPathGraph();
});