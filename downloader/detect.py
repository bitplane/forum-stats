#!/usr/bin/python
"""
"""
import sys

from lxml import etree
from lxml.html.soupparser import fromstring

def detect(doc):
    """Detect the software that generated the given HTML document"""

    tree = fromstring(doc)

    match = tree.xpath("//head/meta[@name='generator' and contains(@content,'vBulletin')]")
    if match:
        try:
            version = match[0].get("content").split()[1]
        except IndexError:
            version = "Unknown"
        return ("vBulletin", version)

    if tree.xpath("//head/meta[@name='copyright' and contains(@content,'phpBB')]"):
        return ('phpBB', 'Unknown')

    if tree.xpath("//script[contains(@src, 'vbulletin_global.js')]"):
        return ('vBulletin', 'Unknown')

    if tree.xpath("//script[contains(@src, 'ipb_forum.js')]") or \
       tree.xpath("//link[@rel='stylesheet' and contains(@href, 'ipb_common.css')]") or \
       tree.xpath("//p[@id='copyright']/a[@href='http://www.invisionpower.com/products/board/' and contains(@title,'Invision')]") or \
       tree.xpath("//*[contains(@class, 'ipsType_small')]"):
        return ('Invision', 'Unknown') # new invision




    match = tree.xpath("//a[@href='http://www.simplemachines.org/' and @title='Simple Machines Forum']")
    if match and len(match[0].text.split('SMF ')) > 1:
        return ('SMF', match[0].text.split('SMF ')[-1])

    if tree.xpath("//a[@href='http://www.simplemachines.org/about/smf/license.php' and @title='License']"):
        return ('SMF', 'Unknown')

    if tree.xpath("//span[@id='copyright']/*[@target='_blank' and contains(.,'MyBB')]"):
        return ('MyBB', 'Unknown')

    match = tree.xpath("//head/meta[@name='generator' and contains(@content, 'Web Wiz Forums')]")
    if match:
        try:
            version = match[0].get('content')[15:]
        except indexError:
            version = 'Unknown'
        return ('Web Wiz Forums', version)

    if tree.xpath("//span[@class='smText']"):
        return ('Web Wiz Forums', 'Unknown')

    if tree.xpath("//div[@id='copyright']/a[@href='http://xenforo.com']"):
        return ('XenForo', 'Unknown')

    if tree.xpath("//a[@class='forumlink']") and tree.xpath("//span[@class='gensmall']"):
        return ('phpBB', 'Unknown')

    print etree.tostring(tree)
    return ('Unknown', 'Unknown')

# If launched from the command line, use stdin
def main():
    doc = sys.stdin.read()
    print detect(doc)

if __name__ == "__main__":
    main()
