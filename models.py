"""SQLAlchemy models for Art Fair helper."""


from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


# Define your models
class Artist(db.Model):
    """Artist model."""

    __tablename__ = 'artists'

    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(255), nullable=False)
    artist_birthdate = db.Column(db.Date)
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.gallery_id'))
    gallery = db.relationship('Gallery', backref='artists')
    artworks = db.relationship('Artwork', backref='artist')


class Artwork(db.Model):

    __tablename__ = 'artworks'

    artwork_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))
    artwork_title = db.Column(db.String(255))
    artwork_medium = db.Column(db.String(255))
    artwork_price = db.Column(db.Integer)
    artwork_year = db.Column(db.Integer)
    artwork_image = db.Column(db.Text)
    artist = db.relationship('Artist', backref='artworks')
    favorites = db.relationship('Favorite', backref='artwork')


class Gallery(db.Model):

    __tablename__ = 'galleries'

    gallery_id = db.Column(db.Integer, primary_key=True)
    gallery_name = db.Column(db.String(255), nullable=False)
    gallery_location = db.Column(db.String(255))
    art_fair_id = db.Column(db.Integer, db.ForeignKey('art_fairs.art_fair_id'))
    art_fair = db.relationship('ArtFair', backref='galleries')
    artists = db.relationship('Artist', backref='gallery')


class Fair(db.Model):

    __tablename__ = 'art_fairs'

    fair_id = db.Column(db.Integer, primary_key=True)
    fair_name = db.Column(db.String(255), nullable=False)
    fair_about = db.Column(db.String(255))
    fair_start_date = db.Column(db.Date)
    fair_end_date = db.Column(db.Date)
    galleries = db.relationship('Gallery', backref='art_fair')
    gallery_art_fairs = db.relationship('GalleryArtFair', backref='art_fair')


class GalleryArtFair(db.Model):
    __tablename__ = 'gallery_art_fairs'
    gallery_art_fair_id = db.Column(db.Integer, primary_key=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.gallery_id'))
    art_fair_id = db.Column(db.Integer, db.ForeignKey('art_fairs.art_fair_id'))

    # gallery = relationship('Gallery', backref='gallery_art_fairs')
    # art_fair = relationship('ArtFair', backref='gallery_art_fairs')


class User(db.Model):
        """User in the system."""

    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), unique=True)
    user_password = db.Column(db.String(255))
    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    header_image_url = db.Column(
        db.Text,
        default="/static/images/warbler-hero.jpg"
    )
    favorites = db.relationship('Favorite', backref='user')

    # likes = db.relationship(
    #     'Message',
    #     secondary="likes")

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

#this user id favorited this artwork id

class Favorite(db.Model):
    
    __tablename__ = 'favorites'
    
    favorite_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    artwork_id = Column(Integer, ForeignKey('artworks.artwork_id'))
    artwork = relationship('Artwork', backref='favorites')
    user = relationship('User', backref='favorites')


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
    
    
    
    
    
    
    

# class User(db.Model):
#     """User in the system."""

#     __tablename__ = 'users'

    # id = db.Column(db.Integer,primary_key=True,)
    # email = db.Column(db.Text,
    #     nullable=False,
    #     unique=True,)
    # username = db.Column(
    #     db.Text,
    #     nullable=False,
    #     unique=True,)
    # image_url = db.Column(
    #     db.Text,
    #     default="/static/images/default-pic.png",)
    # header_image_url = db.Column(
    #     db.Text,
    #     default="/static/images/warbler-hero.jpg")
    # bio = db.Column(
    #     db.Text,)
    # location = db.Column(
    #     db.Text,)
    # password = db.Column(
    #     db.Text,
    #     nullable=False,)
    # messages = db.relationship('Message')
    # followers = db.relationship(
    #     "User",
    #     secondary="follows",
    #     primaryjoin=(Follows.user_being_followed_id == id),
    #     secondaryjoin=(Follows.user_following_id == id))
    # following = db.relationship(
    #     "User",
    #     secondary="follows",
    #     primaryjoin=(Follows.user_following_id == id),
    #     secondaryjoin=(Follows.user_being_followed_id == id))




# from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship

# Create a SQLAlchemy engine to connect to your database
# engine = create_engine(
#     'postgresql://your_username:your_password@your_database_host:your_database_port/your_database_name')

# Create a base class for your declarative models
# Base = declarative_base()

# Define your models


# class Artist(Base):
#     __tablename__ = 'artists'
#     artist_id = Column(Integer, primary_key=True)
#     artist_name = Column(String(255), nullable=False)
#     artist_birthdate = Column(Date)
#     artist_nationality = Column(String(255))
#     gallery_id = Column(Integer, ForeignKey('galleries.gallery_id'))
#     gallery = relationship('Gallery', back_populates='artists')
#     artworks = relationship('Artwork', back_populates='artist')
