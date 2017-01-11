import math
from bottle import Bottle, view, static_file, request
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
    page_size = 20
    order = request.GET.get('order_by', 'date')
    if order == 'likes':
        ord_by = lambda p: desc(p.likes / (avg(c.likes for c in p.owner.posts if c.share_count) + 1))
    elif order == 'reposts':
        ord_by = lambda p: desc(p.reposts / (avg(c.reposts for c in p.owner.posts) + 1))
    elif order == 'comments':
        ord_by = lambda p: desc(p.comments / (avg(c.comments for c in p.owner.posts) + 1))
    elif order == 'share':
        ord_by = lambda p: desc(p.share_count / (avg(c.share_count for c in p.owner.posts if c.share_count) + 1))
    else:
        ord_by = lambda p: desc(p.date)
    page = request.GET.get('page', '1')
    page = int(page) if page.isdigit() else 1
    try:
        member = User[user_id]
        if order != 'share':
            page_count = math.ceil(count(p for p in Post if p.owner in member.friends)/page_size)
            posts = select(p for p in Post if p.owner in member.friends).order_by(ord_by).page(page, pagesize=page_size)
        else:
            page_count = math.ceil(count(p for p in Post if p.owner in member.friends if p.share_count)/page_size)
            posts = select(p for p in Post if p.owner in member.friends if p.share_count).order_by(ord_by)\
                .page(page, pagesize=page_size)
        return dict(user=member, posts=posts, page=page, page_count=page_count, order_by=order)
    except pony.orm.core.ObjectNotFound:
        return "not found"


#run(app, server='paste', host='localhost', port=8080)
app.run(host='localhost', port=8080)

