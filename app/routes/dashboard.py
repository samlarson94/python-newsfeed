from flask import Blueprint, render_template, session
from app.models import Post
from app.db import get_db

# url_prefix argument will prefix every route in the blueprint witn /dashboard
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
def dash():
  # Add connection and query of the database
  db = get_db()
  posts = (
    db.query(Post)
    .filter(Post.user_id == session.get('user_id'))
    .order_by(Post.created_at.desc())
    .all()
  )
  # Revise return statement to pass posts and session data
  return render_template(
    'dashboard.html',
    posts=posts,
    loggedIn=session.get('loggedIn')
  )

@bp.route('/edit/<id>')
def edit(id):
  # Add connection to and query the database
  db = get_db()
  post = db.query(Post).filter(Post.id == id).one()

  # Update return statement to pass new post and session information
  return render_template(
    'edit-post.html',
    post=post,
    loggedIn=session.get('loggedIn')
  )