"""
Example workflow for downloading a set of articles associated with a set of domains, 
represented by categories
"""


import os
import pandas as pd
from progress.bar import IncrementalBar
import wikipedia_histories


def find_articles(domains):
    """
    Download a list of articles titles associated with a domain
    """
    df = wikipedia_histories.find_articles(domains, max_level=2)
    return df


def get_article(title):
    """
    Given an article title, download the article and return it as a DataFrame
    """
    cur = wikipedia_histories.get_history(title, include_text=False)
    if cur == -1:
        return -1
    df = wikipedia_histories.build_df(cur)
    return df


def download_articles(df, output_path):
    """
    Download a list of articles based on the find_articles function
    """
    for page, domain in zip(df["Pages"], df["Domain"]):
        df = get_article(page)
        # If there was an error in collecting the DataFrame
        if df == -1:
            continue
        domain_output = "{}/{}".format(output_path, domain)
        if not os.path.isdir(domain_output):
            os.makedirs(domain_output)

        df.to_csv("{}/{}.csv".format(domain_output, page))

    return 1


def aggregate_metadata(mediums, files_path):
    """
    Aggregate metadata for the articles
    """
    df = []
    for medium in mediums:
        directory = "{}/{}/".format(files_path, medium)
        files = os.listdir(directory)
        bar = IncrementalBar(medium + "... ", max=len(files))

        for file in files:
            bar.next()
            page = pd.read_csv(directory + file)

            try:
                row = wikipedia_histories.get_metadata(page, file.split(".")[0])
            except:
                continue
            row["medium"] = medium
            df.append(row)
        bar.finish()

    df = pd.DataFrame(df)
    return df
