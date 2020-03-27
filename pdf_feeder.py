import sys
from urllib import request
import os

import feedparser


class DataFeeder(object):
    def feed(self):
        raise NotImplementedError


class LocalFeeder(DataFeeder):
    def __init__(self, root_path, file_ext):
        self.root = root_path
        self.ext = file_ext

    def feed(self):
        for r, ds, fs in os.walk(self.root):
            for f in fs:
                if f.endswith(f".{self.ext}"):
                    abs_fname = os.path.join(r, f)
                    yield open(abs_fname, 'rb')


class ArxivFeeder(DataFeeder):

    def __init__(self, keywords=None):
        if keywords is None:
            self.keywords = ['covid19', 'coronavirus', 'covid']
        else:
            self.keywords = keywords

    def query(self):
        feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
        feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

        qterm = '+OR+'.join(self.keywords)
        start = 0
        total = sys.maxsize  # will be updated once the first request gets response with total_matched_doc_num information
        pagination = 2000

        while start < total:
            q = f'http://export.arxiv.org/api/query?search_query={qterm}&start={start}&max_results={pagination}'
            response = request.urlopen(q).read()
            feed = feedparser.parse(response)

            # update looping variables
            total = int(feed.feed.opensearch_totalresults)
            start = start + pagination
            for entry in feed.entries:
                article_url = entry['link']
                yield f"{article_url[:17]}pdf{article_url[20:]}.pdf"
                # yield entry["link"]

    def feed(self):
        for url in self.query():
            fname, _ = request.urlretrieve(url)
            yield open(fname, 'rb')


