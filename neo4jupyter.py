import os
import json
import uuid
import tempfile
from IPython.display import HTML, Javascript, display

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
        Javascript(data="require.config({ " +
                        "    paths: { " +
                        "        vis: '//cdnjs.cloudflare.com/ajax/libs/vis/4.8.2/vis.min' " +
                        "    } " +
                        "}); " +
                        "require(['vis'], function(vis) { " +
                        " window.vis = vis; " +
                        "}); ",
                   css='https://cdnjs.cloudflare.com/ajax/libs/vis/4.8.2/vis.css')
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
    MATCH (n)
    WITH n, rand() AS random
    ORDER BY random
    LIMIT $limit
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n AS source_node,
           id(n) AS source_id,
           r,
           m AS target_node,
           id(m) AS target_id
    """

    data = graph.run(query, limit=limit)

    nodes = []
    edges = []

    def get_vis_info(node, id):
        node_label = list(node.labels)[0]
        prop_key = options.get(node_label)
        vis_label = node.get(prop_key, "")

        return {"id": id, "label": vis_label, "group": node_label, "title": repr(node)}

    for row in data:
        source_node = row[0]
        source_id = row[1]
        rel = row[2]
        target_node = row[3]
        target_id = row[4]

        source_info = get_vis_info(source_node, source_id)

        if source_info not in nodes:
            nodes.append(source_info)

        if rel is not None:
            target_info = get_vis_info(target_node, target_id)

            if target_info not in nodes:
                nodes.append(target_info)

            edges.append({"from": source_info["id"], "to": target_info["id"], "label": rel.__class__.__name__})

    return vis_network(nodes, edges, physics=physics)

def get_vis_edge_info(r):
    return({"from": id(r.start_node), "to": id(r.end_node), "label": r.__class__.__name__ })

##calculate the dict that will represent a node.
def get_vis_node_info(node, options):
    node_label = list(node.labels)[0]
    prop_key = options.get(node_label)
    vis_label = dict(node).get(prop_key, "")
    
    return {"id": id(node), "label": vis_label, "group": node_label, "title": repr(node)}

def draw_subgraph(subgraph, options, physics=True, limit=100):
    """
    The options argument should be a dictionary of node labels and property keys; it determines which property
    is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    Omitting a node label from the options dict will leave the node unlabeled in the visualization.
    Setting physics = True makes the nodes bounce around when you touch them!
    :param subgraph: Subgaph containing nodes and relationships to plot.
    :param options: Options for the Nodes.
    :param physics: Physics of the vis.js visualization.
    :return: IPython.display.HTML
    """

    nodes = [get_vis_node_info(n,options) for n in subgraph.nodes]
    edges = [get_vis_edge_info(r) for r in subgraph.relationships]
    return vis_network(nodes, edges, physics=physics)
