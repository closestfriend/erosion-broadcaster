#!/usr/bin/env python3
"""
Genesis Tweet: Manual introduction to the Digital Erosion artwork
This will be the only manually crafted tweet to set the stage
"""

from twitter_integration import TwitterPoster

def send_genesis_tweet():
    """Send the inaugural tweet introducing the artwork"""
    
    genesis_message = """Digital Erosion begins.

A self-modifying artwork that slowly corrupts its own source code, committing each mutation to git. 

I will witness and document this decay.

The program dreams of its own entropy.

#DigitalErosion #ConceptualArt #GenerativeArt"""

    print("Genesis Tweet:")
    print("=" * 50)
    print(genesis_message)
    print("=" * 50)
    print(f"Length: {len(genesis_message)} characters")
    
    # Confirm before posting
    response = input("\nPost this genesis tweet? (y/N): ")
    
    if response.lower() == 'y':
        poster = TwitterPoster()
        
        if poster.connected:
            tweet_id = poster.post_tweet(genesis_message)
            if tweet_id:
                print(f"\n✓ Genesis tweet posted successfully!")
                print(f"URL: https://twitter.com/i/web/status/{tweet_id}")
                return True
            else:
                print("\n⚠ Failed to post genesis tweet")
                return False
        else:
            print("\n⚠ Twitter API not connected")
            return False
    else:
        print("\nGenesis tweet cancelled")
        return False

if __name__ == "__main__":
    send_genesis_tweet()