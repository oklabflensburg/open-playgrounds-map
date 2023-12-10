#!./venv/bin/python

import json
import click

from geojson import FeatureCollection, Feature, Point
from pathlib import Path


def get_data(src):
    with open(Path(src), 'r') as f:
        d = json.loads(f.read())
    
    return d


@click.command()
@click.argument('src')
@click.argument('dst')
def main(src, dst):
    d = get_data(src)
    fc = []

    crs = {
        'type': 'name',
        'properties': {
            'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
        }
    }

    for o in d:
        if not o['coords'] or len(o['coords']) != 2:
            continue

        point = Point((float(o['coords'][0]), float(o['coords'][1])))
            
        properties = {
            'place': o['place'],
            'attributes': o['attributes'],
            'image': o['image']
        }

        fc.append(Feature(geometry=point, properties=properties))

    c = FeatureCollection(fc, crs=crs)

    with open(Path(dst), 'w') as f:
        json.dump(c, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
