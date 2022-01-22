#!/usr/bin/env python
# *-* encoding: utf-8 -*-
#
# (c) Copyright 2008 Osvaldo Santana <osantana@gmail.com>
# All Rights Reserved. Licenced under the BSD terms.
#
# convert.py - Convert a CSV file into a XML compatible with KeePass
#
# You can use this script to convert a CSV exported by Firefox Password Exporter[1]
# Extension into a XML for KeePass X[2] importation.
#
# Usage: ./convert.py input.csv > output.xml
#
# [1] https://addons.mozilla.org/en-US/firefox/addon/2848
# [2] http://www.keepassx.org/

import sys
import urlparse
import time
import csv

from xml.etree.ElementTree import Element, dump

try:
    input_fname = sys.argv[1]
except IndexError, e:
    print >>sys.stderr, "Usage: %s input.csv > output.xml" % (sys.argv[0])
    sys.exit(1)

try:    
    input = open(input_fname, "rU")
except OSError, e:
    print >>sys.stderr, "%s not found." % (input_fname)
    sys.exit(2)

reader = csv.reader(input, quoting=csv.QUOTE_ALL)
header = reader.next()[0:3]

database = Element("database")
group = Element("group")
title = Element("title")
title.text = u"Internet"
icon = Element("icon")
icon.text = u"1"

database.append(group)
group.append(title)
group.append(icon)

title_counter = {}
for record in reader:
    url, username, password = record[0:3]

    try:
        title = urlparse.urlparse(url)[1]
    except Exception, e:
        title = ""
    
    if not title.strip():
        title = "Imported Entry"
    title_counter[title] = title_counter.get(title, 0) + 1
    title = "%s #%s" % (title, title_counter[title])

    timestamp = time.strftime("%Y-%M-%dT%H:%M:%S")
    
    node_entry = Element("entry")
    
    node_title = Element("title");              node_title.text = title
    node_username = Element("username");        node_username.text = username
    node_password = Element("password");        node_password.text = password
    node_url = Element("url");                  node_url.text = url
    node_comment = Element("comment")
    node_icon = Element("icon");                node_icon.text = u"0"
    node_creation = Element("creation");        node_creation.text = timestamp
    node_lastaccess = Element("lastaccess");    node_lastaccess.text = timestamp
    node_lastmod = Element("lastmod");          node_lastmod.text = timestamp
    node_expires = Element("expires");          node_expires.text = u"Never"
    
    node_entry.append(node_title)
    node_entry.append(node_username)
    node_entry.append(node_password)
    node_entry.append(node_url)
    node_entry.append(node_comment)
    node_entry.append(node_icon)
    node_entry.append(node_creation)
    node_entry.append(node_lastaccess)
    node_entry.append(node_lastmod)
    node_entry.append(node_expires)
    
    group.append(node_entry)
    
dump(database)