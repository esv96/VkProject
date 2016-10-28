from typing import List, Dict
import requests
import asyncio
from aiohttp import ClientSession
import requests.exceptions
import math


class VkApi:
    def __init__(self):
        self.__session = ClientSession()

    def get_members(self, group_id: str) -> List[Dict]:
        try:
            res = requests.get('https://api.vk.com/method/groups.getMembers',
                               params={'group_id': group_id, 'fields': 'photo_100', 'v': '5.57'})
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Cannot connect to vk")
        vk_members = res.json()['response']['items']
        member_list = []
        for user in vk_members:
            if 'deactivated' not in user:
                member_list.append(user)
        return member_list

    async def friends_fetch(self, user_id):
        async with self.__session.get("https://api.vk.com/method/friends.get",
                                      params={'user_id': user_id, 'fields': "photo_100", 'v': '5.57'}) as response:
            res = await response.json()
            items = res['response']['items']
            friend_list = []
            for user in items:
                if 'deactivated' not in user and 'hidden' not in user:
                    friend_list.append(user)
            return friend_list

    async def __posts_fetch(self, user_id, offset):
        async with self.__session.get('https://api.vk.com/method/wall.get',
                                      params={'owner_id': user_id, 'count': 100, 'offset': offset,
                                              'filter': 'owner', 'v': '5.57'}) as response:
            res = await response.json()
            items = res['response']['items']
            # filters
            return items

    async def all_posts_fetch(self, user_id):
        async with self.__session.get('https://api.vk.com/method/wall.get',
                                      params={'owner_id': user_id, 'count': 1, 'v': '5.57'}) as response:
            res = await response.json()
            count = res['response']['count']
            tasks = []

            req_count = math.ceil(count/100)
            for i in range(0, req_count):
                task = asyncio.ensure_future(self.__posts_fetch(user_id, i*100))
                tasks.append(task)

            results = await asyncio.gather(*tasks)
            wall = []
            for result in results:
                wall.extend(result)
            return wall

    def __del__(self):
        self.__session.close()
