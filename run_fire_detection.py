#!/usr/bin/env python3
"""
Peril Detection Pipeline
========================
Automated pipeline to search for peril-related tweets and verify incidents.

This script runs the complete workflow:
1. Search for peril-related tweets from the last 72 hours
2. Verify incidents using AI
3. Generate Excel and JSON reports
4. Send results via email

Usage:
    python run_fire_detection.py
"""

import os
import sys
import subprocess
import time
from datetime import datetime
from dotenv import load_dotenv
import glob

# Load environment variables from .env file
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        "TWITTER_API_KEY",
        "OPENAI_API_KEY",
        "EMAIL_ADDRESS",
        "EMAIL_PASSWORD"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these in your .env file:")
        print("TWITTER_API_KEY=your_twitter_api_key")
        print("OPENAI_API_KEY=your_openai_api_key")
        print("EMAIL_ADDRESS=your_email@gmail.com")
        print("EMAIL_PASSWORD=your_app_password")
        return False
    
    return True

def run_tweet_search():
    """Run the tweet search script"""
    print("🔍 Step 1: Searching for peril-related tweets...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "tweet_peril_search.py"], 
                              check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running tweet search: {e}")
        return False

def run_verification():
    """Run the tweet verification script"""
    print("\n🤖 Step 2: Verifying peril incidents with AI...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "verify_tweets.py"], 
                              check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running verification: {e}")
        return False

def main():
    """Main execution function"""
    print("🚨 Peril Detection Pipeline")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Step 1: Tweet Search
    if not run_tweet_search():
        print("❌ Tweet search failed. Stopping pipeline.")
        sys.exit(1)
    
    # Check if peril_tweets_72h_*.json was created in output directory
    peril_tweets_files = glob.glob("output/peril_tweets_72h_*.json")
    if not peril_tweets_files:
        print("❌ No peril_tweets_72h_*.json files found after search. Stopping pipeline.")
        sys.exit(1)
    
    print(f"✅ Found {len(peril_tweets_files)} peril tweet files")
    latest_file = max(peril_tweets_files, key=os.path.getctime)
    print(f"📁 Latest file: {latest_file}")
    
    # Step 2: Verification
    if not run_verification():
        print("❌ Verification failed. Stopping pipeline.")
        sys.exit(1)
    
    print("\n🎉 Pipeline completed successfully!")
    print("=" * 50)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📁 Check the 'output' folder for results")
    print("📧 Results have been sent via email")

if __name__ == "__main__":
    main() 