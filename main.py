from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 
 
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(db.text))

    def __init__(self, title, post):
        self.title = title
        self.post = post
        

    def validation(self, title, post):
        
        if self.title and self.post:
            return True
        else:
            return False



@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():
    
    post_id = request.args.get('id')
    if (post_id):
        new_post = Blog.query.get(post_id)
        return render_template('single_post.html', new_post=new_post)
    else:
        
        every_blog_posts = Blog.query.all()
        
        return render_template('blog.html', posts=every_blog_posts)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_post = request.form['blog_post']
        title_error=''
        new_post_error=''
        new_blog = Blog(blog_title, blog_post)

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

if __name__ == '__main__':
    app.run()