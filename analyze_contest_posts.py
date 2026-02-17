from blurtpy import Blurt
from blurtpy.account import Account
from datetime import datetime, timedelta
import json

import re

def analyze_posts():
    # Connect to Blurt
    b = Blurt(node=["https://rpc.beblurt.com", "https://rpc.blurt.world"])
    
    account_name = "drakernoise"
    print(f"Fetching posts for @{account_name}...")
    
    acc = Account(account_name, blockchain_instance=b)
    
    # Get history (blog posts)
    # We'll fetch a batch and filter by date
    # Use naive UTC for simplicity as Blurt usually returns naive UTC or we can strip it
    stop_time = datetime.utcnow() - timedelta(days=14)
    print(f"Analyzing posts since {stop_time} (UTC)...")
    
    contest_posts = []
    
    # get_blog returns a generator of posts
    for post in acc.get_blog(limit=50): # Increased limit to ensure we cover 2 weeks
        post_time = post["created"]
        if isinstance(post_time, str):
            post_time = datetime.strptime(post_time, "%Y-%m-%dT%H:%M:%S")
        
        # Make post_time naive if it is aware (assume UTC)
        if post_time.tzinfo is not None:
            post_time = post_time.replace(tzinfo=None)
            
        if post_time < stop_time:
            break
            
        title = post["title"]
        if "Guess the number" in title:
            print(f"\n[FOUND] {title} ({post_time})")
            print(f"Permlink: {post['permlink']}")
            print("-" * 40)
            
            # Extract key info
            body = post["body"]
            
            # Try to find the "Exact number" if it's a result post
            if "The exact number was" in body:
                match = re.search(r"The exact number was `(\d+)`", body)
                if match:
                    print(f"  -> Winning Number: {match.group(1)}")
                
                winner_match = re.search(r"And the winner is (@\w+)", body)
                if winner_match:
                    print(f"  -> Winner: {winner_match.group(1)}")
            
            # Check for range
            range_match = re.search(r"Guess the number between: `(\d+ - \d+)`", body)
            if range_match:
                print(f"  -> Range: {range_match.group(1)}")
                
            contest_posts.append(post)

    print(f"\nFound {len(contest_posts)} contest posts in the last 2 weeks.")

if __name__ == "__main__":
    analyze_posts()
