from bottle import Bottle, view, static_file
from db.service import DbService, Sorting
from pony.orm.integration.bottle_plugin import PonyPlugin

from db.models import *

app = Bottle()
app.install(PonyPlugin())


@app.route('/static/<filename>')
def static(filename):
    return static_file(filename, root="./static")


@app.route('/')
@view('index')
def index():
    members = select(p for p in User if p.is_member).order_by(User.id_)
    return dict(members=members)


@app.route('/id<user_id:int>')
@view('user')
def user(user_id=0):
    try:
        member = User[user_id]
        posts = DbService.get_news_feed(member.id_, Sorting.likes)
        return dict(user=member, posts=posts)
    except pony.orm.core.ObjectNotFound:
        return "not found"


#run(app, server='paste', host='localhost', port=8080)
app.run(host='localhost', port=8080)

