# FROM TUTORIAL: https://codeburst.io/automated-web-scraping-with-python-and-celery-ac02a4a9ce51
# Web Scraping - scraper tester
import os
from celery import Celery
from datetime import datetime # for time stamps
import requests # pulling data
from bs4 import BeautifulSoup # xml parsing
import json # exporting to files
from celery.schedules import crontab # scheduler


app = Celery('tasks')
# scheduled task execution
app.conf.beat_schedule = {
    # executes every 1 minute
    'scraping-task-one-min': {
        'task': 'tasks.hackernews_rss',
        'schedule': crontab()
    }
}

# save function
@app.task
def save_function(article_list):
    with open('articles.txt'), 'w' as outfile:
        json.dump(article_list, outfile)



# scraping function
@app.task
def hackernews_rss():
    article_list = []
    try:
        # execute my request, parse the data using the XML 
        # parser in BS4
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features='xml')
        # select only the "items" I want from the data      
        articles = soup.findAll('item')
        # for each "item" I want, parse it into a list
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text
            # create an "article" object with the data
            # from each "item"
            article = {
                'title': title,
                'link': link,
                'published': published,
                'created_at': str(datetime.now()),
                'source': 'HackerNews RSS'
                }
            # append my "article_list" with each "article" object
            article_list.append(article)
        # after the loop, dump my saved objects into a .txt file
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)


def save_function(articles_list):
    # timestamp and filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = 'articles-{}.json'.format(timestamp)
    # creating our articles file with timestamp
    with open(filename, 'w').format(timestamp) as outfile:
        json.dump(articles_list, outfile)
