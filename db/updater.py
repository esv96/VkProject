from datetime import timedelta
from multiprocessing.dummy import Pool as ThreadPool

import pony.orm
from pony.orm import *

from db.models import User, Post
from fbapi import FBApi
from vk.vkclient import VkClient


class DbUpdater:
    def __init__(self, group_id):
        self.__group_id = group_id
        self.fbapi = FBApi()
        self.vk_client = VkClient()
        self.vk_client.set_share_func(FBApi)

    @db_session
    def update_users(self):
        user_ids = set()
        members = self.vk_client.get_members(self.__group_id)
        pony_members = []
        for member in members:
            user_ids.add(member.uid)
            usr = None
            try:
                usr = User[member.uid]
                usr.first_name = member.first_name
                usr.last_name = member.last_name
                usr.photo_url = member.photo_url
                usr.is_member = True
            except pony.orm.core.ObjectNotFound:
                usr = User(id_=member.uid, first_name=member.first_name,
                           last_name=member.last_name, photo_url=member.photo_url, is_member=True)
            pony_members.append(usr)
        print("members ok")

        with ThreadPool(30) as pool:
            friend_groups = pool.map(self.vk_client.get_friends, [member.id_ for member in pony_members])
        print("friends ok")
        for idx, member in enumerate(pony_members):
            friends_set = set((i.id_ for i in member.friends))
            for friend in friend_groups[idx]:
                usr = None
                user_ids.add(friend.uid)
                try:
                    usr = User[friend.uid]
                    usr.first_name = friend.first_name
                    usr.last_name = friend.last_name
                    usr.photo_url = friend.photo_url
                except pony.orm.core.ObjectNotFound:
                    usr = User(id_=friend.uid, first_name=friend.first_name,
                               last_name=friend.last_name, photo_url=friend.photo_url, is_member=False)

                member.friends.add(usr)
                if usr.id_ in friends_set:
                    friends_set.remove(usr.id_)
            for i in friends_set:
                member.friends.remove(User[i])

        delete(p for p in User if p.id_ not in user_ids)
        print("ok")

    @db_session
    def update_posts(self):
        users = select(p for p in User if not p.is_member)
        pool = ThreadPool(30)
        pool.map(self.update_user_post, [user.id_ for user in users])
        pool.close()
        pool.join()

    @db_session
    def update_user_post(self, user_id):
        vk_posts = self.vk_client.get_posts(user_id, interval=timedelta(days=30))
        for vk_post in vk_posts:
            try:
                post = Post[vk_post.owner_id, vk_post.pid]
                post.comments = vk_post.comments
                post.likes = vk_post.likes
                post.reposts = vk_post.reposts
                post.share_count = vk_post.share_count
            except pony.orm.core.ObjectNotFound:
                Post(owner=User[user_id], id_=vk_post.pid, date=vk_post.date, text=vk_post.text,
                     comments=vk_post.comments, likes=vk_post.likes, reposts=vk_post.reposts,
                     attachments=vk_post.attachments, original_post_id=vk_post.original_post_id,
                     share_count=vk_post.share_count)


if __name__ == '__main__':
    updater = DbUpdater("30390813")
    updater.update_users()
    updater.update_posts()
