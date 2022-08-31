from . import api
from flask import jsonify, request
from app.models import Post

# here we are linking the __init__.py to this file, returning a json api object
@api.route('/')
def index():
    names = ['Al', 'By', 'Tay']
    return jsonify(names)

# this /api/posts route/fn takes all the posts existingin db, and returns a json type object with each of the posts as a dict...this is done by a method within the Post class 
@api.route('/posts', methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

@api.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@api.route('/posts', methods=["POST"])
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content type must be application/json'}), 400
    # get the data from the request body
    data = request.json
    print(data)
    # validate the data
    for field in ['title', 'body', 'user_id']:
        if field not in data:
            # if field not in request body, respond w a 400 error
            return jsonify({'error': f"{field} must be in request body"}), 400 # returning a tuple w jsonfy stmt and 400, which throws an error to indicate request not found

    # get fields from data dict
    title = data.get('title')
    body = data.get('body')
    user_id = data.get('user_id')
    # create a new instance of post w data
    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict()), 201 # 201 status returns 'created'