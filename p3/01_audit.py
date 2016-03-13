# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import xml.etree.cElementTree as ET
import re


OSMFILE = "chelyabinsk.osm"


expected_street_re = [
    "^(улица|переулок|шоссе|проезд|тракт|проспект|площадь|тупик|посёлок|район|садоводческое товарищество|станция)",
    "(улица|переулок|шоссе|проезд|тракт|проспект|площадь|тупик|посёлок|район|садоводческое товарищество|станция)$",
]

mapping_re = [
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
    ('^ул\. ?', 'улица '),
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


def audit_street_type(unexpected_types, street_name):
    """
    Collect all unexpected street types.
    :param unexpected_types: set
    :param street_name: string
    :return: None
    """
    street_name = street_name.strip()
    for pattern in expected_street_re:
        if re.search(pattern, street_name):
            return
    unexpected_types.add(street_name)


def is_street_name(elem):
    """
    Check if element contains address
    :param elem: Element
    :return: boolean
    """
    return elem.attrib['k'] == "addr:street"


def audit(osmfile):
    """
    Collect all unexpected stret types. Only process <node> and <way> tags in
    osm file.
    :param osmfile: string file name
    :return: None
    """
    osm_file = open(osmfile, "r")
    unexpected_street_types = set()
    for event, elem in ET.iterparse(osm_file, events=(b"start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(unexpected_street_types, tag.attrib['v'])

    return unexpected_street_types


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


def process():
    st_types = audit(OSMFILE)
    for unexpected_type in sorted(st_types):
        print "[{0}] => [{1}]".format(
                unexpected_type,
                update_street_name(unexpected_type, mapping_re))


if __name__ == '__main__':
    process()
