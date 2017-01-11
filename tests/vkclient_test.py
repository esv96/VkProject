import unittest
from datetime import datetime
from unittest.mock import patch, Mock
from vk.vkclient import VkClient
from vk.models import User, Post
from vk.vkapi import VkApi
import json
patch.object = patch.object


class TestVkClient(unittest.TestCase):
    def setUp(self):
        self.group_id='30390813'
        self.user_id = 528243
        with open('members.json', encoding='utf-8') as f:
            self.members_data = json.load(f)
        with open('friends.json', encoding='utf-8') as f:
            self.friends_data = json.load(f)
        with open('posts.json', encoding='utf-8') as f:
            self.posts_data = json.load(f)

    def test_get_members(self):
        with patch.object(VkApi, 'get_members', return_value=self.members_data) as mock_method:
            vkclient = VkClient()
            members = vkclient.get_members(self.group_id)
            self.assertIsInstance(members, list)
            self.assertGreater(len(members), 0)
            self.assertIsInstance(members[0], User)
            member = members[0]
            orig_member = self.members_data[0]
            self.assertEqual(member.first_name, orig_member['first_name'])
            self.assertEqual(member.last_name, orig_member['last_name'])
            self.assertEqual(member.uid, orig_member['id'])
            self.assertEqual(member.photo_url, orig_member['photo_100'])

    def test_get_friends(self):
        with patch.object(VkApi, 'get_friends', return_value=self.friends_data) as mock_method:
            vkclient = VkClient()
            friends = vkclient.get_friends(self.user_id)
            self.assertIsInstance(friends, list)
            self.assertGreater(len(friends), 0)
            self.assertIsInstance(friends[0], User)
            friend = friends[0]
            orig_friend = self.friends_data[0]
            self.assertEqual(friend.first_name, orig_friend['first_name'])
            self.assertEqual(friend.last_name, orig_friend['last_name'])
            self.assertEqual(friend.uid, orig_friend['id'])
            self.assertEqual(friend.photo_url, orig_friend['photo_100'])

    def test_get_posts(self):
        with patch.object(VkApi, 'get_posts', return_value=self.posts_data) as mock_method:
            vkclient = VkClient()
            posts = vkclient.get_posts(self.user_id)
            self.assertIsInstance(posts, list)
            self.assertGreater(len(posts), 0)
            self.assertIsInstance(posts[0], Post)
            post = posts[0]
            orig_post = self.posts_data[0]
            self.assertEqual(post.pid, orig_post['id'])
            self.assertEqual(post.owner_id, orig_post['owner_id'])
            self.assertEqual(post.date, datetime.fromtimestamp(orig_post['date']))
            self.assertEqual(post.text, orig_post['text'])
            self.assertEqual(post.likes, orig_post['likes']['count'])
