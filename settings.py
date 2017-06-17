import os

SITES = [
    {
        'url': 'http://cnn.com',
        'links_pattern': '"(/[0-9]+/[0-9]+/[0-9]+/[A-z]+/[A-z0-9\-]+/index.html)"',
        'html_parse': {'tag': 'div', 'class': 'zn-body__paragraph'}

    },
    {
        'url': 'http://foxnews.com',
        'links_pattern': '"(/[0-9]+/[0-9]+/[0-9]+/[A-z]+/[A-z0-9\-]+/index.html)"',
        'html_parse': {'tag': 'div', 'class': 'article-text'}
    }
]


STORED_DATA_DIR = os.getcwd()
STORED_DATA_FILE = 'articles.txt'
STORED_DATA_PATH = os.path.join(STORED_DATA_DIR, STORED_DATA_FILE)