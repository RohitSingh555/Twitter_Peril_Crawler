"""
tweet_fire_search.py
--------------------
Fetches the latest fire‑related tweets across U.S. states and core EMS accounts.

Usage:
    export TWITTER_API_KEY="YOUR_API_KEY"
    python tweet_fire_search.py
"""

import os
import json
import time
import requests
import itertools
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
if not TWITTER_API_KEY:
    print("Error: TWITTER_API_KEY environment variable is required")
    print("Please set your Twitter API key in a .env file or environment variable.")
    exit(1)

# Get hours from environment variable, default to 72 if not set
SEARCH_HOURS = os.getenv('SEARCH_HOURS', '72')
try:
    SEARCH_HOURS = int(SEARCH_HOURS)
except ValueError:
    print(f"Warning: Invalid SEARCH_HOURS value '{SEARCH_HOURS}', using default 72 hours")
    SEARCH_HOURS = 72

# Constants
US_STATES = [
    "Arizona", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Idaho", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Michigan", "Minnesota", "Mississippi", "Montana", "Nebraska",
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "North Carolina",
    "North Dakota", "Ohio", "Oklahoma", "Oregon", "South Carolina", "Tennessee",
    "Texas", "US Virgin Islands", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming", "DC"
]

def load_damage_keywords() -> List[str]:
    """Load damage keywords from JSON file."""
    try:
        with open('damage_keywords.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('damage_keywords', [])
    except FileNotFoundError:
        print("Warning: damage_keywords.json not found, using default keywords")
        return ["explosion damage", "lightning damage", "flood damage", "freezing damage", 
                "tornado damage", "storm damage", "hail damage", "pipe burst damage", 
                "structure damage", "water damage", "smoke damage"]
    except json.JSONDecodeError:
        print("Warning: Invalid JSON in damage_keywords.json, using default keywords")
        return ["explosion damage", "lightning damage", "flood damage", "freezing damage", 
                "tornado damage", "storm damage", "hail damage", "pipe burst damage", 
                "structure damage", "water damage", "smoke damage"]

# Load damage keywords
DAMAGE_KEYWORDS = load_damage_keywords()

def generate_search_combinations() -> List[str]:
    """Generate all possible search combinations using permutations and combinations of damage keywords."""
    combinations = []
    
    # Single keyword combinations
    for state in US_STATES:
        for keyword in DAMAGE_KEYWORDS:
            combinations.append(f"{state} {keyword}")
    
    # Two keyword combinations (permutations)
    for state in US_STATES:
        for combo in itertools.permutations(DAMAGE_KEYWORDS, 2):
            combinations.append(f"{state} {' '.join(combo)}")
    
    # Three keyword combinations (permutations)
    for state in US_STATES:
        for combo in itertools.permutations(DAMAGE_KEYWORDS, 3):
            combinations.append(f"{state} {' '.join(combo)}")
    
    return combinations

FIRE_ACCOUNTS = [
    "@DFWscanner", "@DallasTexasTV", "@NWSSanAntonio", "@FriscoFFD", "@RedCrossTXGC",
    "@whatsupTucson", "@WacoTXFire", "@SouthMetroPIO", "@NWSBoulder", "@SeattleFire",
    "@CityofMiamiFire", "@PeterNewcomb41", "@ffxfirerescue", "@ScannerRadioDFW",
    "@sfgafirerescue", "@THEJFRD", "@ChicagoMWeather", "@ToledoFire", "@AustinFireInfo"
]

# Generate search combinations using damage keywords
DAMAGE_SEARCH_COMBINATIONS = generate_search_combinations()

def get_all_fire_accounts() -> List[str]:
    """Returns fire account handles without '@' prefix."""
    return [account[1:] for account in FIRE_ACCOUNTS]

def get_all_damage_search_combinations() -> List[str]:
    """Returns all damage search combinations."""
    return DAMAGE_SEARCH_COMBINATIONS

def handle_rate_limit(response: requests.Response) -> None:
    """Handle rate limiting by sleeping for a fixed time."""
    if response.status_code == 429:
        print("Rate limited. Sleeping for 60 seconds...")
        time.sleep(60)

def fetch_tweets(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """Fetch tweets from Kaito Twitter API for a given query."""
    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    headers = {
        "X-API-Key": TWITTER_API_KEY
    }
    params = {
        "query": f"{query} within_time:{SEARCH_HOURS}h",
        "queryType": "Latest"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 429:
            handle_rate_limit(response)
            # Retry the request after rate limit handling
            response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            tweets = data.get('tweets', [])
            # Limit to max_results
            return tweets[:max_results]
        else:
            print(f"Error fetching tweets for query '{query}': {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Exception while fetching tweets for query '{query}': {str(e)}")
        return []

def fetch_user_tweets(username: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """Fetch latest tweets from a specific user using Kaito Twitter API."""
    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    headers = {
        "X-API-Key": TWITTER_API_KEY
    }
    params = {
        "query": f"from:{username} within_time:{SEARCH_HOURS}h",
        "queryType": "Latest"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 429:
            handle_rate_limit(response)
            # Retry the request after rate limit handling
            response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            tweets = data.get('tweets', [])
            # Limit to max_results
            return tweets[:max_results]
        else:
            print(f"Error fetching tweets for user '{username}': {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Exception while fetching tweets for user '{username}': {str(e)}")
        return []

def deduplicate_tweets(tweets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate tweets based on tweet ID."""
    seen_ids = set()
    unique_tweets = []
    
    for tweet in tweets:
        tweet_id = tweet.get('id')
        if tweet_id and tweet_id not in seen_ids:
            seen_ids.add(tweet_id)
            unique_tweets.append(tweet)
    
    return unique_tweets

def save_tweets_to_file(tweets: List[Dict[str, Any]], filename: str = "damage_tweets.json") -> None:
    """Save tweets to JSON file with deduplication."""
    # Load existing tweets if file exists
    existing_tweets = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_tweets = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_tweets = []
    
    # Combine existing and new tweets
    all_tweets = existing_tweets + tweets
    
    # Deduplicate by tweet ID
    unique_tweets = deduplicate_tweets(all_tweets)
    
    # Save to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(unique_tweets, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(unique_tweets)} unique tweets to {filename}")

def main():
    """Main routine to fetch and save damage-related tweets."""
    print("Starting damage tweet search...")
    
    # Generate unique timestamped filename
    dt_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"damage_tweets_72h_{dt_str}.json"
    
    total_queries = 0
    total_tweets_fetched = 0
    
    # Fetch tweets for search combinations
    search_combinations = get_all_damage_search_combinations()
    print(f"Fetching tweets for {len(search_combinations)} search combinations...")
    
    for i, query in enumerate(search_combinations, 1):
        print(f"Query {i}/{len(search_combinations)}: {query}")
        tweets = fetch_tweets(query)
        
        if tweets:
            total_tweets_fetched += len(tweets)
            # Save immediately after each successful query
            save_tweets_to_file(tweets, output_file)
            print(f"  -> Fetched {len(tweets)} tweets")
        
        total_queries += 1
        
        # Small delay to be respectful to the API
        time.sleep(0.1)
    
    # Fetch tweets from damage-related accounts
    fire_accounts = get_all_fire_accounts()
    print(f"\nFetching tweets from {len(fire_accounts)} damage-related accounts...")
    
    for i, username in enumerate(fire_accounts, 1):
        print(f"Account {i}/{len(fire_accounts)}: {username}")
        tweets = fetch_user_tweets(username)
        
        if tweets:
            total_tweets_fetched += len(tweets)
            # Save immediately after each successful query
            save_tweets_to_file(tweets, output_file)
            print(f"  -> Fetched {len(tweets)} tweets")
        
        total_queries += 1
        
        # Small delay to be respectful to the API
        time.sleep(0.1)
    
    # Print final summary
    print(f"\n=== Final Summary ===")
    print(f"Total queries run: {total_queries}")
    print(f"Total tweets fetched: {total_tweets_fetched}")
    print(f"Output file: {os.path.abspath(output_file)}")
    
    # Show final count of unique tweets
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            final_tweets = json.load(f)
        print(f"Final unique tweets in file: {len(final_tweets)}")
    except Exception as e:
        print(f"Error reading final file: {e}")

if __name__ == "__main__":
    main() 