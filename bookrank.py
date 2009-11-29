#!/usr/bin/env python

import os
import sys
import time
import simplejson as json
from ecs import ECS

def sales_rank(config, asin):
    ecs = ECS(config['access_key'],
              config['secret_key'],
              config['associate_tag'])

    doc = ecs.request({'Operation': 'ItemLookup',
                       'ItemId': asin,
                       'ResponseGroup': 'SalesRank'})
    
    rank = doc.getElementsByTagName('SalesRank')[0]
    return int(rank.childNodes[0].nodeValue)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "usage: bookrank.py CONFIG OUTPUT"
        sys.exit(1)

    config = json.loads(open(sys.argv[1]).read())
    
    if os.path.exists(sys.argv[2]):
        data = json.loads(open(sys.argv[2]).read())
    else:
        data = {}

    for book in config['books']:
        asin = book['asin']
        rank = sales_rank(config, asin)

        if asin not in data:
            data[asin] = {"name": book['name'],
                          "asin": asin,
                          "data": []}

        stamp = int(time.time()) / 86400 * 86400 * 1000

        if len(data[asin]['data']) == 0 or data[asin]['data'][-1][0] < stamp:
            data[asin]['data'].append([stamp, rank])

    open(sys.argv[2], 'w').write(json.dumps(data))
