#!/bin/bash

echo 'Downloading list of sites from The Open Directory,'
echo 'this may take a while. Keep an eye on dmoz.txt, it'
echo 'should have about 10,000 rows when complete.'

URL=http://rdf.dmoz.org/rdf/content.rdf.u8.gz

# strip quotes, replace &amp;, replace &quot;
PARSE='s/.*\"\(.*.*\)\".*/\1/;s/\&amp;/\&/g;s/\&quot;/\"/g'

# download     | extract | fast filter       | slow filter   | parse      > save
wget -qO- $URL | zcat    | grep ExternalPage | grep -i forum | sed $PARSE > dmoz.txt

if [ $? == 0 ]
then
    echo 'Sorting and removing duplicates...'
    mv dmoz.txt dmoz.tmp
    cat dmoz.tmp | sort | uniq > dmoz.txt
    rm dmoz.tmp
    echo 'All done!'
else
    echo 'Ugh, something went wrong :('
fi

