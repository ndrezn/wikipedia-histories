"""
Container for Change object
"""


class Revision:
    """
    Class to track data about each change of a page
    """

    def __init__(self, index, title, time, revid, kind, user, comment, rating, content):
        """
        Create a change object

        :param index: edit level
        :param title: page title
        :param time: time the edit was made
        :param revid: the id number of the revision
        :param kind: minor or non-minor edit
        :param user: the user who made the edit
        :param comment: the comment attached to the edit
        :param class: the quality of the edit
        :param content: the content of the edit, i.e. the text
        """
        self.index = index
        self.title = title
        self.time = time
        self.revid = revid
        self.kind = kind
        self.user = user
        self.comment = comment
        self.rating = rating
        self.content = content

    def __str__(self):
        return str(self.revid)

    def __repr__(self):
        return str(self.revid)
