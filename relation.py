"""
Basic idea is taking two groups of papers (domain and codomain),
and for each in domain find any references of papers in codomain.
"""

import pdf_feeder
import pdf_parser


def testload_domain():
    local_feeder = pdf_feeder.LocalFeeder('/data/dtriac/dtra-covid/Papers', 'pdf')
    domain = []
    for paper in local_feeder.feed():
        parsed = (pdf_parser.parse_pdf(paper))
        if parsed is not None:
            domain.append(parsed)
    return domain


def testload_codomain():
    local_feeder = pdf_feeder.LocalFeeder('./test', 'pdf')
    codomain = []
    for paper in local_feeder.feed():
        parsed = pdf_parser.parse_pdf(paper)
        if parsed is not None:
            codomain.append(parsed)
    return codomain


def load_domain():
    arxiv_feeder = pdf_feeder.ArxivFeeder()
    domain = []
    for paper in arxiv_feeder.feed():
        parsed = pdf_parser.parse_pdf(paper)
        if parsed is not None:
            domain.append(parsed)
    return domain


def load_codomain():
    local_feeder = pdf_feeder.LocalFeeder('/data/dtriac/dtriac-534/spv1-results', 'json')
    codomain = []
    for paper in local_feeder.feed():

        parsed = pdf_parser.parse_json(paper)
        if parsed is not None:
            codomain.append(parsed)
    return codomain


def find_citation(domain, codomain):
    citations = {}
    for new_paper in domain:
        for old_paper in codomain:
            if new_paper.cites(old_paper):
                cited = citations.get(str(new_paper), [])
                if str(old_paper) not in cited:
                    cited.append(str(old_paper))
                citations[str(new_paper)] = cited
                #  print(cited)
    #  print(citations)
    return citations


if __name__ == '__main__':
    import json
    dom = load_domain()
    print(f'done reading domain, {len(dom)} documents loaded')
    cod = load_codomain()
    print(f'done reading codomain, {len(cod)} documents loaded')
    print(json.dumps(find_citation(dom, cod), indent=2))
