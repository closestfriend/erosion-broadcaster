#!/usr/bin/env python3
"""
Twitter Integration for Erosion Broadcaster
Handles actual posting to Twitter/X API
"""

import os
import tweepy
from typing import Optional
from pathlib import Path

class TwitterPoster:
    def __init__(self):
        """Initialize Twitter API connection using environment variables"""
        self.api = None
        self.client = None
        self.connected = False
        
        # Load from .local.env if it exists
        self._load_local_env()
        
        # Get credentials from environment
        api_key = os.environ.get('TWITTER_API_KEY')
        api_secret = os.environ.get('TWITTER_API_SECRET')
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_secret = os.environ.get('TWITTER_ACCESS_SECRET')
        
        if all([api_key, api_secret, access_token, access_secret]):
            try:
                # Twitter API v2 (for posting)
                self.client = tweepy.Client(
                    consumer_key=api_key,
                    consumer_secret=api_secret,
                    access_token=access_token,
                    access_token_secret=access_secret
                )
                
                # Verify credentials work
                self.verify_credentials()
                self.connected = True
                print("✓ Twitter API connected successfully")
                
            except Exception as e:
                print(f"⚠ Twitter API connection failed: {e}")
                self.connected = False
        else:
            print("⚠ Twitter API credentials not found in environment")
            self.connected = False
    
    def _load_local_env(self):
        """Load environment variables from .env.local file if it exists"""
        env_file = Path(__file__).parent / '.env.local'
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Only set if not already in environment (GitHub secrets take precedence)
                        if key not in os.environ:
                            os.environ[key] = value
    
    def verify_credentials(self):
        """Verify that we can connect to Twitter"""
        try:
            # Try to get authenticated user info
            me = self.client.get_me()
            if me and me.data:
                print(f"Authenticated as: @{me.data.username}")
                return True
        except Exception as e:
            print(f"Credential verification failed: {e}")
            return False
    
    def post_tweet(self, text: str) -> Optional[str]:
        """
        Post a tweet and return the tweet ID if successful
        
        Args:
            text: The tweet text (max 280 characters)
            
        Returns:
            Tweet ID if successful, None otherwise
        """
        if not self.connected:
            print("Cannot post: Twitter API not connected")
            return None
        
        if len(text) > 280:
            print(f"Warning: Tweet too long ({len(text)} chars), truncating...")
            text = text[:277] + "..."
        
        try:
            response = self.client.create_tweet(text=text)
            
            if response and response.data:
                tweet_id = response.data['id']
                print(f"✓ Tweet posted successfully: ID {tweet_id}")
                return tweet_id
            else:
                print("⚠ Tweet may have failed: No response data")
                return None
                
        except tweepy.errors.TooManyRequests:
            print("⚠ Rate limit exceeded. Try again later.")
            return None
        except tweepy.errors.Forbidden as e:
            print(f"⚠ Forbidden: {e}")
            print("This might mean duplicate tweet or suspended account")
            return None
        except Exception as e:
            print(f"⚠ Failed to post tweet: {e}")
            return None
    
    def post_thread(self, tweets: list) -> bool:
        """
        Post a thread of tweets
        
        Args:
            tweets: List of tweet texts
            
        Returns:
            True if all tweets posted successfully
        """
        if not tweets:
            return False
        
        last_tweet_id = None
        
        for i, tweet_text in enumerate(tweets):
            try:
                if last_tweet_id:
                    # Reply to previous tweet in thread
                    response = self.client.create_tweet(
                        text=tweet_text,
                        in_reply_to_tweet_id=last_tweet_id
                    )
                else:
                    # First tweet in thread
                    response = self.client.create_tweet(text=tweet_text)
                
                if response and response.data:
                    last_tweet_id = response.data['id']
                    print(f"✓ Thread tweet {i+1}/{len(tweets)} posted")
                else:
                    print(f"⚠ Thread tweet {i+1} may have failed")
                    return False
                    
            except Exception as e:
                print(f"⚠ Failed to post thread tweet {i+1}: {e}")
                return False
        
        return True


# Integration with the main broadcaster
def enhance_broadcaster():
    """
    Enhance the broadcast.py script to use actual Twitter posting
    """
    code = '''
# Add this to broadcast.py to enable actual Twitter posting:

from twitter_integration import TwitterPoster

class ErosionBroadcaster:
    def __init__(self):
        # ... existing init code ...
        self.twitter = TwitterPoster()
    
    def broadcast(self, dry_run=True):
        # ... existing broadcast code ...
        
        if not dry_run and self.twitter.connected:
            # Actually post the tweet
            tweet_id = self.twitter.post_tweet(tweet)
            if tweet_id:
                print(f"Successfully posted: https://twitter.com/i/web/status/{tweet_id}")
            else:
                print("Failed to post tweet")
'''
    return code


if __name__ == "__main__":
    # Test the Twitter connection
    poster = TwitterPoster()
    
    if poster.connected:
        print("\n✓ Twitter integration ready!")
        print("\nTo post a test tweet, uncomment the line below:")
        # poster.post_tweet("Testing the Digital Erosion Broadcaster 🌑 #DigitalErosion")
    else:
        print("\n⚠ Twitter API not configured")
        print("\nTo enable Twitter posting:")
        print("1. Get API credentials from https://developer.twitter.com")
        print("2. Add these secrets to your GitHub repository:")
        print("   - TWITTER_API_KEY")
        print("   - TWITTER_API_SECRET")  
        print("   - TWITTER_ACCESS_TOKEN")
        print("   - TWITTER_ACCESS_SECRET")