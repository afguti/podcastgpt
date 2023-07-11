from duckduckgo_search import DDGS
from itertools import islice
from web_scrapt import parser

DUCKDUCKGO_MAX_ATTEMPTS = 3 

def web_search(query: str, num_results: int = 8) -> str:
    search_results = []
    attempts = 0
    while attempts < DUCKDUCKGO_MAX_ATTEMPTS:
        if not query:
            return json.dumps(search_results)
        results = DDGS().text(query)
        search_results = list(islice(results, num_results))
        if search_results:
            break
        time.sleep(1)
        attempts += 1
    result = content_count(search_results)
    return result
    ##return search_results

def content_count(result):
    lenght = len(result)
    for i in range(lenght):
        a, b = parser(result[i]['href'])
        result[i]['size'] = a
    return result

##def main():
##    web_search(topic: str)
##
##if __name__ = "__main__":
##    main()