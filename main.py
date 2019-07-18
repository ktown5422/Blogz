from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:ktizzle314@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 
 
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(db.text))

    def __init__(self, title, post):
        self.title = title
        self.post = post



@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST'])
def blog():

    return render_template('blog.html')

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_post = request.form['blog_post']
        title_error=''
        new_post_error=''
        if not blog_title.strip():
            title_error = 'Please insert title'
        if not blog_post.strip():
            new_post_error = 'Pleases insert a blog post'
        if title_error or new_post_error:
            return render_template('newpost.html', title_error=title_error, new_post_error=new_post_error)
        else:
            new_blog = Blog(blog_title, blog_post)
            db.session.add(new_blog)
            db.session.commit()


           

    return render_template('newpost.html', blog_title=blog_title, blog_post=blog_post)    

if __name__ == '__main__':
    app.run()