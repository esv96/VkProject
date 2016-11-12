from db.models import *
from typing import List
from enum import Enum


class Sorting(Enum):
    likes = 1
    reposts = 2
    comments = 3
    shares = 4


class DbService:
    @staticmethod
    def get_news_feed(user_id: int, order_by: Sorting = None) -> List[Post]:
        if order_by is Sorting.likes:
            news_feed = DbService.__posts_by_likes(user_id)
        elif order_by is Sorting.comments:
            news_feed = DbService.__posts_by_comments(user_id)
        elif order_by is Sorting.reposts:
            news_feed = DbService.__posts_by_reposts(user_id)
        elif order_by is Sorting.shares:
            news_feed = select(p for p in Post if p.owner in User[user_id].friends)\
                .order_by(desc(Post.share_count)).limit(100)
        else:
            news_feed = select(p for p in Post if p.owner in User[user_id].friends).\
                order_by(desc(Post.date)).limit(100)
            print("kek")
        return news_feed

    @staticmethod
    def __posts_by_likes(user_id):
        posts = Post.select_by_sql("select p.* "
                                   "from post p, "
                                   "(select p.owner as own, avg(p.likes) as avglikes "
                                   "from post p, user_friends f "
                                   "where p.owner = f.user_2 and f.user = $user_id "
                                   "group by p.owner) t "
                                   "where p.owner = t.own "
                                   "order by (p.likes+1)*2/(t.avglikes+1) desc, p.likes desc limit 100")
        return posts

    @staticmethod
    def __posts_by_comments(user_id):
        posts = Post.select_by_sql("select p.* "
                                   "from post p, "
                                   "(select p.owner as own, avg(p.comments) as avgcomments "
                                   "from post p, user_friends f "
                                   "where p.owner = f.user_2 and f.user = $user_id "
                                   "group by p.owner) t "
                                   "where p.owner = t.own "
                                   "order by (p.comments+1)*2/(t.avgcomments+1) desc, p.comments desc limit 100")
        return posts

    @staticmethod
    def __posts_by_reposts(user_id):
        posts = Post.select_by_sql("select p.* "
                                   "from post p, "
                                   "(select p.owner as own, avg(p.reposts) as avgreposts "
                                   "from post p, user_friends f "
                                   "where p.owner = f.user_2 and f.user = $user_id "
                                   "group by p.owner) t "
                                   "where p.owner = t.own "
                                   "order by (p.reposts+1)*2/(t.avgreposts+1) desc, p.reposts desc limit 100")
        return posts
