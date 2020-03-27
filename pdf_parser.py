import requests
import pdf_feeder
import json
from paper import Paper

SPV1_URL = 'http://localhost:8123/v1'


def run_spv1(pdf_fp):
    files = {'file': pdf_fp}
    r = requests.post(SPV1_URL, files=files, headers={'Content-type': 'application/pdf'})
    return r.text


def parse_spv1_json(json_str):
    metadata = json.loads(json_str)
    title = metadata['title']
    authors = [author['name'] for author in metadata['authors']]
    refereces = [Paper(title=citation['title'],
                       authors=citation['authors'],
                       refereces=[])
                 for citation in metadata['refereces']]
    Paper(title, authors, refereces)


def parse_pdf(pdf_fp):
    return parse_spv1_json(run_spv1(pdf_fp))


if __name__ == '__main__':
    feeder = pdf_feeder.LocalPDFFeeder('./test')
    for pdf in feeder.feed():
        run_spv1(pdf)
