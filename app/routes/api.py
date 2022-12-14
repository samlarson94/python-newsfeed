# Add import statements
import sys
from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
from app.utils.auth import login_required

bp = Blueprint('api', __name__, url_prefix='/api')

# ADD SIGN UP ROUTE
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

# Create New User - use Python dictionary notation
  try:
    # Attempt to create a new user
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
  )

# Save to Database - Add to prep, then commit to db
    db.add(newUser)
    db.commit()
  except:
    # insert failure, rollback db commit and send error message to front end
    print(sys.exe_info()[0])
    db.rollback()
    return jsonify(message = 'Signup Failed'), 500

# Sessions - clear existing session data and create two new session properties for user_id and loggedIn 
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True
# Return JSON notation that includes the id of the new user to front end
  return jsonify(id = newUser.id)

# ADD LOGOUT ROUTE
@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables, add 204 status for no information
  session.clear()
  return '', 204

# ADD LOGIN ROUTE
@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()
#   Add try-except statement to handle incorrect credentials
  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])

  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400

  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)

# === COMMENT ROUTES ====
@bp.route('/comments', methods=['POST'])
@login_required
def comment():
  data = request.get_json()
  db = get_db()

  try:
  # create a new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newComment)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Comment failed'), 500

  return jsonify(id = newComment.id)


# === UPVOTE ROUTE ====
@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # create a new vote with incoming id and session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500

  return '', 204

# === CREATE NEW POST ROUTE ====
@bp.route('/posts', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  db = get_db()

  try:
    # create a new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)

# === UPDATE POST ROUTE ====
  # Using id route parameter  
@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
  data = request.get_json()
  db = get_db()

  try:
    # Retrieve post and update title property
    post = db.query(Post).filter(Post.id == id).one()
    post.title = data['title']
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204

# === DELETE POST ROUTE ====
@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
  db = get_db()

  try:
    # delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204