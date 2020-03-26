"""
modified from https://static.arxiv.org/static/arxiv.marxdown/0.1/help/api/examples/python_arXiv_parsing_example.txt by @kelleyl
"""
import datetime
import sys
import urllib
import wget
import os
import feedparser
from pathlib import Path


def scrape_arxiv_cscl():
    # Opensearch metadata such as totalResults, startIndex, and itemsPerPage live in the opensearch namespace.
    # Some entry metadata lives in the arXiv namespace. This is a hack to expose both of these namespaces in feedparser v4.1
    feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

    texts = []

    # set some search parameters
    qterm = 'covid19+OR+coronavirus+OR+covid'  # all coronavirus papers
    start = 0
    total = sys.maxsize  # will be updated once the first request gets response with total_matched_doc_num information
    pagination = 2000

    # set some criteria to filter articles
    # date_begin = datetime.date(2010, 1, 1)
    # date_end = datetime.date(2018, 1, 1)

    # def date_filter(pub_date):
    #     return date_begin <= pub_date < date_end

    documents = 0

    print(f"Downloading arxiv abstracts to output_file")
    while start < total:
        q = f'http://export.arxiv.org/api/query?search_query={qterm}&start={start}&max_results={pagination}'
        response = urllib.request.urlopen(q).read()
        feed = feedparser.parse(response)

        # Run through each entry, and save url
        url_list = []
        for entry in feed.entries:
            url_list.append((entry["link"]))

        # update looping variables
        total = int(feed.feed.opensearch_totalresults)
        start = start + pagination

    print (len(url_list))
    return url_list


def download():
    url_list = scrape_arxiv_cscl()
    with open("url_list.txt", 'w') as ofile:
        ofile.write("\n".join(url_list))
    Path("pdfs").mkdir(exist_ok=True)
    for url in url_list:
        url = f"{url[:17]}pdf{url[20:]}.pdf"
        print (url)
        wget.download(url, f"pdfs/{url[21:]}")

if __name__ == "__main__":
   download()