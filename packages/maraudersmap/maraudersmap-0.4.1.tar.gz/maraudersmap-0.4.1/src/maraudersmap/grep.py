import networkx as nx
from maraudersmap.score import get_leaves, get_routine_content
from maraudersmap.nx_utils import get_root_from_tree


def analyze_grep_pragma(
    pattern, graph: nx.DiGraph, routine: list, leaf_name: str
) -> nx.DiGraph:
    """
    Look for the presence of a pragma grep, if it's there then the grep coverage will be 1.

    Args:
        graph (obj): NetworkX DiGraph
        routine (list): List of routine lines
        leaf_name (str): Name of the leaf

    Returns:
        Update the current graph leaves with the grep key
    """

    for line in routine:
        graph.nodes[leaf_name]["grep"] = 0
        if pattern in line.strip():
            graph.nodes[leaf_name]["grep"] = 1
            break

    return graph


def _rec_inherit_grep_cov(graph: nx.DiGraph, root: str) -> None:
    """
    Recursive addition of grep coverage pourcentage per node starting from the root of the graph

    Args:
        graph (obj): networkX DiGraph
        root (str): name of the root node

    Returns:
        Update the current graph by adding the grep coverage
    """
    succ = list(graph.successors(root))
    if succ:
        grep_cov = 0
        for child in succ:
            _rec_inherit_grep_cov(graph, child)
            grep_cov += graph.nodes[child]["grep"]

        grep_cov /= len(succ)
        graph.nodes[root]["grep"] = grep_cov


def build_covgraph(pattern, graph: nx.DiGraph, leaves: list) -> nx.DiGraph:
    """ """
    for leaf in leaves:
        graph.nodes[leaf]["grep"] = 0
        if graph.nodes[leaf].get("analyzed", True) and not graph.nodes[leaf].get(
            "empty_folder", False
        ):
            # analyze pragma
            routine_content = get_routine_content(
                graph.nodes[leaf]["path"],
                graph.nodes[leaf]["line_start"],
                graph.nodes[leaf]["line_end"],
            )

            graph = analyze_grep_pragma(pattern, graph, routine_content, leaf)

    root_node = get_root_from_tree(graph)
    _rec_inherit_grep_cov(graph, root_node)

    return graph


def get_grep_coverage(pattern, graph: nx.DiGraph) -> nx.DiGraph:
    """
    Compute the grep coverage graph by looking for grep pragma inside the routines
    based on the tree function analysis of maraudersmap

    Args:
        graph (obj): networkX DiGraph

    Returns:
        grep_cov_graph (obj) networkX DiGraph with grep coverage computed
    """
    leaves = get_leaves(graph)
    grep_cov_graph = build_covgraph(pattern, graph, leaves)
    return grep_cov_graph
