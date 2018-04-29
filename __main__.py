from __init__ import WebCache
import time

with WebCache() as c:
    c.reset()

w1 = 'https://www.python.org'
w2 = 'https://duckduckgo.com'
w3 = 'https://www.wikipedia.org'

with WebCache() as c:
    print(c.get(w1).split('\n')[12])

with WebCache() as c:
    
    c.insert(w2)
    assert(c.fetch()[1] == 1)
    assert(c.update_url(w1, w2)[1] == 2)
    time.sleep(4)
    assert(c.update_url(w1)[1] == 1)
    assert(c.update_old(2)[1] == 1)
    
