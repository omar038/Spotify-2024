import pandas as pd
import requests
from time import sleep, time

# Your Spotify API credentials
CLIENT_ID = 'b2096cdc92e04fa8ac468d1af08c02b4'
CLIENT_SECRET = '809a0ecee8dc4fe29c7ad12c77f9e3e9'

# Get a new access token
def get_access_token():
    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
    )
    return auth_response.json().get('access_token')

# Initialize token and timestamp
access_token = get_access_token()
token_acquired_time = time()
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Refresh token if it's older than 50 minutes
def refresh_token_if_needed():
    global access_token, token_acquired_time, headers
    if time() - token_acquired_time > 3000:  # 50 minutes
        access_token = get_access_token()
        token_acquired_time = time()
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

# Load your dataset
df = pd.read_csv('Spotify2024.csv', encoding='ISO-8859-1')
df['Genre'] = ''
df['Album Cover URL'] = ''

def enrich_song(track, artist):
    refresh_token_if_needed()

    query = f'track:{track} artist:{artist}'
    search_url = f'https://api.spotify.com/v1/search?q={requests.utils.quote(query)}&type=track&limit=1'

    try:
        r = requests.get(search_url, headers=headers)
        if r.status_code != 200:
            return '', ''
        results = r.json().get('tracks', {}).get('items', [])
        if not results:
            return '', ''

        track_info = results[0]
        album_cover = track_info['album']['images'][0]['url'] if track_info['album']['images'] else ''
        artist_id = track_info['artists'][0]['id']

        # Get artist genres
        artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
        r_artist = requests.get(artist_url, headers=headers)
        if r_artist.status_code != 200:
            return '', ''
        artist_data = r_artist.json()
        genres = artist_data.get('genres', [])
        genre = genres[0] if genres else ''

        return genre, album_cover

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return '', ''
    except Exception as e:
        print(f"Error on {track} by {artist}: {e}")
        return '', ''

# Loop through dataset
for idx, row in df.iterrows():
    genre, cover_url = enrich_song(row['Track'], row['Artist'])
    df.at[idx, 'Genre'] = genre
    df.at[idx, 'Album Cover URL'] = cover_url
    print(f"{idx+1}/{len(df)}: {row['Track']} by {row['Artist']} → Genre: {genre}, Cover: {cover_url}")
    sleep(0.3)  # Slightly slower to be safer with API limits

# Save final result
df.to_csv('Spotify2024_with_genres_and_covers.csv', index=False, encoding='utf-8')
print("✅ All done! Enriched CSV saved.")
