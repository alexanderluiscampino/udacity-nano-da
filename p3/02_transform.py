#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import xml.etree.cElementTree as ET
import re
import codecs
import json
"""
We are transforming the shape of the data here.
The output is a list of dictionaries that look like this:

{
    "id": "2406124091",
    "type: "node",
    "visible":"true",
    "created": {
              "version":"2",
              "changeset":"17206049",
              "timestamp":"2013-08-03T16:43:42Z",
              "user":"linuxUser16",
              "uid":"1219059"
            },
    "pos": [41.9757030, -87.6921867],
    "address": {
              "housenumber": "5157",
              "postcode": "60625",
              "street": "North Lincoln Ave"
            },
    "amenity": "restaurant",
    "cuisine": "mexican",
    "name": "La Cabana De Don Luis",
    "phone": "1 (773)-271-5176"
}

How the data is processed:

- only 2 types of top level tags: "node" and "way" are processed
- all attributes of "node" and "way" are turned into regular key/value pairs, except:
    - attributes in the CREATED array are added under a key "created"
    - attributes for latitude and longitude are added to a "pos" array,
      for use in geospacial indexing. Values inside "pos" array are floats
      and not strings.
- if second level tag "k" value contains problematic characters, it is ignored
- if second level tag "k" value starts with "addr:", it is added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", we process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag is ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  is turned into:

{...
    "address": {
        "housenumber": 5158,
        "street": "North Lincoln Avenue"
    }
    "amenity": "pharmacy",
    ...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

is turned into
    "node_refs": ["305896090", "1719825889"]
"""


CREATED = ["version", "changeset", "timestamp", "user", "uid"]

STREET_RE = [
    "^(улица|переулок|шоссе|проезд|тракт|проспект|площадь|тупик|посёлок|район|садоводческое товарищество|станция)",
    "(улица|переулок|шоссе|проезд|тракт|проспект|площадь|тупик|посёлок|район|садоводческое товарищество|станция)$",
]

MAP_STREET_RE = [
    ('\.', '. '),
    ('\\/', ' / '),
    ('\s+', ' '),
    ('«', '"'),
    ('»', '"'),
    ('(сдт|снт|СНТ)\.? ?', 'садоводческое товарищество '),
    (' ул\. ?', ' улица '),
    ('^ул\. ?', 'улица '),
    (' (уч\.|уч-к) ?', ' участок '),
    ('^(уч\.|уч-к) ?', 'участок '),
    (' п\. ?', ' поселок '),
    ('^п\. ?', 'поселок '),
    (' с\. ?', ' село '),
    ('^с\. ?', 'село '),
    (' обл\. ?', ' область '),
    ('^обл\. ?', 'область '),
    ('^д\. ?', 'деревня '),
    (' ж\.[ \-]*?д.? ?', ' ж/д '),
    ('^ж\.[ \-]*?д.? ?', 'ж/д '),
    ('№ ?', '')
]


def is_address(tag_key):
    return tag_key.startswith('addr:')


def is_address_street(tag_key):
    return tag_key == 'addr:street'


def is_address_detail(tag_key):
    return is_address(tag_key) and len(tag_key.split(':')) == 3


def has_colon(tag_key):
    return ':' in tag_key


def is_street_good(street_name, expected):
    for pattern in expected:
        if re.search(pattern, street_name):
            return True
    return False


def update_street_name(name, mapping):
    """
    Change street name according to standard rules in mapping dict
    :param name: string street name
    :param mapping: list
    :return: string
    """
    for bad, good in mapping:
        name = re.sub(bad, good, name)
    name = name.strip()
    return name


def add_tag_info(node, tag_key, tag_val):
    """
    Add tag key and value, special treatment for addresses
    :param node:
    :param tag_key:
    :param tag_val:
    :return:
    """
    if is_address(tag_key):
        address_part = tag_key.split(':')[1]
        if 'address' not in node:
            node['address'] = {}
        if is_address_street(tag_key) and not is_street_good(tag_val, STREET_RE):
            tag_val = update_street_name(tag_val, MAP_STREET_RE)
        node['address'][address_part] = tag_val
    elif has_colon(tag_key):
        pass
    elif tag_key == 'type':
        # We already have "type", it's either "node" or "way".
        # Let's rename "type" to "type_tag" so we don't confuse the two.
        node["type_tag"] = tag_val
    else:
        node[tag_key] = tag_val
    return node


def add_attr_info(node, attr_key, attr_val):
    """
    Reshape node
    :param node:
    :param attr_key:
    :param attr_val:
    :return:
    """
    if attr_key == 'lat':
        node['pos'] = [float(attr_val)] + node.get('pos', [])
    elif attr_key == 'lon':
        node['pos'] = node.get('pos', []) + [float(attr_val)]
    elif attr_key in CREATED:
        created = node.get('created', {})
        created[attr_key] = attr_val
        node['created'] = created
    else:
        node[attr_key] = attr_val
    return node


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        node['type'] = element.tag
        for k, v in element.items():
            node = add_attr_info(node, k, v)
        for tag in element.iter("tag"):
            node = add_tag_info(node, tag.attrib['k'], tag.attrib['v'])
        for nd in element.iter('nd'):
            if 'node_refs' not in node:
                node['node_refs'] = []
            node['node_refs'] += [nd.attrib['ref']]
        return node
    else:
        return None


def process_map(file_in, pretty=False):
    """
    Process and rewrite OSM file data to structured JSON
    :param file_in: string
    :param pretty: boolean
    """
    file_out = "{0}.json".format(file_in)
    with codecs.open(file_out, "w", encoding='utf-8') as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                if pretty:
                    json.dump(el, fo, ensure_ascii=False, indent=2)
                    fo.write("\n")
                else:
                    json.dump(el, fo, ensure_ascii=False)
                    fo.write("\n")


def process():
    process_map('chelyabinsk.osm', False)


if __name__ == "__main__":
    process()
