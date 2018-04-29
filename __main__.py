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
    c.update()
    c.update(w1)
    c.update([w1, w2])
    time.sleep(4)
    c.update(w1)
    c.update(age = 2)
    
