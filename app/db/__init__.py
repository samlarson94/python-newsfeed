from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

load_dotenv()

# connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()
# DEV note:
    # The engine variable manages the overall connection to the database.
    # The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations.
    # The Base class variable helps us map the models to real MySQL tables.

def init_db():
  Base.metadata.create_all(engine)
  app.teardown_appcontext(close_db)

# Set up function to return new session-connection object
    #Utilizing "g" object  to save the current connection and avoid repeat connections
def get_db():
  if 'db' not in g:
    # store db connection in app context
    g.db = Session()
  return g.db

# Set up connection to database that will work on Heroku & other hosting sites
def close_db(e=None):
  db = g.pop('db', None)
  # pop method attempts to find and remove db from the g object.
    # if db exists, then db.close will end the connection
    # The app.teardown_appcontext(close_db), in init_db(), flask method will automate db.close

  if db is not None:
    db.close()