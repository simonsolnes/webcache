# webcache
Cache webpages when you are testing your web scrapers.

## Putting it in your project
Add this to your project with:

`$ git submodule add https://github.com/simonsolnes/webcache webcache`

and

```python3
from webcache import WebCache
```

## Quick Intro


To download a webpage:
```python
with WebCache() as c:
	website = c.get('https://www.python.org')
```

## Methods

`get(url) -> webpage data (str)`  
Gets the webpage data from the web or local cache.

`insert(*urls (string)) -> None`  
Puts one or several urls in the directory, but the cache doesn't download it. Meant for cuncurrent downloads.

`fetch() -> pages that failed (list), number of pages fetched (int)`  
Will download all webpages that are not local.

`update_url(*urls (string)) ->` pages that failed `(list),` number of pages fetched `(int)`  
Will update the urls that is passed.

`update_all() -> pages that failed (list), number of pages fetched (int)`  
Will redownload all webpages that the cache knows about.

`update_old(age (int, seconds)) -> pages that failed (list), number of pages fetched (int)`  
Will update the urls that has an age older than the one specified.

`reset() -> None`  
Will delete all local data.


## Downloading concurrently; `insert` and `fetch`

```python
urls = [
	'https://www.python.org'
	'https://duckduckgo.com'
	'https://www.wikipedia.org'
]
with WebCache() as c:
	c.insert(*urls)
	c.fetch()
	website = c.get('https://www.python.org')
```

## Updating webpages

Update an url:
```python
with WebCache() as c:
	# one
	c.update_url('https://www.python.org')
	# or several
	c.update(*urls)
```

Update old urls:
```python
with WebCache() as c:
	c.update_old(60 * 60)
```

Update all urls:
```python
with WebCache() as c:
	c.update_all()
```

## Not get a DoS
To not overload a server, you can set an amount of time that you are willing to wait when the cache is downloading several webpages. The longer the wait, the longer the time between each request.

```python
with WebCache(60) as c:
	...
```

## Without context
It is possible to do:
```python
c = WebCache():
website = c.get('https://www.python.org')
```
But is not recommended when several webpages is needed, since the cache needs to load its directory for each time you create an instance.

The class is a singleton, so there is no need to worry about if there is something else is using the cache at the moment.

## Reset
Reset the whole cache:
```python
WebCache().reset()
```
