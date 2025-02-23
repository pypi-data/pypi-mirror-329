import random
from datetime import datetime, timedelta



def post_reply(comment_id, reply):
    print(f"POSTED: {reply}")
    return True






#helper methods
def get_latest_youtube_comments(channel_id, num_comments):
    # List of mock author names
    author_names = ["User1", "Commenter2", "Viewer3", "Fan4", "Subscriber5"]
    
    # List of mock comment texts
    comment_texts = [
        "Great video!",
        "I learned a lot from this.",
        "Can you make more content like this?",
        "Interesting perspective.",
        "Thanks for sharing!",
        "I disagree with point X, but overall good video.",
        "Looking forward to your next upload!",
        "This helped me understand the topic better.",
        "Could you elaborate on minute 3:45?",
        "Your channel is awesome!"
    ]
    
    # Generate mock comments
    comments = []
    for i in range(num_comments):
        comment = {
            "comment_id": f"comment_{channel_id}_{i}",
            "comment_text": random.choice(comment_texts),
            "publish_date": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            "author_name": random.choice(author_names)
        }
        comments.append(comment)
    
    # Sort comments by publish_date (most recent first)
    comments.sort(key=lambda x: x["publish_date"], reverse=True)
    
    return comments