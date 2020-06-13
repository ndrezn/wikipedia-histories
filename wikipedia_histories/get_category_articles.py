"""
Given a set of categories representing domains, gather the articles emcompassed by those categories
"""

import pandas as pd
import wikipediaapi


def get_pages_of_cat(category, categorymembers, dict_of_cats, level=0, max_level=2):
    pages = []

    for c in categorymembers.values():
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            dict_of_cats = get_pages_of_cat(
                c.title,
                c.categorymembers,
                dict_of_cats=dict_of_cats,
                level=level + 1,
                max_level=max_level,
            )
        if "Category:" in c.title:
            continue
        else:
            pages.append((c.title, level))

    dict_of_cats[category] = pages
    return dict_of_cats


def find_articles(domains, max_level=2):
    wiki = wikipediaapi.Wikipedia("en")

    dfs = []
    for domain in domains:
        for category in domains[domain]:
            cat = wiki.page(category)
            d = get_pages_of_cat(category, cat.categorymembers, {}, max_level=max_level)

            for subcat in d:
                cur_df = pd.DataFrame()
                cur_df["Pages"] = [val[0] for val in d[subcat]]
                cur_df["Level"] = [val[1] for val in d[subcat]]
                cur_df["Subcategory"] = subcat
                cur_df["Category"] = category
                cur_df["Domain"] = domain

                dfs.append(cur_df)

    full_df = pd.concat(dfs)

    return full_df
