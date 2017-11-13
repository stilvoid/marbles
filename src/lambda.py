"""
Marbles lambda function
"""

from bottle import SimpleTemplate

POSTS_PER_PAGE = 5

with open("assets/template.html") as f:
    TEMPLATE = SimpleTemplate(f.read())

def generate_page(site_title, posts, prev_page=None, next_page=None):
    return TEMPLATE.render(
        site_title=site_title,
        posts=posts,
        prev_page=prev_page,
        next_page=next_page,
    )

def page_name(i, num_pages):
    if i < 0 or i >= num_pages:
        return None

    if i == 0:
        return "index.html"

    return "index{}.html".format(i + 1)

def generate_site(site_title, posts):
    posts = sorted(posts, key=lambda post: post["timestamp"])

    pages = [
        posts[i:i+POSTS_PER_PAGE]
        for i
        in range(0, len(posts), POSTS_PER_PAGE)
    ]

    site = {}

    num_pages = len(pages)

    for i, page_posts in enumerate(pages):
        site[page_name(i, num_pages)] = generate_page(
            site_title,
            page_posts,
            prev_page=page_name(i - 1, num_pages),
            next_page=page_name(i + 1, num_pages),
        )

    return site

if __name__ == "__main__":
    posts = [
        {
            "title": "Post number {}".format(i),
            "content": "Here is some content for post number {}. ".format(i) * 10,
            "timestamp": 1234567890 + i,
        }
        for i in range(99)
    ]

    site = generate_site("Magic page", posts)

    for name, page in site.items():
        with open("build/{}".format(name), "w") as f:
            f.write(page)
