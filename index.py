from config import db, app, loginManager
from models import User, Post
from flask import render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from modules import *
from sqlalchemy import desc

@loginManager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@loginManager.unauthorized_handler
def unauthorized_callback():
    flash("Log in to access this page")
    return redirect(url_for('login_page'))

@app.route('/')
def index():

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():

    posts = Post.query.order_by(desc(Post.date_posted))

    return render_template('dashboard.html', posts=posts)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile_page.html')

@app.route('/post_page', methods=['POST', 'GET'])
@login_required
def post_page():

    return render_template('post.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/signup_page/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
    
        name = request.form['namee']
        email = request.form['mail']
        contact = request.form['contact']
        school = request.form['school']
        user_name = request.form['user_name']
        user_password = request.form['user_password']
        profile_pict = request.files['pict']
        
        toHash = generate_password_hash(user_password)
        picture_filename = get_file_name(profile_pict)

        upload_file_to_folder(profile_pict, picture_filename)

        users = User(name = name, email =email, contact=contact, username = user_name, user_password=toHash, education = school, profile_pic=picture_filename)

        db.session.add(users)
        db.session.commit()

        return redirect(url_for('login_page'))

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login_page/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':

        username = request.form['userName']
        password = request.form['pas']

        user = User.query.filter(User.username == username).first()
        
        if user: 
            checkPassword = check_password_hash(user.user_password, password)

            login_user(user)

            if checkPassword == True:
                login_user(user)
                return redirect(url_for('profile'))

            else:
                flash("Wrong password or username")
                return redirect(url_for('login_page'))
            
        else:
            flash("Wrong password or username")
            return redirect(url_for('login_page'))
        
@app.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('login_page'))

@app.route('/profile/update', methods=['POST', 'GET'])
def update():

    if request.method == 'POST':
        
        name = request.form['namee']
        email = request.form['mail']
        contact = request.form['contact']
        school = request.form['school']
        username = request.form['user_name']
        profile_pict = request.files['pict']

        if request.files['pict']:

            uniquename = get_file_name(profile_pict)

            upload_file_to_folder(profile_pict, uniquename)

            current_user.name = name
            current_user.email = email
            current_user.contact = contact
            current_user.education = school
            current_user.username = username
            current_user.profile_pic = uniquename

            db.session.commit()

            flash('Updated successfully')

            return redirect(url_for('profile'))
        else:
            current_user.name = name
            current_user.email = email
            current_user.contact = contact
            current_user.education = school
            current_user.username = username

            db.session.commit()

            flash('Updated successfully')   
            return redirect(url_for('profile')) 

@app.route('/profile/delete', methods=['POST', 'GET'])
def delete():

    db.session.delete(current_user)
    db.session.commit()

    return redirect(url_for('login_page'))

@app.route('/post_page/post', methods=['POST', 'GET'])
def post():

    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        user = current_user

        post = Post(title = title, body = body, user=user)

        db.session.add(post)
        db.session.commit()

        flash("Posted Successfully")

        return redirect(url_for('post_page'))
    
@app.route('/view_post')
def view_post():

    posts = current_user.posts

    return render_template('view_post.html', posts = posts)

@app.route('/delete_post/<post_id>', methods=['GET', 'POST'])
def delete_post(post_id):

    post = Post.query.filter(Post.id==post_id).first()

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully')

    return redirect(url_for('dashboard'))

@app.route('/update_post_page/<int:post_id>')
def update_post_page(post_id):

    post = Post.query.filter(Post.id == post_id).first()

    title = post.title
    body = post.body
    
    return render_template('update_post.html', title = title, body = body, post_id = post_id)

@app.route('/update_post_page/update_post', methods=['POST', 'GET'])
def update_post():

    if request.method == 'POST':
        title = request.form['title1']
        body = request.form['body1']
        ids = request.form['postId']

        post = Post.query.filter(Post.id == ids).first()

        post.title = title
        post.body = body

        db.session.commit()

        flash("Post Updated")

        return redirect(url_for('dashboard'))


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=False)



