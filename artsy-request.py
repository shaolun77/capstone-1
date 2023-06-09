import requests

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

# print(API_KEY)


def get_artists():
    url = "https://api.artsy.net/api/artists"
    headers = {
        "Accept": "application/vnd.artsy-v2+json",
        "X-Xapp-Token": API_KEY
    }
    response = requests.get(url, headers=headers)
    artists_data = response.json()

    print(artists_data)

    if "_embedded" in artists_data and "artists" in artists_data["_embedded"]:
        artists = artists_data["_embedded"]["artists"]

        for artist in artists_data["_embedded"]["artists"]:
            artist_name = artist.get('name')
            if artist_name:
                print(f'Artist Name: {artist_name}')
                print('---')
            else:
                print("Artist name not available")
    else:
        print("No artists found.")


# # Set the number of fairs you want to retrieve
# fair_count = 20

# # Construct the API request URL with query parameters
# api_url = f'https://api.artsy.net/api/fairs?size={fair_count}'

# # Set the request headers with the access token
# headers = {
#     'Accept': 'application/vnd.artsy-v2+json',
#     'X-Xapp-Token': access_token
# }

# # Send the API request
# response = requests.get(api_url, headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the JSON response
#     fairs_data = response.json()

#     # Extract fair information from the response
#     for fair in fairs_data['_embedded']['fairs']:
#         fair_name = fair['name']
#         fair_start_date = fair['start_at']
#         fair_end_date = fair['end_at']

#         # Do something with the fair information
#         print(f'Fair Name: {fair_name}')
#         print(f'Start Date: {fair_start_date}')
#         print(f'End Date: {fair_end_date}')
#         print('---')
# else:
#     # Handle the case when the request was not successful
#     print(f'Error: {response.status_code} - {response.text}')


def get_partners():
    url = "https://api.artsy.net/api/partners"

    headers = {
        "Accept": "application/vnd.artsy-v2+json",
        "X-Xapp-Token": API_KEY
    }
    response = requests.get(url, headers=headers)
    partners_data = response.json()

    print(partners_data)

# Create a function to get the shows from the Artsy API


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

            return galleries
        else:
            return "Failed to retrieve gallery information."
    else:
        return "Failed to retrieve fair information."


def art_gallery(gallery_id):
    """Show specific gallery:

    - List the artworks that the gallery is showing.
    - Allow users to favorite them.
    """

    # Construct the partner API URL
    partner_url = f"https://api.artsy.net/api/partners/{gallery_id}"
    headers = {
        "Accept": "application/vnd.artsy-v2+json",
        "X-Xapp-Token": API_KEY
    }
    # Make the partner API request
    partner_response = requests.get(partner_url, headers=headers)

    if partner_response.status_code == 200:
        partner_data = partner_response.json()
        partner = partner_data

        print(partner)

        # Extract the fair ID from the shows information
        shows_url = partner['_links']['shows']['href']
        shows_response = requests.get(shows_url, headers=headers)

        if shows_response.status_code == 200:
            shows_data = shows_response.json()
            first_show = shows_data['_embedded']['shows'][0]
            fair_id = first_show['_links']['fair']['href'].split('/')[-1]

            # Construct the shows API URL with the fair_id and partner_id
            shows_url = f"https://api.artsy.net/api/shows?fair_id={fair_id}&partner_id={gallery_id}"

            # Make the shows API request
            shows_response = requests.get(shows_url, headers=headers)

            if shows_response.status_code == 200:
                shows_data = shows_response.json()
                shows = shows_data['_embedded']['shows']

                print(shows)

                return shows
            else:
                # Handle error when retrieving show information
                return "Failed to retrieve show information."
        else:
            # Handle error when retrieving shows information
            return "Failed to retrieve shows information."
    else:
        # Handle error when retrieving partner information
        return "Failed to retrieve gallery information."


def show(show_id):
    show_url = f"https://api.artsy.net/api/shows/{show_id}"
    headers = {
        "Accept": "application/vnd.artsy-v2+json",
        "X-Xapp-Token": API_KEY
    }

    # Make the show API request
    show_response = requests.get(show_url, headers=headers)

    if show_response.status_code == 200:
        show_data = show_response.json()
        show = show_data

        # Retrieve the artworks associated with the show
        artworks_url = show_data['_links']['artworks']['href']
        print("Artworks URL:", artworks_url)  # Check the URL

        artworks_response = requests.get(artworks_url, headers=headers)

        if artworks_response.status_code == 200:
            artworks_data = artworks_response.json()
            artworks = artworks_data['_embedded']['artworks']

            if artworks:
                print("Artworks:", artworks)  # Check the artworks data
            else:
                print("No artworks found for the show.")

            return render_template('show.html', show=show, artworks=artworks)
        else:
            return "Failed to retrieve artworks for the show."
    else:
        return "Failed to retrieve show information."
