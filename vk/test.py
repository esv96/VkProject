import unittest
from vkclient import VkClient, VkApi
from models import User, Post
from unittest.mock import Mock, patch

get_members_json = [{"id": 1, "first_name": "Павел", "last_name": "Дуров",
                     "photo_100": "https://pp.vk.me/c629231/v629231001/c542/fcMCbfjDsv0.jpg"},
                    {"id": 5, "first_name": "Илья", "last_name": "Перекопский",
                     "photo_100": "https://pp.vk.me/c636524/v636524005/2f794/DLdW2jwjWg0.jpg"}]

async def fake_friends_fetch(user_id):
    return get_members_json


class TestVkWorker(unittest.TestCase):
    @patch.object(VkApi, 'get_members', return_value=get_members_json)
    def test_getmembers(self, mock_method):
        vk_client = VkClient()
        members = vk_client.get_members('1')
        self.assertIsInstance(members, list)
        self.assertEqual(len(members), len(get_members_json))
        self.assertIsInstance(members[0], User)
        user = members[0]
        self.assertEqual(user.first_name, get_members_json[0]['first_name'])
        self.assertEqual(user.last_name, get_members_json[0]['last_name'])

    @patch.object(VkApi, 'friends_fetch', side_effect=fake_friends_fetch)
    def test_get_friends_for_many_users(self, mock_method):
        vk_client = VkClient()
        members = [User(112, "Kek", "Sesov", "url"), (113, "Ses", "Kekov", "url")]
        friends_group = vk_client.get_friends_for_many_users([i['id'] for i in get_members_json])

if __name__ == '__main__':
    unittest.main()
