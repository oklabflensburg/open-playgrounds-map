#!./venv/bin/python

import re
import json
import click
import httpx

from pathlib import Path


def extract_image(obj):
    if not 'image' in obj:
        return ''

    base = 'https://www.tbz-flensburg.de'
    path = obj['image']
    url = f'{base}{path}'

    return url


def request_content(url):
    r = httpx.get(url, timeout=2)

    if r.status_code != 200:
        return None

    return r.text


def generate_request(content):
    kat_url = re.search(r'url: "(.*)"', content, re.MULTILINE)
    poi_id = re.search(r'poiTpID\' : \'(.*)\'', content, re.MULTILINE)
    mod_ids = re.search(r'baseMods\': \[(.*)\]', content, re.MULTILINE)

    poi = poi_id.group(1)
    mod = mod_ids.group(1)

    url = f'https://www.tbz-flensburg.de/output/get_content.php?id={poi}&max=1000&data=1&type=json&i_mods={mod}&i_sub=0&kat=2693.65.1'
    result = request_content(url)

    return result


def parse_result(result):
    c = json.loads(result)
    d = []

    for i in c:
        if not len(i) > 0:
            continue

        place = i[8]['Name'].strip()
        attributes = [u.strip() for u in i[8]['Beschreibung'].split(',')]
        image = extract_image(i[8])

        properties = {
            'place': place,
            'attributes': attributes,
            'coords': [float(i[1]), float(i[0])],
            'image': image
        }

        d.append(properties)

    return d


def write_result(data, dst):
    with open(Path(dst), 'w') as f:
        json.dump(data, f, ensure_ascii=False)


@click.command()
@click.argument('dst')
def main(dst):
    url = 'https://www.tbz-flensburg.de/%C3%96ffentliches-Gr%C3%BCn/Spielfl%C3%A4chen/'
    content = request_content(url)
    result = generate_request(content)
    data = parse_result(result)
    write_result(data, dst)


if __name__ == '__main__':
    main()
