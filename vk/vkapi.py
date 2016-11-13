import requests
import requests.exceptions
from typing import List, Dict
from vk.vktoken import token #token str


class SyncVkApi:
    def __init__(self):
        self.__session = requests.Session()

    def get_members(self, group_id: str) -> List[Dict]:
        try:
            res = self.__session.get('https://api.vk.com/method/groups.getMembers',
                                     params={'group_id': group_id, 'fields': 'photo_100',
                                             'access_token': token, 'v': '5.57'})
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Cannot connect to vk")
        vk_members = res.json()['response']['items']
        member_list = []
        for user in vk_members:
            if 'deactivated' not in user:
                member_list.append(user)
        return member_list

    def get_friends(self, user_id):
        try:
            res = self.__session.get("https://api.vk.com/method/friends.get",
                                     params={'user_id': user_id, 'fields': "photo_100", 'v': '5.57'})
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Cannot connect to vk")
        items = res.json()['response']['items']
        friend_list = []
        for user in items:
            if 'deactivated' not in user and 'hidden' not in user:
                friend_list.append(user)
        return friend_list

    def get_posts(self, user_id: int, offset: int=0) -> List[Dict]:
        try:
            res = self.__session.get('https://api.vk.com/method/wall.get',
                                     params={'owner_id': user_id, 'count': 100, 'offset': offset,
                                             'filter': 'owner', 'v': '5.57'})
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Cannot connect to vk")
        try:
            posts = res.json()['response']['items']
        except KeyError:
            print(res.text)
            posts = []
        return posts
