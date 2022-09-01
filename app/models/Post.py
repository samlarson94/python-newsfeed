from datetime import datetime
from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# Create Post class to extend Base
    # Add ForeignKeys to reference users table
    # Add created_at and updated_at fields that use Python's built-in datetime module to add timestamps
class Post(Base):
  __tablename__ = 'posts'
  id= Column(Integer, primary_key=True)
  title = Column(String(100), nullable=False)
  post_url = Column(String(100), nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
# Add relationships to the User and Comment models
  user = relationship('User')
  comments = relationship('Comment', cascade='all,delete')
    # cascade will delete all of a post's comments when a post is deleted