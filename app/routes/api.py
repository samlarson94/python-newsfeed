# Add import statements
from flask import Blueprint, request, jsonify
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

# ADD SIGN UP ROUTE
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

# Create New User - use Python dictionary notation
  newUser = User(
    username = data['username'],
    email = data['email'],
    password = data['password']
  )

# Save to Database - Add to prep, then commit to db
  db.add(newUser)
  db.commit()
  
# Return JSON notation that includes the id of the new user to front end
  return jsonify(id = newUser.id)