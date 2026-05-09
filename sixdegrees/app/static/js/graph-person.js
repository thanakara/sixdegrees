/**
 * Renders the ego-network for a person page with click-to-expand.
 * Config is read from data-* attributes on #neovis-graph.
 */

const _el = document.getElementById("neovis-graph");
const NEO4J_URI = _el.dataset.uri;
const NEO4J_USER = _el.dataset.user;
const NEO4J_PASSWORD = _el.dataset.password;
const PERSON_ID = _el.dataset.personId;

const expanded = new Set();

const config = {
    containerId: "neovis-graph",
    neo4j: {
        serverUrl: NEO4J_URI,
        serverUser: NEO4J_USER,
        serverPassword: NEO4J_PASSWORD,
    },
    visConfig: {
        nodes: {
            font: {
                size: 14,
                face: "DM Sans",
                strokeWidth: 0,
                strokeColor: "transparent",
            },
        },
        edges: {
            color: { color: "#555", highlight: "#f5c518" },
            font: {
                color: "#888",
                face: "DM Mono",
                size: 10,
                align: "middle",
                strokeWidth: 0,
                strokeColor: "transparent",
            },
            width: 1.5,
            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
        },
        physics: {
            enabled: true,
            solver: "forceAtlas2Based",
            forceAtlas2Based: {
                gravitationalConstant: -40,
                springLength: 120,
                springConstant: 0.08,
            },
            stabilization: { iterations: 150 },
        },
        interaction: { hover: true, clickToUse: false },
        autoResize: true,
    },
    labels: {
        Person: { label: "name" },
        Movie: { label: "title" },
    },
    relationships: {
        ACTED_IN: { label: "ACTED_IN" },
        DIRECTED: { label: "DIRECTED" },
    },
    initialCypher: `
    MATCH (p:Person {person_id: "${PERSON_ID}"})-[r:ACTED_IN|DIRECTED]->(m:Movie)
    RETURN p, r, m
  `,
};

function styleNodes(viz) {
    const updates = [];
    viz.nodes.getIds().forEach(id => {
        const node = viz.nodes.get(id);
        const labels = node.raw && node.raw.labels ? node.raw.labels : [];

        if (labels.includes("Person")) {
            updates.push({
                id,
                shape: "dot",
                size: 24,
                color: {
                    background: "#1a1a2e",
                    border: "#a0a8d4",
                    highlight: { background: "#20203e", border: "#f5c518" },
                },
                font: { color: "#a0a8d4", size: 14, face: "DM Sans", strokeWidth: 0 },
            });
        } else if (labels.includes("Movie")) {
            const movieId = node.raw.properties.movie_id;
            const isExpanded = expanded.has(movieId);
            updates.push({
                id,
                shape: "box",
                size: 18,
                color: {
                    background: isExpanded ? "#1a2a00" : "#2a1a00",
                    border: isExpanded ? "#6fcf4a" : "#f5c518",
                    highlight: { background: "#3d2800", border: "#fff" },
                },
                font: {
                    color: isExpanded ? "#6fcf4a" : "#f5c518",
                    size: 14,
                    face: "DM Sans",
                    strokeWidth: 0,
                },
            });
        }
    });
    viz.nodes.update(updates);
}

function styleEdges(viz) {
    const updates = [];
    viz.edges.getIds().forEach(id => {
        const edge = viz.edges.get(id);
        const type = edge.raw && edge.raw.type ? edge.raw.type : "";
        updates.push({
            id,
            label: type === "ACTED_IN" ? "ACTED IN" : type,
            font: { color: "#666", size: 10, face: "DM Mono", strokeWidth: 0, strokeColor: "transparent", align: "middle" },
            color: { color: "#444", highlight: "#f5c518" },
            dashes: type === "DIRECTED",
            width: type === "DIRECTED" ? 2 : 1.5,
        });
    });
    viz.edges.update(updates);
}

const viz = new NeoVis.default(config);

viz.registerOnEvent(NeoVis.NeoVisEvents.CompletionEvent, () => {
    styleNodes(viz);
    styleEdges(viz);
    document.getElementById("graph-loading").style.display = "none";
    document.getElementById("neovis-graph").style.display = "block";
});

// Register click handler once after first render
let clickRegistered = false;
viz.registerOnEvent(NeoVis.NeoVisEvents.CompletionEvent, () => {
    if (clickRegistered) return;
    clickRegistered = true;

    viz.network.on("click", params => {
        if (!params.nodes.length) return;

        const nodeId = params.nodes[0];
        const node = viz.nodes.get(nodeId);
        if (!node) return;

        const labels = node.raw && node.raw.labels ? node.raw.labels : [];
        if (!labels.includes("Movie")) return;

        const movieId = node.raw.properties.movie_id;
        if (expanded.has(movieId)) return;

        expanded.add(movieId);

        viz.updateWithCypher(`
      MATCH (m:Movie {movie_id: "${movieId}"})<-[r:ACTED_IN|DIRECTED]-(co:Person)
      RETURN m, r, co
    `);
    });
});

viz.render();