import json
from vk.vkapi import VkApi

api = VkApi()


def load_members():
    members = api.get_members('30390813')
    with open('members.json', 'w', encoding='utf-8') as f:
        json.dump(members, f, ensure_ascii=False, indent=4)


def load_friends():
    friends = api.get_friends(528243)
    with open('friends.json', 'w', encoding='utf-8') as f:
        json.dump(friends, f, ensure_ascii=False, indent=4)


def load_posts():
    posts = api.get_posts(528243)
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)


load_members()
load_friends()
load_posts()