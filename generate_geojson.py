#!./venv/bin/python

import json

from geojson import FeatureCollection, Feature, Point


LIST = ['spielplaetze_flensburg.json', 'spielplaetze_naturnahes_spielen_flensburg.json', 'spielplaetze_aktivitaetsflaeche_flensburg.json', 'spielplaetze_fitness_parcours_flensburg.json', 'spielplaetze_inklusiver_spielplatz_flensburg.json']


def get_data(file):
    with open(file, 'r', encoding='Windows-1252') as file:
        data = file.read()

        return data

    return None


def make_geojson(d):
    fc = []

    for o in d:
        if not o['coords'] or len(o['coords']) != 2:
            continue

        point = Point((float(o['coords'][0]), float(o['coords'][1])))

        properties = {
            'name': o['name'],
            'object': o['object'],
            'attributes': o['attributes'],
            'image_id': o['image_id'],
            'image': o['image']
        }

        fc.append(Feature(geometry=point, properties=properties))

    c = FeatureCollection(fc)

    with open('spielplaetze_flensburg.geojson', 'w') as f:
        json.dump(c, f, ensure_ascii=False, indent=4)


def main():
    objects = []

    for file in LIST:
        data = get_data(file)

        # replace special characters
        data = data.encode('Windows-1252').decode('unicode-escape')

        # parse the JSON data
        json_data = json.loads(data.replace('\n', ''))

        for entry in json_data:
            object = {
                'coords': [0, 0],
                'attributes': '',
                'image_id': '',
                'image': '',
                'object': ''
            }

            for index, value in enumerate(entry):
                if index == 0:
                    object['coords'][0] = value
                elif index == 1:
                    object['coords'][1] = value
                elif index == 6:
                    object['object'] = value
                elif index == 8:
                    if 'Name' in value:
                        object['name'] = value['Name']

                    if 'Beschreibung' in value:
                        attributes = value['Beschreibung'].split(',')
                        attributes = [attribute.replace(' ', '').replace('\n', '') for attribute in attributes]

                        object['attributes'] = attributes

                    if 'image' in value and value['image']:
                        object['image'] = f"https://www.tbz-flensburg.de{value['image']}"

                    if 'imgfid' in value:
                        object['image_id'] = value['imgfid']

            objects.append(object)

    make_geojson(objects)


if __name__ == '__main__':
    main()