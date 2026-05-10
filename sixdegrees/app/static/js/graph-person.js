/**
 * Renders ego network for a person page with click-to-expand.
 * Fetches data from /api/person/<id>/graph and /api/movie/<id>/expand.
 */
document.addEventListener("DOMContentLoaded", () => {
    const _el = document.getElementById("neovis-graph");
    if (!_el) return;

    const PERSON_ID = _el.dataset.personId;

    const PERSON_COLOR = { background: "#1a1a2e", border: "#a0a8d4", highlight: { background: "#20203e", border: "#f5c518" } };
    const MOVIE_COLOR = { background: "#2a1a00", border: "#f5c518", highlight: { background: "#3d2800", border: "#ffffff" } };
    const EXPANDED_COLOR = { background: "#1a2a00", border: "#6fcf4a", highlight: { background: "#253d00", border: "#ffffff" } };

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
                springLength: 120,
                springConstant: 0.08,
            },
            stabilization: { iterations: 150 },
        },
        interaction: { hover: true },
    };

    function styleNode(node) {
        if (node.group === "person") {
            return { ...node, shape: "dot", size: 24, color: PERSON_COLOR, font: { color: "#a0a8d4", face: "DM Sans", size: 14, strokeWidth: 0 } };
        }
        return { ...node, shape: "box", size: 18, color: MOVIE_COLOR, font: { color: "#f5c518", face: "DM Sans", size: 14, strokeWidth: 0 } };
    }

    async function renderPersonGraph() {
        const res = await fetch(`/api/person/${PERSON_ID}/graph`);
        const data = await res.json();

        const nodesDS = new vis.DataSet(data.nodes.map(styleNode));
        const edgesDS = new vis.DataSet(data.edges);
        const expanded = new Set();

        const container = document.getElementById("neovis-graph");
        const network = new vis.Network(container, { nodes: nodesDS, edges: edgesDS }, options);

        network.once("stabilized", () => {
            document.getElementById("graph-loading").style.display = "none";
            container.style.display = "block";
        });

        // Click to expand movie nodes
        network.on("click", async params => {
            if (!params.nodes.length) return;

            const nodeId = params.nodes[0];
            const node = nodesDS.get(nodeId);
            if (!node || node.group !== "movie") return;

            const movieId = node.movie_id;
            if (!movieId || expanded.has(movieId)) return;
            expanded.add(movieId);

            // Mark as expanded
            nodesDS.update({ id: nodeId, color: EXPANDED_COLOR, font: { color: "#6fcf4a", face: "DM Sans", size: 14, strokeWidth: 0 } });

            const res = await fetch(`/api/movie/${movieId}/expand`);
            const data = await res.json();

            // Add new nodes and edges — skip ones already in the graph
            const existingIds = new Set(nodesDS.getIds());
            const newNodes = data.nodes
                .filter(n => !existingIds.has(n.id))
                .map(styleNode);

            const existingEdges = new Set(edgesDS.getIds());
            const newEdges = data.edges.filter(e => !existingEdges.has(e.id));

            nodesDS.add(newNodes);
            edgesDS.add(newEdges);
        });
    }

    renderPersonGraph();
});