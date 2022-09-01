from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

# User class inherits the initial Base class created in db package
# Set up User table and columns
class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False, unique=True)
  password = Column(String(100), nullable=False)

#Add validation through email

  @validates('email')
  def validate_email(self, key, email):
    # make sure email address contains @ character using assert keyword
    assert '@' in email
    return email
#Add validation for password - length of over 4 characters using assert keyword
  @validates('password')
  def validate_password(self, key, password):
    assert len(password) > 4

    return password