import wikipedia_histories
import threading
import time


METADATA_PATH = "/Users/ndrezn/Documents/Github/txtLab/results/data2/sampled.csv"
NETWORKS_PATH = "/Users/ndrezn/Documents/Github/txtLab/results/data2/networks"
FILES_PATH = "/Users/ndrezn/Documents/Github/txtLab/results/data2/sampled"


def build_networks(mediums):
    s = time.time()

    wikipedia_histories.generate_networks(
        2, 300, NETWORKS_PATH, METADATA_PATH, FILES_PATH, mediums=mediums
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
    print(df)


build_networks(["all"])
