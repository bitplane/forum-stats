#!/usr/bin/python
"""
"""
import sys
import elementtidy.TidyHTMLTreeBuilder as TB
from StringIO import StringIO

from lxml import etree

def detect(doc):
    """Detect the software that generated the given HTML document"""
    # Fix damaged HTML using TidyHTMLTreeBuilder
    tree = TB.parse(StringIO(doc))
    # Back to basic HTML from XHTML, 'cause it's easier to handle
    XHTML = "{http://www.w3.org/1999/xhtml}"
    for elem in tree.getiterator():
        if elem.tag.startswith(XHTML):
            elem.tag = elem.tag[len(XHTML):]

    # Now convert this into an element tree. Ugly hackery, but whatever.
    strHTML = StringIO()
    tree.write(strHTML)
    #print strHTML.getvalue()
    tree = etree.HTML(strHTML.getvalue())
    strHTML.close()

    match = tree.xpath("/html/head/meta[@name='generator' and contains(@content,'vBulletin')]")
    if match:
        try:
            version = match[0].get("content").split()[1]
        except IndexError:
            version = "Unknown"
        return ("vBulletin", version)

    if tree.xpath("/html/head/meta[@name='copyright' and contains(@content,'phpBB')]"):
        return ('phpBB', 'Unknown')

    if tree.xpath("//script[contains(@src, 'vbulletin_global.js')]"):
        return ('vBulletin', 'Unknown')

    if tree.xpath("//script[contains(@src, 'ipb_forum.js')]"):
        return ('IP.B', 'Unknown') # new invision

    match = tree.xpath("/html/head/meta[@name='generator' and contains(@content, 'Web Wiz Forums')]")
    if match:
        try:
            version = match[0].get('content')[15:]
        except indexError:
            version = 'Unknown'
        return ('Web Wiz Forums', version)

    if tree.xpath("//span[@class='smText']"):
        return ('Web Wiz Forums', 'Unknown')

    return ('Unknown', 'Unknown')

# If launched from the command line, use stdin
def main():
    doc = sys.stdin.read()
    print detect(doc)

if __name__ == "__main__":
    main()
