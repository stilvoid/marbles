"""
Marbles lambda function
"""

from bottle import SimpleTemplate
from markdown import markdown
import boto3
import json
import os
import re

POSTS_PER_PAGE = 5

with open("assets/template.html") as f:
    TEMPLATE = SimpleTemplate(f.read())

s3 = boto3.client("s3")

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
    posts = sorted(posts, key=lambda post: post["timestamp"], reverse=True)

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

def handler(event, context):
    print(json.dumps(event, indent=4))

    bucket = event["Records"][0]["s3"]["bucket"]["name"]

    paginator = s3.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=bucket):
        for obj in page["Contents"]:
            print(s3.get_object(Bucket=bucket, Key=obj["Key"]))

    paginator = s3.get_paginator("list_objects_v2")

    pages = [
        {
            "content": markdown(obj["Body"].read().decode("utf-8")),
            "timestamp": obj["Metadata"].get("Date", obj["LastModified"]),
        }
        for page in paginator.paginate(Bucket=bucket)
        for obj in [
            s3.get_object(Bucket=bucket, Key=row["Key"])
            for row in page["Contents"]
        ]
    ]

    site = generate_site(os.environ["SITE_NAME"], pages)

    # Copy assest
    with open("assets/style.css", "rb") as f:
        s3.put_object(
            Bucket=os.environ["OUT_BUCKET"],
            Key="assets/style.css",
            ContentType="text/css",
            ACL="public-read",
            Body=f,
        )

    # Put pages in place
    for name, contents in site.items():
        s3.put_object(
            Bucket=os.environ["OUT_BUCKET"],
            Key=name,
            ContentType="text/html",
            ContentDisposition="inline",
            ACL="public-read",
            Body=contents,
        )
