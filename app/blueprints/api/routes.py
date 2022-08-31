from . import api
from flask import jsonify
from app.models import Post

# here we are linking the __init__.py to this file, returning a json api object
@api.route('/')
def index():
    names = ['Al', 'By', 'Tay']
    return jsonify(names)

# this /api/posts route/fn takes all the posts existingin db, and returns a json type object with each of the posts as a dict...this is done by a method within the Post class 
@api.route('/posts')
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

@api.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())