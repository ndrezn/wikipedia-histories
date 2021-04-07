"""
Based on a set of downloaded articles represented as CSV's, generate a metadata for those articles.
"""

import pandas as pd
import os
from statistics import mean
import time
from datetime import datetime


def get_time_diff(prev_time, cur_time):
    try:
        if prev_time is not None and cur_time is not None:
            time_diff = cur_time - prev_time
            return time_diff.total_seconds() / 3600
        return None
    except TypeError:
        return None


def convert_to_datetime(time):
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")


def get_metadata(df, title):
    addition_lengths = []
    deletion_lengths = []
    time_diffs = []
    prev_count = 0
    prev_time = None

    prev_quality = str(df.iloc[0]["Rating"]).strip().lower()
    prev_quality_time = df.iloc[0]["Time"]
    rating_change_times = []

    df["Time"] = df["Time"].apply(convert_to_datetime)

    for i, row in df.iterrows():

        word_count = len(str(row["Content"]).split())

        if word_count < prev_count:
            deletion_lengths.append(prev_count - word_count)
        else:
            addition_lengths.append(word_count - prev_count)

        prev_count = word_count

        cur_time = row["Time"]
        # time_diff = get_time_diff(prev_time, cur_time)
        # time_diffs.append(time_diff)
        prev_time = cur_time

        # if str(row["Rating"]).strip().lower() != prev_quality or i == len(df) - 1:
        #     time_to_change = get_time_diff(prev_quality_time, cur_time)
        #     rating_change_times.append(time_to_change)
        #     prev_quality_time = cur_time
        #     prev_quality = str(row["Rating"]).strip().lower()

    age = get_time_diff(df.iloc[0]["Time"], df.iloc[len(df) - 1]["Time"])

    if not deletion_lengths:
        deletion_length = 0
    else:
        deletion_length = mean(deletion_lengths)

    row = {
        "title": title,
        "edit_count": len(df),
        "added_words_per_edit": mean(addition_lengths),
        "deleted_words_per_edit": deletion_length,
        # "hours_between_edits": mean(time_diffs),
        # "rating_change_times": mean(rating_change_times),
        "article_age_hours": age,
        "unique_editors": len(df["User"].unique()),
    }

    return row


def rating_meta(df):
    ratings = {}
    cur_ratings = df["Rating"].value_counts()

    for rating in cur_ratings.keys():
        try:
            ratings[str(rating).strip().lower()] += cur_ratings[rating]
        except Exception as e:
            ratings[str(rating).strip().lower()] = cur_ratings[rating]

    return ratings
