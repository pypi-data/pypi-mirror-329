from types import MappingProxyType

list_headers = dict()
def header(proxy_header):
    list_headers[proxy_header.__name__] = proxy_header()

@header
def no_header()-> dict:
    return {}

@header
def bascic_header() -> dict:
    return dict(
    {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    'Accept-Language' : 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control' : 'max-age=0',
    'Sec-Ch-Ua' : '"Not_A Brand";v="8", "Chromium";v="120", "Opera GX";v="106"',
    'Sec-Ch-Ua-Mobile' : '?0',
    'Sec-Ch-Ua-Platform' : '"Windows"',
    'Sec-Fetch-Dest ' : 'document',
    'Sec-Fetch-Mode' : 'navigate',
    'Sec-Fetch-Site' : 'none',
    'Sec-Fetch-User' : '?1',
    'Upgrade-Insecure-Requests' : '1',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0'
    }
)

class database():

    def __int__(self):
        self.db = {

        }

    def add(self, **kwargs):
        for x in kwargs:
            self.db[x] = kwargs[x]

class headers_generator():

    def __init__(self, db=None):
        if db is None:
            self.db = database
        else:
            self.db = db
        self.count = 0

    def next(self, url):
        if url in self.db.db.values():
            return self.db.db[url]
        else:
            if self.count == len(list_headers):
                self.count = 0
            self.count += 1
            return list_headers[self.count-1]

