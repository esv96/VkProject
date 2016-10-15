import time
from bottle import Bottle, run, view, static_file
from vk import VkClient
app = Bottle()

group_id = "30390813"

t1 = time.clock()
vk_client = VkClient()
members = vk_client.get_members(group_id)
friend_groups = vk_client.get_friends_for_many_users([member['id'] for member in members])
print(time.clock()-t1)
print("graph is loaded")


@app.route('/static/<filename>')
def static(filename):
    return static_file(filename, root="./static")


@app.route('/')
@view('index')
def index():
    return dict(members=members)


@app.route('/id<user_id:int>')
@view('user')
def user(user_id=0):
    print("news_feed ", user_id)
    t1 = time.clock()
    member = members[user_id]
    friends = friend_groups[user_id]
    post_groups = vk_client.get_posts_for_many_users(friend['id'] for friend in friends)
    news_feed = []
    for post_group in post_groups:
        news_feed.extend(post_group)
    news_feed.sort(key=lambda post: post['likes']['count'], reverse=True)
    print(time.clock()-t1)
    return dict(user=member, posts=news_feed[:100])

run(app, host='localhost', port=8080, debug=True)

