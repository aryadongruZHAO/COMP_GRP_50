import json
from OOP_models import User, Post

# This file converts between JSON and in-memory objects
# Note: active is based on Post.is_active; used to filter closed or full posts


def load_users_posts(path):
    # Read file → in a single pass create users and their posts
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    users, posts = [], []
    for u in data.get("preset_users", []):
        users.append(User.from_dict(u))
        pub = u.get("username", "")
        for pd in u.get("published_posts", []):
            posts.append(Post.from_dict(pd, publisher_username=pub))
    test = data.get("test_user")
    if test:
        users.append(User.from_dict(test))
    return users, posts


def save_data(path, users, posts):
    # Put current in-memory objects back to JSON (for persistence/debugging)
    payload = {
        "users": [u.to_dict() for u in users],
        "posts": [p.to_dict() for p in posts],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def query(users, posts, username=None, publisher=None, course=None, active=None):
    # A query helper; active compares to post.is_active
    ures = users
    pres = posts
    if username is not None:
        ures = [u for u in ures if u.username == username]
    if publisher is not None:
        pres = [p for p in pres if p.publisher_username == publisher]
    if course is not None:
        pres = [p for p in pres if p.course == course]
    if active is not None:
        pres = [p for p in pres if bool(p.is_active) == bool(active)]
    return {"users": ures, "posts": pres}
