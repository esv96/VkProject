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
    def __init__(self, pid: int, from_id: int, owner_id: int, date: datetime, text: str, likes: int,
                 comments: int, reposts: int, image: str = None):
        self.pid = pid
        self.from_id = from_id
        self.owner_id = owner_id
        self.date = date
        self.text = text
        self.likes = likes
        self.comments = comments
        self.reposts = reposts
        self.image = image

    def __repr__(self):
        return "VkPost {}_{}".format(self.owner_id, self.pid)

