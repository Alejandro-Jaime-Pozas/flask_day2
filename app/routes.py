from app import app # this refers to app folder, then imports directly from __init__.py file the app module
from flask import render_template, redirect, url_for, flash # url_for looks for the FUNCTION name, no the route name
from flask_login import login_user, logout_user, login_required, current_user # current_user sets user_id to current_user, login_required adds an addtl security measure to ensure user is logged in to create a post
from app.forms import LoginForm, SignUpForm, PostForm
from app.models import User, Post


@app.route('/') # this creates a route to the page
@app.route('/index')
def index():
    posts = Post.query.all()
    print(posts)
    return render_template('index.html', posts=posts) # for render_template, first param is the html template, the first posts refers to a variable inside the html template, and indicates it is equal to whatever is in the fn defined here above

@app.route('/signup', methods=["GET", "POST"]) # this creates a different page; METHODS allows to get and post from/to server
def signup():
    form = SignUpForm() # form is an instance of class of SignUpForm from app.forms
    # if the form is submitted and all the data is valid
    if form.validate_on_submit():
        print('Form has been validated!!!')
        print(form.email.data, form.username.data, form.password.data) # this allows you to print the data received from user; form instance > instance variable > data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # before we add the user to the db, check to see if there is already a user w username or email
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first() # first() means the first instance of that..check this documentation db.Model 
        if existing_user:
            flash('A user with that username or email already exists.', 'danger') # flash stores message and shows it until the NEXT request; for signup page, will show message as red
            return redirect(url_for('signup'))
        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created.", "success") # for whatever page comes after, will show message as green
        return redirect(url_for('index'))
    return render_template('signup.html', form=form) # form = form to be able to use in frontend html


@app.route('/create', methods=["GET", "POST"]) # MAKE SURE YOU ALLOW BOTH GET AND POST METHODS...
@login_required # use this to require the user to be logged in
def create():
    form = PostForm()
    if form.validate_on_submit(): ################# MISSING SOMETHING HERE
        # get the data from the form
        title = form.title.data
        body = form.body.data
        # create a new instance of Post w the form data
        new_post = Post(title=title, body=body, user_id=current_user.id) # sets the Post instance's user_id to the current user...
        # flash a msg saying the post has been created
        flash(f'{new_post.title} has been created.', 'secondary')
        # return back to homepage
        return redirect(url_for('index'))

    return render_template('createpost.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # get username and password from form
        username = form.username.data
        password = form.password.data
        # query the user table for a user w the same username as the form
        user = User.query.filter_by(username=username).first()
        # if the user exists and the password is correct for that user
        if user is not None and user.check_password(password):
            # log the user in w the login_user fn from flask_login
            login_user(user)
            # flash a success message upon login success
            flash(f"Welcome back {user.username}!", "success")
            # redirect bacl to the homepage
            return redirect(url_for('index'))
        # if no user w username or password incorrect
        else:
            flash('Incorrect username or password. Please try again.', 'danger')
            # redirect back to login page
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user() # this fn call literally logs the user out, import it from flask_login
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('index'))


@app.route('/posts/<post_id>') # need <> angled brackets to make value within it a dynamic variable; <post_id> is the variable part (you can choose multiple posts)
@login_required # use this to require the user to be logged in
def view_post(post_id): # here the fn takes in a post_id NEEDS SAME NAME AS ABOVE IN APP.ROUTE()...
    post = Post.query.get_or_404(post_id) # this encounters error if you just put in the get()
    return render_template('post.html', post=post)


# ESTO DE ABAJO LO VOY A HACER/DEJAR HASTA EL FINAL





@app.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post_to_edit = Post.query.get_or_404(post_id)
    # make sure the post to edit is owned by the current user/author
    if post_to_edit.author != current_user:
        flash("You don't have permission to edit this post", "danger")
        return redirect(url_for('view_post', post_id=post_id)) # redirects to view_post fn w post_id
    form = PostForm()
    if form.validate_on_submit():
        # get the form data
        title = form.title.data
        body = form.body.data
        # update the post w data from the form
        post_to_edit.update(title=title, body=body)
        flash(f"{post_to_edit.title} has been updated", 'success')
        return redirect(url_for('view_post', post_id=post_id))

    return render_template('edit_post.html', post=post_to_edit, form=form)


@app.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    if post_to_delete.author != current_user:
        flash("You don't have permission to delete this post", 'danger')
        return redirect(url_for('index'))
    # delete post
    post_to_delete.delete()
    flash(f"{post_to_delete.title} has been deleted", 'info')
    return redirect(url_for('index'))