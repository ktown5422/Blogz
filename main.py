from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 
app.secret_key = 'asdfjkl;!@#'
 
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner = owner
        

    def validation(self, title, post):
        
        if self.title and self.post:
            return True
        else:
            return False
            
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    
    route_list = ['login', 'blog', 'add_user', 'index', 'styles']
    if request.endpoint not in route_list and 'username' not in session:
        return redirect('/login')       


@app.route('/')
def index():
    every_user = User.query.distinct()
    return render_template('index.html', all_users=every_user)

@app.route('/blog')
def blog():
    
    post_id = request.args.get('id')
    singleUser_id = request.args.get('owner_id')
    if (post_id):
        new_post = Blog.query.get(post_id)
        return render_template('single_post.html', new_post=new_post)
    else:
        if (singleUser_id):
            singleUser_blog_posts = Blog.query.filter_by(owner_id=singleUser_id)
            return render_template('singleUser.html', posts=singleUser_blog_posts)
        else:
            every_blog_posts = Blog.query.all()
        
            return render_template('blog.html', posts=every_blog_posts)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_post = request.form['blog_post']
        owner = User.query.filter_by(username=session['username']).first()
        title_error=''
        new_post_error=''
        new_blog = Blog(blog_title, blog_post, owner)

        if new_blog.validation(blog_title, blog_post):
            db.session.add(new_blog)
            db.session.commit()
            new_blog_url = "/blog?id=" + str(new_blog.id)
            return redirect(new_blog_url)
        else:
            if not blog_title.strip():
                title_error = 'Please insert title'
            if not blog_post.strip():
                new_post_error = 'Pleases insert a blog post'
            if title_error or new_post_error:
                return render_template('newpost.html', title_error=title_error, new_post_error=new_post_error)
        
    return render_template('newpost.html')

@app.route('/signup', methods=['GET', 'POST'])
def add_user():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        


        username_error = ''
        password_error = ''
        verify_error = ''
        

        if len(username) < 3 or len(username) > 20 or " " in username:
            username_error='check the length of your username'

        if len(password) < 3 or len(password) > 20 or " " in password:
            password_error ='check the length of your password'

        if password != verify_password:
            verify_error='The users password and password-confirmation do not match.'

        if username_error or password_error or verify_error:
            return render_template('signup.html', username_error=username_error, password_error=password_error, verify_error=verify_error, username=username)
        # else:
        #     return render_template('signup.html', username=username)


        user_exist = User.query.filter_by(username=username).first()
        if not user_exist: 
        
            new_user = User(username, password) 
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash('New user created', 'success')
            return redirect('/newpost')

    else:
        return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        if not username and not password:
            flash('Username and password cannot be blank', 'error')
            return render_template('login.html')
        if not username:
            flash('Username cannot be blank', 'error')
            return render_template('login.html')
        if not password:
            flash('Password cannot be blank', 'error')
            return render_template('login.html')
        
    
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('Username does not exist', 'error')
            return render_template('login.html')
        if user.password != password:
            flash('Password is incorrect', 'error')
            return render_template('login.html')

    
        if user and user.password == password:
            session['username'] = username
            return redirect('newpost')

    return render_template('login.html')



@app.route('/logout')
def logout():
    del session['username']
    flash('logged Out', 'success')
    return redirect('/blog')

# @app.route('/delete-post', methods=['POST'])
# def delete_post():

#     blog_id = int(request.form['post-id'])
#     blog = Blog.query.get(blog_id)
#     blog.completed = True
#     db.session.add(blog_id)
#     db.session.commit()

#     return redirect('/login')



if __name__ == '__main__':
    app.run()