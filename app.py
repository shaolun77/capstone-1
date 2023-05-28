import os
import requests

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, UserEditForm, LoginForm
from models import db, connect_db, User, Fair, Gallery

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///artfairhelper'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

db.init_app(app)

with app.app_context():
    db.create_all()

connect_db(app)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")


##############################################################################
# General user routes:


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    # need to show list of favorited artworks

    # likes = [message.id for message in user.likes]
    return render_template('users/show.html', user=user)


# @app.route('/users/<int:user_id>/likes', methods=["GET"])
# def show_likes(user_id):
#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")

#     user = User.query.get_or_404(user_id)
#     return render_template('users/likes.html', user=user, likes=user.likes)


# @app.route('/messages/<int:message_id>/like', methods=['POST'])
# def add_like(message_id):
#     """Toggle a liked message for the currently-logged-in user."""

#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")

#     liked_message = Message.query.get_or_404(message_id)
#     if liked_message.user_id == g.user.id:
#         return abort(403)

#     user_likes = g.user.likes

#     if liked_message in user_likes:
#         g.user.likes = [like for like in user_likes if like != liked_message]
#     else:
#         g.user.likes.append(liked_message)

#     db.session.commit()

#     return redirect("/")


@app.route('/users/profile', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"
            user.header_image_url = form.header_image_url.data or "/static/images/warbler-hero.jpg"
            user.bio = form.bio.data

            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit.html', form=form, user_id=user.id)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


##############################################################################
# Homepage and error pages

# Set your Client ID and Client Secret
client_id = 'd23126726160b1141ff8'
client_secret = '5e636238807b6ade106aa3738d75e56d'

# Construct the API request URL
token_url = 'https://api.artsy.net/api/tokens/xapp_token'
# api_url = 'https://api.artsy.net/api/artists'

# Set the request payload with client_id and client_secret
payload = {
    'client_id': client_id,
    'client_secret': client_secret
}

# Send the API request to obtain the access token
response = requests.post(token_url, data=payload)

# Parse the JSON response
token_data = response.json()

API_KEY = token_data['token']


def get_fairs():
    url = "https://api.artsy.net/api/fairs"
    headers = {
        "Accept": "application/vnd.artsy-v2+json",
        "X-Xapp-Token": API_KEY
    }

# Set the query parameters, including the status and size (number of results)
    params = {
        "status": "upcoming",  # Filter by upcoming fairs
        "size": 10,  # Number of fairs to retrieve
        # Sort by start date in ascending order (earliest first)
        "sort": "start_at"
    }

# Make the GET request
    response = requests.get(url, headers=headers, params=params)

# Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

    # Extract the list of fairs from the response
        fairs = data["_embedded"]["fairs"]
        # print(fairs)

    # Return the list of fairs
        return fairs

    # Return an empty list if the request was not successful
    return []


@app.route('/')
def homepage():
    """Show homepage:

    - call the get_fairs function and seed the database
    - anon users: list of art fairs 
    - logged in: below list of art fairs is a list of their favorited artworks. 

    """
    fairs = get_fairs()

    # for fair in fairs:
    #     fair['id'] = str(fair['id'])

# Store the fair data in the database (using SQLAlchemy)
    # for fair_data in fairs:
    #     fair = Fair(
    #         fair_id=fair_data["id"],
    #         fair_name=fair_data["name"],
    #         fair_about=fair_data["about"],
    #         fair_start_date=fair_data["start_at"],
    #         fair_end_date=fair_data["end_at"]
    #     )
    #     db.session.add(fair)

    # db.session.commit()

    # Pass the fair data to the template for rendering
    return render_template('homepage.html', fairs=fairs)

    # if g.user:
    #     following_ids = [f.id for f in g.user.following] + [g.user.id]

    #     messages = (Message
    #                 .query
    #                 .filter(Message.user_id.in_(following_ids))
    #                 .order_by(Message.timestamp.desc())
    #                 .limit(100)
    #                 .all())

    #     liked_msg_ids = [msg.id for msg in g.user.likes]

    #     return render_template('home.html', messages=messages, likes=liked_msg_ids)

    # else:
    #     return render_template('home-anon.html')


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404

##############################################################################
# Art Fair and Gallery pages


@app.route('/fairs/<string:fair_id>')
def art_fair(fair_id):
    """Show specific art fair:

    - Retrieve fair information from the Artsy API using the fair_id.
    - List the galleries participating in the art fair.
    """

    # Construct the fair API URL with the fair_id
    fair_url = f"https://api.artsy.net/api/fairs/{fair_id}"
    headers = {
        "Accept": "application/vnd.artsy-v2+json",
        "X-Xapp-Token": API_KEY
    }

    # Make the fair API request
    fair_response = requests.get(fair_url, headers=headers)

    if fair_response.status_code == 200:
        fair_data = fair_response.json()
        fair = fair_data

        # Construct the gallery API URL with the fair_id
        gallery_url = f"https://api.artsy.net/api/shows?fair_id={fair_id}"

        # Make the gallery API request
        gallery_response = requests.get(gallery_url, headers=headers)

        if gallery_response.status_code == 200:
            gallery_data = gallery_response.json()
            galleries = gallery_data["_embedded"]["shows"]

            return render_template('fairs.html', fair=fair, galleries=galleries)
        else:
            return "Failed to retrieve gallery information."
    else:
        return "Failed to retrieve fair information."


@app.route('/galleries/<int:gallery_id>')
def art_gallery(gallery_id):
    """Show specific gallery:

    - List the artworks that the gallery is showing.
    - Allow users to favorite them.
    """

    # Construct the gallery API URL with the gallery_id
    gallery_url = f"https://api.artsy.net/api/shows/{gallery_id}"

    # Make the gallery API request
    gallery_response = requests.get(gallery_url, headers=headers)

    if gallery_response.status_code == 200:
        gallery_data = gallery_response.json()
        gallery = gallery_data

        # Extract the artworks brought by the gallery
        artworks_url = gallery_data['_links']['artworks']['href']
        artworks_response = requests.get(artworks_url, headers=headers)
        if artworks_response.status_code == 200:
            artworks_data = artworks_response.json()
            artworks = artworks_data['_embedded']['artworks']
        else:
            artworks = []

        return render_template('galleries.html', gallery=gallery, artworks=artworks)
    else:
        return "Failed to retrieve gallery information."


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
