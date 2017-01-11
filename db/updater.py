from concurrent.futures import ThreadPoolExecutor
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
        self.vk_client.set_share_func(FBApi.get_share_count)

    @db_session
    def update_users(self):
        user_ids = set()
        member_set = set((i.id_ for i in select(p for p in User if p.is_member)))
        vk_members = self.vk_client.get_members(self.__group_id)
        members = []
        for member in vk_members:
            user_ids.add(member.uid)
            try:
                usr = User[member.uid]
                usr.first_name = member.first_name
                usr.last_name = member.last_name
                usr.photo_url = member.photo_url
                usr.is_member = True
            except pony.orm.core.ObjectNotFound:
                usr = User(id_=member.uid, first_name=member.first_name,
                           last_name=member.last_name, photo_url=member.photo_url, is_member=True)
            if usr.id_ in member_set:
                member_set.remove(usr.id_)
            members.append(usr)
        for i in member_set:
            User[i].is_member = False
        print("members ok")

        with ThreadPoolExecutor(max_workers=30) as executor:
            friend_groups = list(executor.map(self.vk_client.get_friends, [member.id_ for member in members]))
        print("friends ok")
        for idx, member in enumerate(members):
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
        users = select(p for p in User)
        with ThreadPoolExecutor(max_workers=30) as executor:
            for user in users:
                executor.submit(self.update_user_post, user.id_)

    @db_session
    def update_user_post(self, user_id):
        user = User[user_id]
        post_set = set((i.id_ for i in user.posts))
        vk_posts = self.vk_client.get_posts(user.id_, interval=timedelta(days=1))
        for vk_post in vk_posts:
            try:
                post = Post[vk_post.owner_id, vk_post.pid]
                post.comments = vk_post.comments
                post.likes = vk_post.likes
                post.reposts = vk_post.reposts
                post.share_count = vk_post.share_count
            except pony.orm.core.ObjectNotFound:
                post = Post(owner=user, id_=vk_post.pid, date=vk_post.date, text=vk_post.text,
                            comments=vk_post.comments, likes=vk_post.likes, reposts=vk_post.reposts,
                            attachments=vk_post.attachments, original_post_id=vk_post.original_post_id,
                            share_count=vk_post.share_count)
            if post.id_ in post_set:
                post_set.remove(post.id_)
        for i in post_set:
            Post[user_id, i].delete()


if __name__ == '__main__':
    updater = DbUpdater("30390813")
    updater.update_users()
    updater.update_posts()
