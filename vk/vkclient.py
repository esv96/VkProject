from typing import List
import asyncio
from aiohttp.errors import ClientOSError
from vkapi import VkApi
from models import User, Post
from datetime import datetime


class VkClient:
    def __init__(self):
        self.__api = VkApi()

    def get_members(self, group_id: str) -> List[User]:
        vk_members = self.__api.get_members(group_id)
        members = []
        for i in vk_members:
            members.append(User(i['id'], i['first_name'], i['last_name'], i['photo_100']))
        return members

    async def __friends_run(self, ids):
        tasks = []
        for i in ids:
            task = asyncio.ensure_future(self.__api.friends_fetch(i))
            tasks.append(task)
        return await asyncio.gather(*tasks)

    def get_friends_for_many_users(self, ids: List[int]) -> List[User]:
        loop = asyncio.get_event_loop()
        try:
            # friend_groups = loop.run_until_complete(VkWorker.friends_run(ids))
            future = asyncio.ensure_future(self.__friends_run(ids))
            vk_friend_groups = loop.run_until_complete(future)
            friend_groups = []  # parse to vk.User
            for vk_friend_group in vk_friend_groups:
                friend_group = []
                for vk_friend in vk_friend_group:
                    i = vk_friend
                    friend_group.append(User(i['id'], i['first_name'], i['last_name'], i['photo_100']))
                friend_groups.append(friend_group)  ###
            return friend_groups
        except ClientOSError:
            raise ConnectionError("Cannot connect to vk")

    async def __posts_run(self, ids):
        tasks = []
        for i in ids:
            task = asyncio.ensure_future(self.__api.all_posts_fetch(i))
            tasks.append(task)
        return await asyncio.gather(*tasks)

    def get_posts_for_many_users(self, ids: List[int]):
        loop = asyncio.get_event_loop()
        try:
            future = asyncio.ensure_future(self.__posts_run(ids))
            vk_post_groups = loop.run_until_complete(future)
            #vk_post_groups = loop.run_until_complete(self.__posts_run(ids))
            post_groups = []
            for vk_post_group in vk_post_groups:
                post_group = []
                for vk_post in vk_post_group:
                    i = vk_post
                    image = None
                    if ('attachments' in vk_post) and (i['attachments'][0]['type'] == 'photo'):
                        image = i['attachments'][0]['photo']['photo_604']
                    post_group.append(Post(i['id'], i['from_id'], i['owner_id'], datetime.fromtimestamp(i['date']),
                                           i['text'], i['likes']['count'], i['comments']['count'],
                                           i['reposts']['count'], image))
                post_groups.append(post_group)
            return post_groups
        except ClientOSError:
            raise ConnectionError("Cannot connect to vk")
