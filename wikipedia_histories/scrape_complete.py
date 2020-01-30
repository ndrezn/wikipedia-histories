from mwclient import Site
import mwparserfromhell as mw
import os
import requests
from lxml import html
from time import mktime
from datetime import datetime
import asyncio
import aiohttp
import json
from Change import Change
import pandas as pd


# Pull users, handles hidden user errors
# Input: sheet of metadata from mwclient
# Output:
def get_users(metadata):
    users = []
    for rev in metadata:
        try:
            users.append(rev["user"])
        except (KeyError):
            users.append(None)
    return users


# Pull edit types (minor or not), handles untagged edits
# Input: sheet of metadata from mwclient
# Output: list of booleans representing whether each revision
# of an article was tagged as minor or not
def get_kind(metadata):
    kind = []
    for rev in metadata:
        if "minor" in rev:
            kind.append(True)
        else:
            kind.append(False)
    return kind


# Check for comments
# Input: sheet of metadata from mwclient
def get_comment(metadata):
    comment = []
    for rev in metadata:
        try:
            comment.append(rev["comment"])
        except (KeyError):
            comment.append("")
    return comment


# Output classes of a page to a list (FA, good, etc.) given a talk page
# Input: set of talk pages from metadata
def get_ratings(talk):
    timestamps = [rev["timestamp"] for rev in talk.revisions()]
    ratings = []
    content = []

    for cur in talk.revisions(prop="content"):
        if cur.__len__() is 1:
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


# Pull plain text representation of a revision from API
# Input: revision id of a page, 0 (initial attempt at pulling the page)
async def get_text(revid, attempts):
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
        if attempts is 10:
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


# Overall function
# Input: article title
# Output: complete list of histories as a json type
# If count_skipped is true, also returns a tuple containing
# the page history and the number of skipped pages
async def compile_edits(title, count_skipped):
    # Load the article
    site = Site("en.wikipedia.org")
    page = site.pages[title]
    talk = site.pages["Talk:" + title]
    ratings = get_ratings(talk)

    # Collect metadata information
    metadata = [rev for rev in page.revisions()]
    users = get_users(metadata)
    kind = get_kind(metadata)
    comments = get_comment(metadata)

    revids = []
    history = []

    # Collect list of revision ids using the metadata pull
    for i in range(0, metadata.__len__()):
        revids.append(metadata[i]["revid"])

    # Container for the revision texts
    texts = []

    # Gather body content of all revisions (asynchronously)
    sema = 100
    for i in range(0, metadata.__len__(), +sema):
        texts += await asyncio.gather(
            *(get_text(revid, 0) for revid in revids[i : (i + sema)])
        )

    # Initialize counter for the number of skipped pages
    j = 0

    # Iterate backwards through our metadata and put together the list of change items
    for i in range(metadata.__len__() - 1, -1, -1):

        # Count deleted pages
        if texts[i] is None:
            j += 1

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

    if count_skipped:
        return (history, j)
    else:
        return history

def build_json(changes):
    jsonified = []
    for item in changes:
        jsonified+=item.make_json()

    return jsonified


# Takes input as a list of changes and a 
def build_df(changes):
    df = pd.DataFrame(columns=['Title','Time','Revid','Kind','User','Comment', 'Rating', 'Content'])
    i = 0
    for change in changes:
        df.loc[i] = [change.title, change.time, change.revid, change.kind, change.user, change.comment, change.rating, change.content]
        i+=1
    return df


def get_history(title, count_skipped=False):
    return asyncio.run(compile_edits(title, count_skipped))

serpent = get_history('Golden swallow')
print(serpent)

