import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(40), nullable=False, unique=True)
    email= Column(String (60), nullable= False, unique=True)
    password= Column(String (40), nullable = False)

    # Relationship to represent the users a user is following
    following = relationship('User', secondary='followers', primaryjoin='User.id==followers.c.follower_id', secondaryjoin='User.id==followers.c.following_id', backref='followers')

    # Relationship to represent posts created by the user
    posts = relationship('Post', back_populates='user')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    caption = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=False)

    # Foreign key relationship to connect with the User who created the post
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='posts')

    # Relationship to represent comments on the post
    comments = relationship('Comment', back_populates='post')

    # Relationship to represent likes on the post
    likes = relationship('Like', back_populates='post')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)

    # Foreign key relationship to connect with the User who made the comment
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')

    # Foreign key relationship to connect with the Post the comment is on
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='comments')

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)

    # Foreign key relationship to connect with the User who made the like
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')

    # Foreign key relationship to connect with the Post that was liked
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='likes')


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
