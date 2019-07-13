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
    post = db.Column(db.String(120))

    def __init__(self, title, post):
        self.title = title
        self.post = post




@app.route('/', methods=['POST', 'GET'])
def index():
    



@app.route('/' methods=['POST'])
def 


if __name__ == '__main__':
    app.run()