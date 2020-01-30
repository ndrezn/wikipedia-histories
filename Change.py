# class to track data about each change of a page
class Change:
    # edit level
    index = 0
    # page title
    title = ""
    # time edit was made
    time = 0
    # id number of revision
    revid = 0
    # minor or non-minor edit
    kind = 0
    # user who made the edit
    user = ""
    # comment attached to the edit
    comment = ""
    # class of article (FA, Good, stub, etc.)
    rating = 0
    # content of the edit page
    content = ""

    def __init__(self, index, title, time, revid, kind, user, comment, rating, content):
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

    # convert change object into json data type
    # input: change object
    def make_json(self):
        body = [
            {
                "index": self.index,
                "metadata": {
                    "revid": self.revid,
                    "time": str(self.time),
                    "kind": str(self.kind),
                    "user": str(self.user),
                    "comment": str(self.comment),
                    "rating": str(self.rating),
                },
                "text": self.content,
            }
        ]
        return body
