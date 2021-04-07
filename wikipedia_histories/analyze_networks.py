"""
Get the purity score given a network representation of an article
"""
import os
from statistics import mean
import pandas as pd

import igraph
import networkx as nx


def get_louvain(g):
    """
    LOUVAIN ALGORITHM
    This is a bottom-up algorithm: initially every vertex belongs to a separate community,
    and vertices are moved between communities iteratively in a way that maximizes the
    vertices' local contribution to the overall modularity score. When a consensus is
    reached (i.e. no single move would increase the modularity score), every community in
    the original graph is shrank to a single vertex (while keeping the total weight of the
    adjacent edges) and the process continues on the next level. The algorithm stops when it
    is not possible to increase the modularity any more after shrinking the communities to vertices.
    """
    weights = [weight for weight in g.es["weight"]]
    louvain = g.community_multilevel(weights=weights)
    return louvain


def purity(attribute, louvain, graph):
    """
    Get the average purity score for the two largest networks in a graph given an attribute to check the purity of
    Usually this attribute will be 'category'
    """
    unique_types = list({v[attribute] for v in graph.vs})
    louvain = sorted(list(louvain), key=len)[-2:]

    cur_purity = []
    for group in louvain:
        categories = []
        for node in group:
            cur = unique_types.index(graph.vs[attribute][node])
            categories.append(cur)
        count_cat0 = categories.count(0)
        count_cat1 = categories.count(1)

        cur_purity.append(max(count_cat1, count_cat0) / len(group))

    return mean(cur_purity)


def get_assortativity(file, attribute):
    """
    Get the assortativity of a graph using networkX
    """
    g = nx.read_graphml(file)

    a = nx.attribute_assortativity_coefficient(g, attribute)
    return a


def get_purity(file, attribute):
    """
    Get the purity of a graph using igraph
    """
    g = igraph.load(file)
    louv = get_louvain(g)
    p = purity(attribute, louv, g)
    return p


def get_network_metadata(
    network_path,
    attribute="category",
    mediums=["all", "culture", "sports", "politics", "sciences"],
):

    df = []
    for medium in mediums:
        directory = "{}/{}".format(network_path, medium)

        files = [
            "{}/{}/{}".format(network_path, medium, f)
            for f in os.listdir(directory)
            if not f.startswith(".")
        ]

        for file in files:
            cur = {}
            p = get_purity(file, attribute)
            a = get_assortativity(file, attribute)
            cur["assortativity"] = a
            cur["purity"] = p
            cur["medium"] = medium
            df.append(cur)

    df = pd.DataFrame(df)

    return df
