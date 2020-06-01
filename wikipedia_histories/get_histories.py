import asyncio
import aiohttp
import json
import requests
import mwparserfromhell as mw
import pandas as pd

from time import mktime
from datetime import datetime
from lxml import html
from mwclient import Site
from .change import *


def get_users(metadata):
    """
    Pull users, handles hidden user errors
    "param metadata: sheet of metadata from mwclient
    """
    users = []
    for rev in metadata:
        try:
            users.append(rev["user"])
        except (KeyError):
            users.append(None)
    return users


def get_kind(metadata):
    """
    Gather edit types (minor or not), handles untagged edits
    :param metadata: sheet of metadata from mwclient
    """
    kind = []
    for rev in metadata:
        if "minor" in rev:
            kind.append(True)
        else:
            kind.append(False)
    return kind


def get_comment(metadata):
    """
    Check for comments
    :param metadata: sheet of metadata from mwclient
    """
    comment = []
    for rev in metadata:
        try:
            comment.append(rev["comment"])
        except KeyError:
            comment.append("")
    return comment


def get_ratings(talk):
    """
    Output classes of a page to a list (FA, good, etc.) given a talk page
    :param talk: set of talk pages from metadata
    """
    timestamps = [rev["timestamp"] for rev in talk.revisions()]
    ratings = []
    content = []

    for cur in talk.revisions(prop="content"):
        if cur.__len__() == 1:
            content.append(prev)
        else:
            content.append(cur)

        prev = cur

    i = 0
    for version in content:
        try:
            templates = mw.parse(version.get("*")).filter_templates()
        except IndexError:
            continue

        rate = "NA"
        for template in templates:
            try:
                rate = template.get("class").value
                break
            except ValueError:
                continue

        rating = (rate, datetime.fromtimestamp(mktime(timestamps[i])))

        ratings.append(rating)
        i += 1

    return ratings


async def get_text(revid, attempts):
    """
    Pull plain text representation of a revision from API
    Input: revision id of a page, 0 (initial attempt at pulling the page)
    """
    try:
        # async implementation of requests get
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://wikipedia.org/w/api.php",
                params={"action": "parse", "format": "json", "oldid": revid,},
            ) as resp:
                response = await resp.json()
    # request errors from server
    except:
        if attempts == 10:
            return -1
        # If there's a server error, just re-send the request until the server complies
        return await get_text(revid, attempts + 1)
    # Check if page was deleted (deleted pages have no text and are therefore un-parsable)
    try:
        raw_html = response["parse"]["text"]["*"]
    # Page error (represents deleted pages)
    except KeyError:
        return None
    # Parse raw html from response
    document = html.document_fromstring(raw_html)
    text = document.xpath("//p")
    paragraphs = []
    for paragraph in text:
        paragraphs.append(paragraph.text_content())

    # Put everything together
    cur = "".join(paragraphs)

    return cur


async def get_texts(revids):
    """
    Get the text of articles given the list of revision ids
    """
    # Container for the revision texts
    texts = []

    # Gather body content of all revisions (asynchronously)
    sema = 100
    for i in range(0, revids.__len__(), +sema):
        texts += await asyncio.gather(
            *(get_text(revid, 0) for revid in revids[i : (i + sema)])
        )
    return texts


def get_history(title, include_text=True):
    """
    Collects everything and returns a list of Change objects
    :param title: article title
    :param include_text: Whether to unclude body text or not. Speed increases if False
    """

    # Load the article
    site = Site("en.wikipedia.org")
    page = site.pages[title]
    talk = site.pages["Talk:" + title]
    ratings = get_ratings(talk)

    # Collect metadata information
    metadata = list(page.revisions())
    users = get_users(metadata)
    kind = get_kind(metadata)
    comments = get_comment(metadata)

    revids = []

    # Collect list of revision ids using the metadata pull
    for i in range(0, metadata.__len__()):
        revids.append(metadata[i]["revid"])

    # Get the text of the revisions. Performance is improved if this isn't done, but you lose the revisions
    if include_text:
        texts = asyncio.run(get_texts(revids))
    else:
        texts = [""] * len(metadata)

    # Iterate backwards through our metadata and put together the list of change items
    history = []
    for i in range(metadata.__len__() - 1, -1, -1):
        # Iterate against talk page editions
        time = datetime.fromtimestamp(mktime(metadata[i]["timestamp"]))
        rating = "NA"

        for item in ratings:
            if time > item[1]:
                rating = item[0]
                break

        change = Change(
            i,
            title,
            time,
            metadata[i]["revid"],
            kind[i],
            users[i],
            comments[i],
            rating,
            texts[i],
        )

        # Compile the list of changes
        history.append(change)

    return history


def build_json(changes):
    """
    Make a json out of the change objects
    :param changes: A list of changes
    """
    jsonified = []
    for item in changes:
        jsonified += item.make_json()

    return jsonified


def build_df(changes):
    """
    Make a dataframe out of the change objects
    :param changes: A list of changes
    """
    df = pd.DataFrame(
        columns=[
            "Title",
            "Time",
            "Revid",
            "Kind",
            "User",
            "Comment",
            "Rating",
            "Content",
        ]
    )
    i = 0
    for change in changes:
        df.loc[i] = [
            change.title,
            change.time,
            change.revid,
            change.kind,
            change.user,
            change.comment,
            change.rating,
            change.content,
        ]
        i += 1
    return df
