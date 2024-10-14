#!./venv/bin/python

import re
import sys
import httpx
import traceback
import logging as log
import click
import json

from pathlib import Path
from lxml import html


# log uncaught exceptions
def log_exceptions(type, value, tb):
    for line in traceback.TracebackException(type, value, tb).format(chain=True):
        log.exception(line)

    log.exception(value)

    sys.__excepthook__(type, value, tb) # calls default excepthook


def request_content(url):
    r = httpx.get(url, timeout=2)

    if r.status_code != 200:
        return None

    return r.text


def parse_result(content, category):
    doc = html.document_fromstring(content)

    meta_rows = doc.xpath('//div[starts-with(@id, "box")]')
    meta_extracts = {}
    address_extracts = {}

    for row in meta_rows:
        row_id = row.get('id')
        row_meta = row.xpath('./div[@class="kdata_lh"]/br/following-sibling::text()')
        rows_address = row.xpath('./div[@class="kdata_c"]/text()')

        meta_info = ''
        address_info = []

        for row_addr in rows_address:
            address_info.append(row_addr.replace('\r\n', ', ').replace('\n', '').strip())

        if len(row_meta) >= 1:
            meta_info = row_meta[0].replace('\r\n', ', ').replace('\n', '').strip()

        meta_extracts[row_id] = meta_info
        address_extracts[row_id] = ', '.join(address_info)

    a = doc.xpath('//script')

    data = []

    for i in a:
        if re.search(r'geoData = \'\{".*', i.text_content()):
            m = re.findall(r"'(.*?)'", i.text_content())
            d = json.loads(m[0])

            for n in d['features']:
                if n['properties']['kat'] == category:
                    e = {
                        'type': f'cat{category}',
                        'place': n['properties']['name'],
                        'address': address_extracts[n['properties']['akz']],
                        'details': meta_extracts[n['properties']['akz']],
                        'coords': n['geometry']['coordinates']
                    }

                    data.append(e)

    return data


def write_result(data, dst):
    with open(Path(dst), 'w') as f:
        json.dump(data, f, ensure_ascii=False)


@click.command()
@click.option('--url', '-u', type=str, required=True, help='Set url you wish to download')
@click.option('--target', '-t', type=str, required=True, help='Set local target path where to save')
@click.option('--category', '-c', type=int, required=True, help='Set category you whish to extract')
@click.option('--verbose', '-v', is_flag=True, help='Print more verbose output')
@click.option('--debug', '-d', is_flag=True, help='Print detailed debug output')
def main(url, target, category, verbose, debug):
    if debug:
        log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)
    if verbose:
        log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)
        log.info(f'set logging level to verbose')
    else:
        log.basicConfig(format='%(levelname)s: %(message)s')

    recursion_limit = sys.getrecursionlimit()
    log.info(f'your system recursion limit: {recursion_limit}')


    content = request_content(url)
    data = parse_result(content, category)
    write_result(data, target)


if __name__ == '__main__':
    sys.excepthook = log_exceptions

    main()
