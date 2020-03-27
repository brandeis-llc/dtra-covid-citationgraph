import requests
import pdf_feeder
import json
from paper import Paper

SPV1_URL = 'http://localhost:8123/v1'


def run_spv1(pdf_fp):
    files = {'file': pdf_fp}
    r = requests.post(SPV1_URL, files=files, headers={'Content-type': 'application/pdf'})
    return pdf_fp.name, r.text


def parse_spv1_json(fname, json_str):
    metadata = json.loads(json_str)
    #  print(fname)
    #  print("-------------------------------------------")
    #  print(json.dumps(metadata, indent=2))
    #  print("-------------------------------------------")
    if not all(map(lambda x: x in metadata, ['title', 'authors', 'references'])):
        print(f"!!!! spv1 failed to parse {fname}")
    else:
        title = metadata['title']
        authors = [author['name'] for author in metadata['authors']]
        refereces = [Paper(title=citation['title'],
                           authors=citation['authors'],
                           refereces=[])
                     for citation in metadata['references']]
        return Paper(title, authors, refereces)


def parse_pdf(pdf_fp):
    fname, json = run_spv1(pdf_fp)
    return parse_spv1_json(fname, json)


if __name__ == '__main__':
    feeder = pdf_feeder.LocalPDFFeeder('./test')
    for pdf in feeder.feed():
        run_spv1(pdf)
