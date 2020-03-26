"""
modified from https://static.arxiv.org/static/arxiv.marxdown/0.1/help/api/examples/python_arXiv_parsing_example.txt by @kelleyl
"""
import datetime
import sys
import urllib

import feedparser

from util import path


def scrape_arxiv_cscl():
    # Opensearch metadata such as totalResults, startIndex, and itemsPerPage live in the opensearch namespase.
    # Some entry metadata lives in the arXiv namespace. This is a hack to expose both of these namespaces in feedparser v4.1
    feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

    texts = []

    # set some search parameters
    qterm = 'cat:cs.CL'  # all `cs.CL` papersj
    start = 0
    total = sys.maxsize  # will be updated once the first request gets response with total_matched_doc_num information
    pagination = 2000

    # set some criteria to filter articles 
    date_begin = datetime.date(2010, 1, 1)
    date_end = datetime.date(2018, 1, 1)

    def date_filter(pub_date):
        return date_begin <= pub_date < date_end

    documents = 0

    print(f"Downloading arxiv abstracts (cs.CL, {date_begin} - {date_end}) to {path.ARXIV_DATA}")
    while start < total:

        q = f'http://export.arxiv.org/api/query?search_query={qterm}&start={start}&max_results={pagination}'
        response = urllib.request.urlopen(q).read()
        feed = feedparser.parse(response)

        # Run through each entry, and print out information
        for entry in feed.entries:
            publication_date = datetime.date.fromisoformat(entry.published.split('T')[0])
            if date_filter(publication_date):
                if "abstract" in entry:
                    texts.append(entry.abstract)
                    documents += 1
                elif "summary" in entry:
                    texts.append(entry.summary)
                    documents += 1
                else:
                    pass
                    #  sys.stderr.write("NO ABSTRACT FOR {}\n".format(entry.title))

        # update looping variables
        total = int(feed.feed.opensearch_totalresults)
        start = start + pagination
        #  sys.stderr.write(f"{documents} documents found between 0 - {start} out of {total} {qterm} results\n")
        print(".", end="")
    print("")
    return "\n".join(texts)


def download():
    with open(path.ARXIV_DATA, 'w') as ofile:
        ofile.write(scrape_arxiv_cscl())


if __name__ == "__main__":
    scrape_arxiv_cscl()
