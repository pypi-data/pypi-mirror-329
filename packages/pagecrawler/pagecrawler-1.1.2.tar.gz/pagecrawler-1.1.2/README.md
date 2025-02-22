# PageCrawler

## How to use
### _request

- call the _request() function, it will first try a request with the request libary and then with selenium
- fill out these keywords: url: str, keyword: str, headers: dict = None, soup:bool=False, max_retry:int=2, wait:int=0
- Explanation:
	- url : request url
	- keyword: the keyword that should be in the website to know whether or not it got the right website, use '' to ignore
	- headers: request header in dicit form, use {} for no headers, leave empty for basic request header
	- soup : Whether or not returned as a soup object
	- max_retry: how often it reties the request (boath the normal and selenium) to get a response containing the keyword

### multi_request
- calls the _request in multiprocessing
- the first argument just uses a list of lists of these 3 arguments: [url, keyword, headers] (lenght of list determines how many request are done)
- new argument: process: int = 1, just determines how many processes are called at the same time
- the rest are just the same as _request, but apply to every request
