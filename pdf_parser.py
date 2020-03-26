import requests
import pdf_feeder

SPV1_URL = 'http://localhost:8123/v1'


def run_spv1(pdf_fp):
    files = {'file': pdf_fp}
    r = requests.post(SPV1_URL, files=files, headers={'Content-type': 'application/pdf'})
    print(r.text)


if __name__ == '__main__':
    feeder = pdf_feeder.LocalPDFFeeder('./test')
    for pdf in feeder.feed():
        run_spv1(pdf)
