import requests
from bs4 import BeautifulSoup

def blogger_article_spider (url):
    post = {}
    post['config'] = {}

    # get source code
    source_code = requests.get(url)
    plain_text = source_code.text
    
    # get target tag and its contents
    soup = BeautifulSoup(plain_text, features="lxml")
    post['content'] = soup.find('div', {'class': 'post-body entry-content float-container'})
    post['config']['url'] = url
    post['config']['title'] = soup.find('title').string
    post['config']['author'] = soup.find('a', {'rel': 'author'}).span.string
    post['config']['published'] = soup.find('span', {'class': 'byline post-timestamp'}).a.time['datetime']
    post['config']['tag'] = []
    for tag in soup.find_all('a', {'rel': 'tag'}):
        post['config']['tag'].append(tag.string)

    # return prettify data string
    soup = BeautifulSoup(str(post['content']), features="lxml")
    post['content'] = str(soup.prettify()) 
    return post

def blogger_sitemap_spider (url):
    data = {}
    data['post'] = []
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="html.parser")
    for title in soup.find_all('loc'):
        if title != None:
            data['post'].append(title.string[30:])

    return data



