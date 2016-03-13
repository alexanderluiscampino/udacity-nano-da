# -*- coding: utf-8
from __future__ import unicode_literals

import re

print re.sub(r' ул\. ?', ' улица ', 'участок 72/ ул. Речная')
print re.sub(r'^ул\. ?', 'улица ', 'ул. Речная')
