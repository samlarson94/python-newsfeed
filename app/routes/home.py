from flask import Blueprint, render_template
from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

# @bp decorator before the function turns it into a route
@bp.route('/')
def index():
   # Adding get all posts
    # get_db() - returns a session connection that's attached to this route's context
    # db.query - Used on the connection object to query the Post model for all posts in descending order
  db = get_db() 
  posts = db.query(Post).order_by(Post.created_at.desc()).all()
  # Update return statement to render the template with posts data
  return render_template(
  'homepage.html',
  posts=posts
)

@bp.route('/login')
def login():
  return render_template('login.html')

# Id represents the parameter in the URL. We capture it in single(id)
@bp.route('/post/<id>')
def single(id):
  return render_template('single-post.html')