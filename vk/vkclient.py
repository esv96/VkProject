from typing import List
from vk.vkapi import SyncVkApi
from vk.models import User, Post
from datetime import datetime, timedelta


class VkClient:
    def __init__(self):
        self.__api = SyncVkApi()
        self.__share_func = None

    def set_share_func(self, share_func):
        self.__share_func = share_func if callable(share_func) else None

    def get_members(self, group_id: str) -> List[User]:
        vk_members = self.__api.get_members(group_id)
        members = []
        for i in vk_members:
            members.append(User(i['id'], i['first_name'], i['last_name'], i['photo_100']))
        return members

    def get_friends(self, user_id: int) -> List[User]:
        vk_friends = self.__api.get_friends(user_id)
        friends = []
        for i in vk_friends:
            friends.append(User(i['id'], i['first_name'], i['last_name'], i['photo_100']))
        return friends

    def get_posts(self, user_id: int, interval: timedelta = None) -> List[Post]:  # посты за интервал но не менее 100
        posts = []
        offset = 0
        now = datetime.now()
        while True:
            vk_posts = self.__api.get_posts(user_id, offset)
            for i in vk_posts:
                attachments, share_count = None, None
                if 'attachments' in i:
                    attachments, share_count = self.__parse_attachments(i['attachments'])
                copy_history = None
                if ('copy_history' in i) and (len(i['copy_history']) == 1):
                    copy_history = i['copy_history'][0]
                orig_post_id = '{}_{}'.format(copy_history['owner_id'], copy_history['id']) if copy_history else None
                post = Post(i['id'], i['owner_id'], datetime.fromtimestamp(i['date']),
                            i['text'], i['comments']['count'], i['likes']['count'],
                            i['reposts']['count'], attachments, orig_post_id, share_count)
                if (interval is None) or (now - post.date) <= interval:
                    posts.append(post)
                else:
                    vk_posts = []
                    break
            if len(vk_posts) == 0 or len(vk_posts) < 100:
                break
            offset += 100
        return posts

    def __parse_attachments(self, vk_attachments: List[dict]):
        attachments = []
        share_count = None
        for vk_att in vk_attachments:
            if vk_att['type'] == 'photo':
                attachments.append(dict(type='photo', url=vk_att['photo']['photo_604']))
            elif vk_att['type'] == 'audio':
                attachments.append(dict(type='audio', url=vk_att['audio']['url'],
                                        artist=vk_att['audio']['artist'],
                                        title=vk_att['audio']['title']))
            elif vk_att['type'] == 'link':
                url = vk_att['link']['url']
                attachments.append(dict(type='link', url=url,
                                        title=vk_att['link']['title'],
                                        image=vk_att['link']['photo']['photo_130'] if 'photo' in vk_att['link'] else None))
                if self.__share_func:
                    share_count = self.__share_func(url)
        return attachments, share_count
