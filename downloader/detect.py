#!/usr/bin/python
"""
"""
import sys

from lxml import etree
from lxml.html.soupparser import fromstring

def detect(doc):
    """Detect the software that generated the given HTML document"""

    tree = fromstring(doc)

    match = tree.xpath("./head/meta[@name='generator' and contains(@content,'vBulletin')]")
    if match:
        try:
            version = match[0].get("content").split()[1]
        except IndexError:
            version = "Unknown"
        return ("vBulletin", version)

    if tree.xpath("./head/meta[@name='copyright' and contains(@content,'phpBB')]"):
        return ('phpBB', 'Unknown')

    if tree.xpath("//script[contains(@src, 'vbulletin_global.js')]"):
        return ('vBulletin', 'Unknown')

    if tree.xpath("//script[contains(@src, 'ipb_forum.js')]"):
        return ('IP.B', 'Unknown') # new invision

    match = tree.xpath("./head/meta[@name='generator' and contains(@content, 'Web Wiz Forums')]")
    if match:
        try:
            version = match[0].get('content')[15:]
        except indexError:
            version = 'Unknown'
        return ('Web Wiz Forums', version)

    if tree.xpath("//span[@class='smText']"):
        return ('Web Wiz Forums', 'Unknown')

    if tree.xpath("//a[@class='forumlink']") and tree.xpath("//span[@class='gensmall']"):
        return ('phpBB', 'Unknown')

    return ('Unknown', 'Unknown')

# If launched from the command line, use stdin
def main():
    doc = sys.stdin.read()
    print detect(doc)

if __name__ == "__main__":
    main()
