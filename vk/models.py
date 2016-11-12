from datetime import datetime


class User:
    def __init__(self, uid: int, first_name: str, last_name: str, photo_url: str):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.photo_url = photo_url

    def __repr__(self):
        return "<VkUser {}> {} {}".format(self.uid, self.first_name, self.last_name)


class Post:
    def __init__(self, pid: int, owner_id: int, date: datetime, text: str, comments: int,
                 likes: int, reposts: int, attachments: dict = None, original_post_id: str = None,
                 share_count: int = None):
        self.pid = pid
        self.owner_id = owner_id
        self.date = date
        self.text = text
        self.comments = comments
        self.likes = likes
        self.reposts = reposts
        self.attachments = attachments
        self.original_post_id = original_post_id
        self.share_count = share_count

    def __repr__(self):
        return "<VkPost {}_{}>".format(self.owner_id, self.pid)

