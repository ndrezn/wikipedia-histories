import pandas as pd
from progress.bar import IncrementalBar
import wikipedia_histories
import time


def download_articles(df,):
    bar = IncrementalBar("Downloading articles... ", max=len(df))

    dfs = {}
    for page, domain in zip(df["Pages"], df["Domain"]):
        bar.next()

        try:
            cur = wikipedia_histories.get_history(page, include_text=False)
            dff = wikipedia_histories.build_df(cur)
            dfs[domain + "/" + page + ".csv"] = dff
        except Exception as e:
            print(e)

    bar.finish()

    return dfs


# sciences = [
#     "Category:Branches_of_biology",
#     "Category:Fields_of_mathematics",
#     "Category:Concepts_in_physics",
#     "Category:Chemistry",
# ]
# sports = [
#     "Category:Ice_hockey_in_the_United_States",
#     "Category:American_football_in_the_United_States",
#     "Category:Basketball_in_the_United_States",
#     "Category:Baseball_in_the_United_States",
# ]
# culture = [
#     "Category:Television_in_the_United_States",
#     "Category:American_films",
#     "Category:American_novels",
# ]
# politics = [
#     "Category:Conservatism",
#     "Category:Liberalism",
# ]
# domains = {
#     "sciences": sciences,
#     "sports": sports,
#     "culture": culture,
#     "politics": politics,
# }

# df = wikipedia_histories.get_article_titles(domains)

# df = pd.read_csv("/Users/ndrezn/Documents/Github/txtLab/results/data2/articles2.csv")

# samples = []
# for name, group in df.groupby("Domain"):
#     minimum = group["Category"].value_counts().min()

#     for name2, group2 in group.groupby("Category"):
#         samples.append(group2.sample(minimum))


# df = pd.concat(samples)
df = pd.read_csv(
    "/Users/ndrezn/Documents/Github/txtLab/results/data2/sampled.csv"
).head(5)
dfs = download_articles(df)
path = "/Users/ndrezn/Documents/Github/txtLab/results/data2/articles"
for df in dfs:
    dfs[df].to_csv(path + "/" + df)
