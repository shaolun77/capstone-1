"""Seed database with data from Artsy API."""

import requests

from flask import Flask
from app import db
from models import Artist, Artwork, Gallery, ArtFair


db.drop_all()
db.create_all()

# Get Artsy API TOKEN:
# Set your Client ID and Client Secret
client_id = 'd23126726160b1141ff8'
client_secret = '5e636238807b6ade106aa3738d75e56d'

# Construct the API request URL
token_url = 'https://api.artsy.net/api/tokens/xapp_token'

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


artfair_url = 'https://api.artsy.net/api/artfairs/{artfair_id}'


# print(API_KEY)

   # Seed the artists database
   for fair_data in fairs:
        fair = Fair(
            fair_id=fair_data['id'],
            fair_name=fair_data['name'],
            fair_about=fair_data['about'],
            fair_start_date=fair_data['start_at'],
            fair_end_date=fair_data['end_at']
        )
        db.session.add(fair)

    db.session.commit()

    else:
        print("No fairs found.")


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

    # Process the fairs
        for fair in fairs:
            fair_id = fair["id"]
            fair_name = fair["name"]
        # Extract other attributes as needed

        # Do something with the fair data (e.g., store in database, display in your application)
            print(f"Fair ID: {fair_id}")
            print(f"Fair Name: {fair_name}")
            print("--------------------")
    else:
        # Request was not successful, handle the error
        print(f"Error: {response.status_code} - {response.text}")
