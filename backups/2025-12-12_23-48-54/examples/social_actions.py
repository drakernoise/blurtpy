import getpass
from datetime import datetime, timedelta
from blurtpy import Blurt
from blurtpy.account import Account
from blurtpy.comment import Comment
from blurtpy.discussions import Query, Discussions_by_created
from blurtpy.wallet import Wallet

from blurtpy.nodelist import NodeList

# Configuration
USERNAME = "your_username"
nl = NodeList()
NODE = [n["url"] for n in nl]

# Initialize Blurt without hardcoded keys
# It will use the local wallet (blurtpy.sqlite)
b = Blurt(node=NODE)

# Unlock Wallet
if b.wallet.created():
    if b.wallet.locked():
        pwd = getpass.getpass(f"Enter wallet password to operate as {USERNAME}: ")
        try:
            b.wallet.unlock(pwd)
            print("Wallet unlocked.")
        except Exception as e:
            print(f"Error unlocking: {e}")
            exit()
else:
    print("No wallet found. Run 'examples/wallet_manager.py' first.")
    exit()

def comment_post(identifier, body, title=""):
    """Comments on an existing post."""
    print(f"Commenting on {identifier}...")
    try:
        c = Comment(identifier, blockchain_instance=b)
        c.reply(body, title=title, author=USERNAME)
        print("Comment published successfully.")
    except Exception as e:
        print(f"Error commenting: {e}")

def analyze_comments(identifier):
    """Counts comments and lists authors."""
    print(f"Analyzing comments of {identifier}...")
    try:
        c = Comment(identifier, blockchain_instance=b)
        replies = c.get_replies()
        print(f"Total direct comments: {len(replies)}")
        
        authors = set()
        for reply in replies:
            authors.add(reply['author'])
        
        print(f"Unique authors: {', '.join(authors)}")
        return replies
    except Exception as e:
        print(f"Error analyzing comments: {e}")
        return []

def vote_comments(replies, weight=100):
    """Votes on a list of comments."""
    print(f"Voting on {len(replies)} comments with weight {weight}%...")
    for reply in replies:
        try:
            print(f"Voting for {reply['author']}...")
            reply.vote(weight, account=USERNAME)
            print("Vote sent.")
        except Exception as e:
            print(f"Error voting for {reply['author']}: {e}")

def last_user_post(user):
    """Finds the last post of a user."""
    print(f"Searching last post of {user}...")
    try:
        acc = Account(user, blockchain_instance=b)
        # get_blog returns a list of blog entries
        blog = acc.get_blog(limit=1)
        if blog:
            last_post = blog[0]
            print(f"Last post: {last_post['title']} ({last_post['permlink']})")
            return last_post
        else:
            print("User has no posts.")
            return None
    except Exception as e:
        print(f"Error searching post: {e}")
        return None

def search_recent_posts(tag, hours=24):
    """Searches recent posts by tag."""
    print(f"Searching posts in tag '{tag}' from the last {hours} hours...")
    try:
        q = Query(limit=20, tag=tag)
        posts = Discussions_by_created(q, blockchain_instance=b)
        
        limit_date = datetime.utcnow() - timedelta(hours=hours)
        
        count = 0
        for post in posts:
            post_date = post['created'] # This should be a datetime object or string
            # Ensure date format if string
            if isinstance(post_date, str):
                post_date = datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S")
            
            if post_date > limit_date:
                print(f"- {post['created']}: {post['title']} by {post['author']}")
                count += 1
            else:
                # Since Discussions_by_created is ordered by date, we can stop if we pass the limit
                break
        print(f"Found {count} recent posts.")
    except Exception as e:
        print(f"Error in search: {e}")

if __name__ == "__main__":
    # USAGE EXAMPLES (Uncomment to test)
    
    # 1. Find last post of a user
    # post = last_user_post("tekraze")
    
    # 2. Comment on that post (BE CAREFUL! This publishes to the real blockchain)
    # if post:
    #    identifier = f"@{post['author']}/{post['permlink']}"
    #    comment_post(identifier, "Hello! This is a test comment from blurtpy.")
    
    # 3. Analyze comments
    # if post:
    #    identifier = f"@{post['author']}/{post['permlink']}"
    #    comments = analyze_comments(identifier)
       
    # 4. Vote comments (BE CAREFUL! This consumes Voting Power)
    #    vote_comments(comments, weight=10) # 10%
    
    # 5. Search recent posts
    search_recent_posts("blurt", hours=24)
