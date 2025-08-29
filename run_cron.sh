#!/bin/bash

# Navigate to project directory
cd /root/twitter_paid_api_crawler

# Activate virtual environment
source env/bin/activate

# Ensure output directory exists
mkdir -p output

# Run the main peril detection script
python tweet_peril_search.py

# Optional: Run additional pipeline scripts if needed
# python verify_tweets.py
# python clean_tweets.py
# python tweet_analyzer.py 