import tweepy
import requests
from bs4 import BeautifulSoup
import json

# Twitter API credentials
TWITTER_CONSUMER_KEY = 'your_consumer_key'
TWITTER_CONSUMER_SECRET = 'your_consumer_secret'
TWITTER_ACCESS_TOKEN = 'your_access_token'
TWITTER_ACCESS_TOKEN_SECRET = 'your_access_token_secret'

def extract_twitter_data(query, count=100):
    """Extract tweets containing specific keywords."""
    auth = tweepy.OAuth1UserHandler(
        TWITTER_CONSUMER_KEY, 
        TWITTER_CONSUMER_SECRET, 
        TWITTER_ACCESS_TOKEN, 
        TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    tweets = tweepy.Cursor(
        api.search_tweets, q=query, lang='en', tweet_mode='extended'
    ).items(count)

    twitter_data = []
    for tweet in tweets:
        twitter_data.append({
            'platform': 'Twitter',
            'user': tweet.user.screen_name,
            'content': tweet.full_text
        })
    return twitter_data

def extract_instagram_data(tag):
    """Extract public posts from Instagram for a specific tag."""
    url = f'https://www.instagram.com/explore/tags/{tag}/'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch data from Instagram. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
    
    if not script_tag:
        print("Failed to find the script tag containing JSON data.")
        return []

    json_data = script_tag.string.split(' = ', 1)[1].rstrip(';')
    data = json.loads(json_data)

    posts = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    instagram_data = []

    for post in posts:
        try:
            instagram_data.append({
                'platform': 'Instagram',
                'user': None,  # Instagram doesn't provide user details in public data
                'email': None,  # Email not available from Instagram public data
                'content': post['node']['edge_media_to_caption']['edges'][0]['node']['text']
            })
        except IndexError:
            pass  # Skip posts without captions

    return instagram_data

def save_data_as_json(data, filename):
    """Save extracted data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    print("This script is for data extraction. Use the main function in another file to call these methods.")
