# Add import statements
import sys
from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db

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