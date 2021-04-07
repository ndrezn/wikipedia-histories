"""
Network builder
In the generated graph: Each node represents an article, and each edge represents whether
the connected nodes share an editor. The weight of the edges is the number of users who edited
both articles.

for instance, if three total users edited both "The Dark Knight" and "Game of Thrones", then there is an
edge between those two nodes with a weight of three.
"""
import random
import os

import pandas as pd
import networkx as nx


def get_documents(domain, size, metadata_path):
    """
    Sample an equal number of articles from two different domains
    :param domain: can be 'sciences', 'sports', 'politics', or 'culture'
    :param size: The number of documents to collect
    :param metadata_path: The path to the metadata sheet
    """

    df = pd.read_csv(metadata_path)

    # pick two random submediums from which to draw documents if we're picking from all
    # (e.g. ('democrat', 'biology') or ('republican', 'democrat'))
    if domain is not None:
        df = df.loc[df["Domain"] == domain]
        selected_categories = random.sample(df["Category"].unique().tolist(), 2)

    else:
        # Select two categories from different domains
        domains = random.sample(df["Domain"].unique().tolist(), 2)
        df = df.loc[df["Domain"].isin(domains)]

        dff = df.groupby("Domain")
        selected_categories = []
        for name, group in dff:
            cat = random.choice(group["Category"].unique().tolist())
            selected_categories.append(cat)

    # clear out rows of the dataframe which don't match the selected types
    container = pd.DataFrame()
    for c in selected_categories:
        cur = df.loc[df["Category"] == c]
        cur = cur.sample(n=int(size / 2))
        container = pd.concat([container, cur])

    return container


def get_users(name, domain, path):
    """
    Get the list of users for an article given the dataframe

    :param name: the name of an article
    :param domain: the domain the article is a member of
    """
    fpath = "{}/{}/{}.csv".format(path, domain, name)

    if os.path.exists(fpath):
        df = pd.read_csv(fpath)
        return list(df["User"])

    # In case the data isn't there
    return None


def intersection(lst1, lst2):
    """
    Get the intersection of two lists, O(n) time
    """

    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def build_graph(df, path):
    """
    Get the list of users for every article selected by the document selector

    :param df: A dataframe of selected articles (equal numbers from each domain)
    """
    df["Users"] = df.apply(
        lambda row: get_users(row["Pages"], row["Domain"], path), axis=1
    )  # get the user lists for each page

    df = df.dropna(subset=["Users"])

    g = nx.Graph()
    # one node for every novel/film/tv
    g.add_nodes_from(list(df["Pages"]))

    attrs = {}
    for i, row in df.iterrows():
        attrs[row["Pages"]] = {"domain": row["Domain"], "category": row["Category"]}

    nx.set_node_attributes(g, attrs)

    for i1, row1 in df.iterrows():  # iterate through all nodes and user lists
        node1 = row1["Pages"]
        users1 = row1["Users"]
        for i2, row2 in df.iterrows():  # iterate through all other nodes and user lists
            node2 = row2["Pages"]
            if node1 != node2:
                users2 = row2["Users"]
                if not g.has_edge(
                    node1, node2
                ):  # if there is not an edge between the two nodes
                    common_users = intersection(users1, users2)  # get the common users
                    if len(common_users) != 0:
                        g.add_edge(
                            node1, node2, weight=len(common_users)
                        )  # add an edge to the network with a weight of the common users

    return g


def generate_networks(
    count=50,
    size=100,
    domain=None,
    write=False,
    output_path=None,
    metadata_path=None,
    articles_path=None,
):
    """
    Generate networks for a set of mediums

    :param count: The number of articles to be referenced
    """
    graphs = []
    for i in range(0, count):
        documents = get_documents(domain, size, metadata_path)
        g = build_graph(documents, articles_path)

        if write:
            if not os.path.isdir("{}/{}/".format(output_path, domain)):
                os.makedirs("{}/{}/".format(output_path, domain))
            out = "{}/{}/{}.GraphML".format(output_path, domain, str(i))
            nx.write_graphml(g, out)
        graphs.append(g)

    return graphs
