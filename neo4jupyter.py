import os
import json
import uuid
import tempfile
from IPython.display import HTML, display

DEFAULT_PHYSICS = {
    "physics": {
        "barnesHut": {
            "gravitationalConstant": -15150,
            "centralGravity": 3.45,
            "springLength": 261,
            "damping": 0.3
        }
    }
}


def get_visjs():
    return


def init_notebook_mode():
    """
    Creates a script tag and prints the JS read from the file in the tag.
    """
    display(
        HTML("<script type='text/javascript'> define('vis', function(require, exports, module) {" +
             open(os.path.join(os.path.dirname(__file__), 'assets/vis.min.js')).read() +
             "}); require(['vis'], function(vis) { window.vis = vis; }); </script>")
        )


def vis_network(nodes, edges, physics=True):
    """
    Creates the HTML page with all the parameters
    :param nodes: The nodes to be represented an their information.
    :param edges: The edges represented an their information.
    :param physics: The options for the physics of vis.js.
    :return: IPython.display.HTML
    """
    base = open(os.path.join(os.path.dirname(__file__), 'assets/index.html')).read()

    unique_id = str(uuid.uuid4())
    html = base.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges), physics=json.dumps(physics))

    # Stores the HTML to show at /tmp folder
    filename = os.path.join(tempfile.gettempdir(), "graph-{}.html".format(unique_id))

    with open(filename, "w") as final_file:
        final_file.write(html)

    return HTML(html)


def draw(graph, options, physics=True, limit=100):
    """
    The options argument should be a dictionary of node labels and property keys; it determines which property
    is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    Omitting a node label from the options dict will leave the node unlabeled in the visualization.
    Setting physics = True makes the nodes bounce around when you touch them!

    :param graph: Connection to the DB where the query will be executed.
    :param options: Options for the Nodes.
    :param physics: Physics of the vis.js visualization.
    :param limit: Maximum number of Nodes or Edges.
    :return: IPython.display.HTML
    """

    query = """
        MATCH n
        WITH n, RAND() AS random
        ORDER BY random LIMIT {limit}
        OPTIONAL MATCH (n)-[r]->(m)
        RETURN n, r, m
    """

    data = graph.cypher.execute(query, limit=limit)

    nodes = []
    edges = []

    def get_vis_info(node):
        node_label = list(node.labels)[0]
        prop_key = options.get(node_label)
        vis_label = node.properties.get(prop_key, "")
        vis_id = node.ref.split("/")[1]

        title = {}

        for key, value in node.properties.items():
            title[key] = value

        return {"id": vis_id, "label": vis_label, "group": node_label, "title": repr(title)}

    for row in data:
        source = row[0]
        rel = row[1]
        target = row[2]

        source_info = get_vis_info(source)

        if source_info not in nodes:
            nodes.append(source_info)

        if rel:
            target_info = get_vis_info(target)

            if target_info not in nodes:
                nodes.append(target_info)

            edges.append({"from": source_info["id"], "to": target_info["id"], "label": rel.type})

    return vis_network(nodes, edges, physics=physics)
