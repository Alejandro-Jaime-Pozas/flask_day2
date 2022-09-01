from . import api
from flask import jsonify, request
from app.models import Post, User

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

#api route to get a single post
@api.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())

# api route to create a post
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


# api route to create a new user
# add the user to the api/users url path
@api.route('/users', methods=["POST"])
def create_user():
    # to create user, need to create instance of User class...push the form, convert data to json type format
    # check if request is json type request application/json, throw error if not
    if not request.is_json:
        return jsonify({'error': 'Your request content type must be applicaton/json'}), 400 # throw a 400 type error
    # validate the data for creation
    data = request.json
    for field in ['email', 'username', 'password']:
        if field not in data:
            return jsonify({'error': f'{field} must be in request body'}), 400 # throw a 400 type error
    # get the fields from the json request
    # id = data.get('id') ###remove id since it should be automatically added as Primary key
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    # date_created = data.get('date_created') ###this doesnt work
    # before we add the user to the db, check to see if there is already a user w username or email
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first() # first() means the first instance of that..check this documentation db.Model 
    if existing_user:
        return jsonify({'error': 'User with username/email already exists'}), 400 # returning tuple here (jsonify(), 400)
    # now create a new user with the data
    new_user = User(email=email, username=username, password=password, )
    return jsonify(new_user.to_dict()), 201 # 201 is created successfully


# get existing user from database of users, similar to get post (get method)
@api.route('/users/<user_id>', methods=["GET"])
def get_user(user_id):
    # to get a user, need to reference the existing db, input the user_id to retrieve json type object
    user = User.query.get_or_404(user_id)
    # need to enable jsonify, so create a method in User class to get it as dict type
    return jsonify(user.to_dict())


# add method to get all users api
@api.route('/users', methods=["GET"])
def get_users():
    # to get a user, need to reference the existing db, input the user_id to retrieve json type object
    users = User.query.all()
    # need to enable jsonify, so create a method in User class to get it as dict type
    return jsonify([user.to_dict() for user in users])