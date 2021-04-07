import asyncio

import pandas as pd
import aiohttp
from time import mktime
import mwparserfromhell as mw

from datetime import datetime
from lxml import html
from mwclient import Site
from .revision import Revision


def get_users(metadata):
    """
    Pull users, handles hidden user errors
    Parameters:
        metadata: sheet of metadata from mwclient
    Returns:
        the list of users
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
    Parameters:
        metadata: sheet of metadata from mwclient
    Returns:
        list of True/False representing whether an edit is minor
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
    Parameters:
        metadata: sheet of metadata from mwclient
    Returns:
        The comments as a list
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
    Parameters:
        talk: set of talk pages from metadata
    Returns:
        The ratings and timestamps for a page
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


async def get_text(revid, attempts=0):
    """
    Pull plain text representation of a revision from API
    Parameters:
        revid: revision id of a page
        attempts: The number of attempts at retrieving the id so far
    """
    try:
        # async implementation of requests get
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://wikipedia.org/w/api.php",
                params={
                    "action": "parse",
                    "format": "json",
                    "oldid": revid,
                },
            ) as resp:
                response = await resp.json()
    # request errors from server
    except:
        if attempts == 10:
            return -1
        # If there's a server error, just re-send the request until the server complies
        return await get_text(revid, attempts=attempts + 1)
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

    Parameters:
        revids: A list of revids (type int) correlating to article revisions
    Returns:
        The text for each revision id
    """
    # Container for the revision texts
    texts = []

    # Gather body content of all revisions (asynchronously)
    sema = 100
    for i in range(0, revids.__len__(), +sema):
        texts += await asyncio.gather(
            *(get_text(revid) for revid in revids[i : (i + sema)])
        )
    return texts


def get_history(title, include_text=True):
    """
    Collects everything and returns a list of Change objects

    Parameters:
        title: article title
        include_text: Whether to unclude body text or not. Speed increases if False
    Returns:
        A list of Change objects representing each revision to the
    """

    # Load the article
    site = Site("en.wikipedia.org")
    try:
        page = site.pages[title]
    except:
        return -1
    try:
        talk = site.pages["Talk:" + title]
    except:
        return -1
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

        change = Revision(
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


def to_df(changes):
    """
    Make a dataframe out of the change objects

    Parameters:
        changes: A list of changes
    Returns:
        A DataFrame representation of the changes
    """
    df = []

    for change in changes:
        row = dict(
            title=change.title,
            time=change.time,
            revid=change.revid,
            kind=change.kind,
            user=change.user,
            comment=change.comment,
            rating=change.rating,
            text=change.content,
        )
        df.append(row)
    return pd.DataFrame(df)
