# ssg-py

Simple Static Site Builder that parses Markdown to HTML.

Requirements:
- parse text separated by a newline into `<div>` block node
- parse blocks as:
    - unordered lists
    - ordered lists
    - blockquote
    - code
    - headings
    - paragraphs
- parse inline markdown (one level deep) into:
    - code
    - emphasis
    - italics
    - links
    - images
    - text
- TODO: copy static files
- TODO: generate pages

## Running
- `./main.sh` to run the builder
- `./start.sh` to run the site
- `./test.sh` to run the tests
