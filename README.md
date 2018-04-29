# webcache
Cache webpages when you are testing your web scrapers.

Add this to your project with :

`$ git submodule add https://github.com/simonsolnes/webcache webcache`

and

```python3
from webcache import WebCache
```

To download a webpage:
```python
with WebCache as c:
	website = c.get('https://www.python.org')
```

If you want to download several pages concurrently:
```python
urls = [
	'https://www.python.org'
	'https://duckduckgo.com'
	'https://www.wikipedia.org'
]
with WebCache as c:
	for url in urls:
		c.insert(url)
	c.update()
	website = c.get('https://www.python.org')
```

## Methods

```
get(url) -> webpage data (str)
insert(url) -> None
update(url?, age?, use_time?) -> pages that failed (list)
reset() -> None
```

## Updating and inserting

Update one url:
```python
with WebCache as c:
	c.update('https://www.python.org')
```

Update several urls:
```python
with WebCache as c:
	c.update(urls)
```

To not overload a server, you can set an amount of time that you are willing to wait for the update (in seconds):
```python
with WebCache as c:
	c.update(use_time = 60)
```

Only update urls that are old
```python
with WebCache as c:
	c.update(age = 60 * 60)
```

## Reset

Reset the whole cache:
```python
with WebCache as c:
	c.reset()
```

## Without context
It is possible to do:
```python
c = WebCache:
website = c.get('https://www.python.org')
```
But is not recommended with several webpages
