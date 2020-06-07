import pandas as pd
from progress.bar import IncrementalBar
import wikipedia_histories
import time
import os
import threading


def get_article(page, domain, path):
    cur = wikipedia_histories.get_history(page, include_text=False)
    if cur == -1:
        return -1
    dff = wikipedia_histories.build_df(cur)
    dff.to_csv(path + domain + "/" + page + ".csv")
    return 1


def download_articles(df, path):

    for page, domain in zip(df["Pages"], df["Domain"]):
        try:
            dff = get_article(page, domain, path)
        except:
            continue

    return 1


def categories():
    sciences = [
        "Category:Branches_of_biology",
        "Category:Fields_of_mathematics",
        "Category:Concepts_in_physics",
        "Category:Chemistry",
    ]
    sports = [
        "Category:Ice_hockey_in_the_United_States",
        "Category:American_football_in_the_United_States",
        "Category:Basketball_in_the_United_States",
        "Category:Baseball_in_the_United_States",
    ]
    culture = [
        "Category:Television_in_the_United_States",
        "Category:American_films",
        "Category:American_novels",
    ]
    politics = [
        "Category:Conservatism",
        "Category:Liberalism",
    ]
    domains = {
        "sciences": sciences,
        "sports": sports,
        "culture": culture,
        "politics": politics,
    }

    return domains

    # df = wikipedia_histories.get_article_titles(domains)


def check_for_files(df):
    print(len(df))
    path = "/Users/ndrezn/Documents/Github/txtLab/results/data2/sampled/"
    cur = []
    for record in df.to_dict("records"):
        cur_path = path + "{}/{}.csv".format(record["Domain"], record["Pages"])

        if os.path.exists(cur_path):
            cur.append(record)

    df = pd.DataFrame(cur)
    print(len(df))
    return df


def count_files():
    path = "/Users/ndrezn/Documents/Github/txtLab/results/data2/sampled/"
    total = 0
    for dire in os.listdir(path):
        if not dire.startswith("."):
            total += len(os.listdir(path + dire))
    print(total)


df = pd.read_csv("/Users/ndrezn/Documents/Github/txtLab/results/data2/sampled.csv")


# df = check_for_files(df)
check_for_files(df)
exit()
samples = []


# df = pd.read_csv("/Users/ndrezn/Documents/Github/txtLab/results/data2/sampled2.csv")


cts = {"culture": 227, "politics": 572, "sciences": 900, "sports": 928}
dfs = []
for name, group in df.groupby("Category"):
    dfs.append(group.sample(cts[name]))
df = pd.concat(dfs)
df.to_csv("/Users/ndrezn/Documents/Github/txtLab/results/data2/sampled2.csv")
print(len(df))


s = time.time()
step = len(df) // 10

threads = []
for i in range(0, len(df), step):
    cur = df[i : i + step]
    t = threading.Thread(target=download_articles, args=(cur, path))
    threads.append(t)

for t in threads:
    t.start()
for t in threads:
    t.join()

e = time.time()

print(e - s)
