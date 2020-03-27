"""
Basic idea is taking two groups of papers (domain and codomain),
and for each in domain find any references of papers in codomain.
"""

import pdf_feeder
import pdf_parser


def load_domain():
    arxiv_feeder = pdf_feeder.ArxivFeeder()
    domain = []
    for paper in arxiv_feeder.feed():
        domain.append(pdf_parser.parse_pdf(paper))
    return domain


def load_codomain():
    local_feeder = pdf_feeder.LocalPDFFeeder('/data/dtriac/dtriac-534')
    codomain = []
    for paper in local_feeder.feed():
        codomain.append(pdf_parser.parse_pdf(paper))
    return codomain


def find_citation(domain, codomain):
    citations = {}
    for new_paper in domain:
        for old_paper in codomain:
            if new_paper.cites(old_paper):
                cited = citations.get(str(new_paper), set())
                cited.add(str(old_paper))
                citations[str(new_paper)] = cited
    return citations


if __name__ == '__main__':
    import json
    dom = load_domain()
    cod = load_codomain()
    print(json.dumps(find_citation(dom, cod)))
