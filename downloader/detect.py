#!/usr/bin/python
"""
"""
import sys

from lxml import etree
from lxml.html.soupparser import fromstring

def detect(doc):
    """Detect the software that generated the given HTML document"""
    try:
        tree = fromstring(doc)
    except:
        return ('Error', 'Error')

    match = tree.xpath("//head/meta[@name='generator' and contains(@content,'vBulletin')]")
    if match:
        try:
            version = match[0].get("content").split()[1]
        except IndexError:
            version = "Unknown"
        return ("vBulletin", version)

    if tree.xpath("//body[@id='phpBB']"):
        return ('phpBB', 'Unknown')

    if tree.xpath("//td[@class='rowpic']") and \
       tree.xpath("//td[@class='gensmall']") and \
       tree.xpath("//a[contains(@href, 'index.php?c=')]") and \
       tree.xpath("//a[contains(@href, 'viewforum.php?')]"):
        return ('phpBB', 'Unknown')

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

    if tree.xpath("//a[contains(@href, 'gforum.cgi?do')]"):
        return ('Gossamer Forum', 'Unknown')

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

    if tree.xpath("//p[@class='copyright']/a[@href='http://www.woltlab.com']/strong"):
        return ('Burning Board', 'Unknown')

    if tree.xpath("//div[@class='yafactiveusers']"):
        return ('YAF', 'Unknown')

    match = tree.xpath("//head/meta[@name='generator' and contains(@content,'BMForum')]")
    if match:
        try:
            version = match[0].get("content").split("BMForum ")[1]
        except IndexError:
            version = "Unknown"
        return ("BMForum", version)


    if "Powered by: vBulletin" in doc:
        return ('vBulletin', 'Unknown')

    if 'Powered by <a href="http://www.invisionboard.com"' in doc:
        return ('Invision', '1.x')

    if 'Powered by <a href="http://www.infopop.com">Infopop Corporation</a><br />Ultimate Bulletin Board' in doc:
        return ('UBB', 'Unknown')

    #print etree.tostring(tree)
    return ('Unknown', 'Unknown')

# If launched from the command line, use stdin
def main():
    doc = sys.stdin.read()
    print detect(doc)

if __name__ == "__main__":
    main()
