#-*- coding:utf-8 -*-

import whosearch
from nuaamongodb import NuaaMongodb
whoosh = whosearch.Whoosh()
con = '南航'
seadata = whoosh.search(con)
print('len=='+str(len(seadata)))
for data in seadata:
    print(data['title'])
    print(data['url'])
    pass
    #print(data)



