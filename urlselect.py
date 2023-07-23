from duckduckgo_search import DDGS
from itertools import islice
from web_scrapt import parser
import time

DUCKDUCKGO_MAX_ATTEMPTS = 3 

def web_search(query: str, browse: str = 'text', num_results: int = 20) -> str:
    search_results = []
    attempts = 0
    url_key = 'href'
    while attempts < DUCKDUCKGO_MAX_ATTEMPTS:
        if not query:
            return json.dumps(search_results)
        if browse == 'news':
            results = DDGS().news(query)
            url_key = 'url'
        else:
            results = DDGS().text(query)
        search_results = list(islice(results, num_results))
        if search_results:
            break
        time.sleep(1)
        attempts += 1
    result = content_count(search_results, url_key)  # <-- HERE IS THE ISSUE
    filtered = [i for i in result if i['size'] < 3001 and i['size'] > 2000]
    if len(filtered) == 0 and num_results < 100:
        num_results = num_results * 2
        time.sleep(1)
        filtered = web_search(query, browse, num_results)
    return filtered
    ##return search_results

def content_count(result, url_key: str = 'href'):
    lenght = len(result)
    for i in range(lenght):
        a, b = parser(result[i][url_key])
        result[i]['size'] = a
    return result

##def main():
##    web_search(topic: str)
##
##if __name__ = "__main__":
##    main()