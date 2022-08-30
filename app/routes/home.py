from flask import Blueprint, render_template

bp = Blueprint('home', __name__, url_prefix='/')

# @bp decorator before the function turns it into a route
@bp.route('/')
def index():
  return render_template('homepage.html')

@bp.route('/login')
def login():
  return render_template('login.html')

# Id represents the parameter in the URL. We capture it in single(id)
@bp.route('/post/<id>')
def single(id):
  return render_template('single-post.html')