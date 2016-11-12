from pony.orm import *
from datetime import datetime


db = Database()


class User(db.Entity):
    id_ = PrimaryKey(int)
    first_name = Required(str)
    last_name = Required(str)
    photo_url = Optional(str)
    is_member = Required(bool)
    friends = Set('User', reverse='friends')
    posts = Set('Post')


class Post(db.Entity):
    owner = Required(User)
    id_ = Required(int)
    date = Required(datetime)
    text = Optional(LongStr)
    comments = Required(int)
    likes = Required(int)
    reposts = Required(int)
    attachments = Optional(Json)
    original_post_id = Optional(str, nullable=True)
    share_count = Optional(int)
    PrimaryKey(owner, id_)


db.bind("postgres", host="localhost", user="postgres", password="root", database="test")
db.generate_mapping(create_tables=True)
