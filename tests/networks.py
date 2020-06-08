import wikipedia_histories
import threading
import time
import pandas as pd
import os
from progress.bar import IncrementalBar
import matplotlib.pyplot as plt
import seaborn as sns

paper = ["#80d3dc", "#f9a43f", "#fde28b", "#ec1b30"]
paper = sns.color_palette(paper)


METADATA_PATH = "/Users/ndrezn/sampled.csv"
NETWORKS_PATH = "/Users/ndrezn/scrape/networks"
FILES_PATH = "/Users/ndrezn/scrape/sampled"
NETWORK_METADATA_PATH = (
    "/Users/ndrezn/Documents/Github/txtLab/results/data2/networks_metadata.csv"
)
SAMPLED_METADATA_PATH = (
    "/Users/ndrezn/Documents/Github/txtLab/results/data2/sampled_metadata.csv"
)
MEDIUMS = ["sciences", "culture", "politics", "sports"]


def build_networks(mediums):
    s = time.time()

    wikipedia_histories.generate_networks(
        1000, 300, NETWORKS_PATH, METADATA_PATH, FILES_PATH, mediums=mediums
    )
    e = time.time()
    print(e - s)


def threaded_build_networks():
    s = time.time()

    threads = []

    count = 1000
    size = 300
    num_threads = 10

    for i in range(0, count, (count // num_threads)):
        t = threading.Thread(
            target=wikipedia_histories.generate_networks,
            args=(
                (count // num_threads),
                size,
                OUTPUT_PATH,
                METADATA_PATH,
                FILES_PATH,
                i,
            ),
        )
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    e = time.time()

    print(e - s)


def analyze_networks():
    df = wikipedia_histories.get_clustering(NETWORKS_PATH)
    df.to_csv(NETWORK_METADATA_PATH)


def get_meta(mediums, files_path):
    df = []
    for medium in mediums:
        directory = "{}/{}/".format(files_path, medium)
        files = os.listdir(directory)
        bar = IncrementalBar(medium + "... ", max=len(files))

        for file in files:
            bar.next()
            page = pd.read_csv(directory + file)

            try:
                row = wikipedia_histories.get_meta(page, file.split(".")[0])
            except:
                continue
            row["medium"] = medium
            df.append(row)
        bar.finish()

    df = pd.DataFrame(df)
    return df


def visualizer(network_meta):
    df = pd.read_csv(network_meta)

    sns.set_palette(sns.color_palette("YlGn", 10))
    print(df.columns)
    ax = sns.boxplot(data=df, x="medium", y="unique_editors", palette=paper)

    plt.show()


def aggregate(df):
    # df["edits_per_user"] = df["edit_count"] / df["unique_editors"]
    # df["article_age_hours"] = df["article_age_hours"] / (24 * 365)
    print(
        df.groupby("medium").mean()
        # ["edit_count", "article_age_hours", "unique_editors", "edits_per_user"]
        # ].mean()
    )


# df = get_meta(MEDIUMS, FILES_PATH)
# df.to_csv(SAMPLED_METADATA_PATH)
# visualizer(NETWORK_METADATA_PATH)
df = pd.read_csv(SAMPLED_METADATA_PATH)
visualizer(df)
