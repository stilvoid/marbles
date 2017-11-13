# Marbles

A Markdown Blogging Engine - Serverless.

Marbles generates an S3 website from markdown files uploaded to an input bucket. The website will show 5 posts per page and automatically have links to next/previous pages. This allows you to host a very simple blog simply by uploading a markdown file to S3 whenever you've finished writing a post.

You can modify the look of the blog by editing `assets/template.html` and `assets/style.css`. The template file uses [SimpleTemplate](https://bottlepy.org/docs/dev/stpl.html) from [Bottle](https://bottlepy.org/).

## Installing

You can install Marbles into your account by running the `./install.sh` script. This will create an input bucket and an S3 website, upload a sample file, and then output the relevant details for uploading your first blog post.
