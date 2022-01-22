#!/usr/bin/env python3

import sys
from datetime import datetime
from xml.etree import ElementTree



dtfmt = "%Y%m%dT%H%M%SZ"
now = datetime.utcnow().strftime(dtfmt)

tree = ElementTree.parse(sys.argv[1])

print(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">
<en-export export-date="{now}" application="Evernote" version="Evernote Mac">""")

for mark in tree.iter("a"):
    url = mark.attrib['href']
    title = mark.text or url
    try:
        added = datetime.utcfromtimestamp(int(mark.attrib['time_added'])).strftime(dtfmt)
    except (TypeError, ValueError):
        added = now

    tags = mark.attrib['tags'].split(",")
    tags = "\n".join(f"<tag>{t}</tag>" for t in tags)

    print(f"""
    <note>
        <title>{title}</title>
        <content>
            <![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
            <en-note style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;">
                {title}
                <br/>
                <a href="{url}">{url}</a>
            </en-note>
            ]]>
        </content>
        <created>{added}</created>
        {tags}
        <note-attributes><source-url>{url}</source-url></note-attributes>
    </note>
    """)

print("</en-export>")
