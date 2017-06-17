import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import os
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from settings import STORED_DATA_PATH, SITES
from decorators import to_json
from args_parser import ArgsParser



class Search(object):
    """
        Class Search: allow the user to search string inside the article body or title
    """
    def search(self, sub_str, search_key):
        """

        :param sub_str: possible sub string in the article
        :param search_key: define where to search (article body or title)
        :return: list of articles
        """
        findings = []
        re_obj = re.compile(sub_str)
        for article in self.articles:
            match = re_obj.findall(article[search_key])
            if len(match) > 0:
                findings.append(article)

        return findings


class FileDao(object):
    """
        Class FileDao: ability to access the file data (select and insert)
    """
    def __init__(self):
        """
            class Constructor, check if the output file exist and load the articles
        """
        if not os.path.isfile(STORED_DATA_PATH):
            os.mknod(STORED_DATA_PATH)
        self.articles = self.get_articles()


    @to_json
    def get_articles(self):
        """
        reads the articles file content and return a list of dictionaries (using to_json decorator)
        :return: list of articles
        """
        with open(STORED_DATA_PATH, 'r') as file_reader:
            return file_reader.read()

    def insert_article(self, article):
        """
        Insert article to the articles.txt file
        :param article: new article
        :return:
        """
        self.articles.append(article)
        with open(STORED_DATA_PATH, 'w') as file_pointer:
            json.dump(self.articles, file_pointer)


class Collector(Search, FileDao):

    def __init__(self):
        super(Search, self).__init__()
        super(FileDao, self).__init__()

    def make_request(self, url):
        """
        make simple HTTP request
        :param url: site address
        :return: http response
        """
        response = requests.get(url)
        if response.ok:
            return response

    def fetch_site_links(self, site):
        """
        fetch the site main links
        :param site: news site
        :return: list of links
        """
        response = self.make_request(site['url'])
        if response is not None:
            return self.match_pattern(response.content, site['links_pattern'])

    def match_pattern(self, data, pattern):
        """
        search links in the site main page using regular expression
        :param data: page source code
        :param pattern: regular expression pattern
        :return: list with the match result
        """
        re_obj = re.compile(pattern)
        return re_obj.findall(data)


    def collect_news(self, site):
        """
        Main function- collect site news.
        :param site: dictionary, news site data
        :return:
        """
        print 'Starting collect data for {0} ...'.format(site['url'])
        links = self.fetch_site_links(site)
        print str(len(links)) + ' links found'
        for link in links:
            article = dict(url=site['url'] + link)
            response = self.make_request(article['url'])
            soup = BeautifulSoup(response.content, 'html.parser')
            body_tags = soup.find_all(site['html_parse']['tag'], site['html_parse']['class'])
            article['title'] = soup.title.get_text().encode('utf-8')
            article['body'] = "\n".join([str(item.get_text().encode('utf-8')) for item in body_tags])
            article['listed_at'] = str(datetime.utcnow())
            if not self.article_exist(article):
                self.insert_article(article)

    def compare_str(self, str1, str2):
        """
        Simple string comparision
        :param str1:
        :param str2:
        :return: boolean value
        """
        return str1.encode('utf-8') == str2.encode('utf-8')

    def article_exist(self, article):
        """
        Check if the article already exist in the articles file
        :param article: dictionary, scanned article
        :return: boolean value
        """
        for item in self.articles:
            if self.compare_str(article['title'], item['title']) or self.compare_str(article['body'], item['body']):
                return True
        return False



def main():
    """
    Driver, parse the user input and run articles collection or search
    :return:
    """
    arg_parser = ArgsParser()
    collector_instance = Collector()
    args = arg_parser.get_args()
    if args.get('collect') is True:
        for site in SITES:
            collector_instance.collect_news(site)
    elif args.get('search') is not None:
        result = collector_instance.search(args['search'][0], 'body')
        if len(result) > 0:
            print '\nFound a match:\n'
        for i in range(0, len(result)):
            print "{0}. {1}".format(str(i + 1), result[i]['title'])

if __name__ == '__main__':
    main()