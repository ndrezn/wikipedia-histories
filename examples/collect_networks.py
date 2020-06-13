"""
Example workflow for converting a set of articles sorted by domain into
social networks based on the common editors between two articles
"""

import wikipedia_histories


def build_networks(domain, output_folder, metadata_path, articles_path):
    """
	Generates 1000 networks from a given domain, and saves those networks
	to an output folder.
	"""
    networks = wikipedia_histories.generate_networks(
        count=1000,
        size=300,
        domain=domain,
        write=True,
        output_folder=output_folder,
        metadata_path=metadata_path,
        articles_path=articles_path,
    )

    return networks


def analyze_networks(networks_path):
    """
	Given the path to networks sorted by domain, get the
	assortativity and purity scores for those networks.
	"""
    df = wikipedia_histories.get_network_metadata(networks_path)
    return df
