from bs4 import BeautifulSoup
import requests

def attempts_scraper(url):
    resp = requests.get(url)
    resp = resp.text
    soup = BeautifulSoup(resp)
    headers_tagged = soup.findAll('th')
    headers_untagged = [item.text for item in headers_tagged]
    headers = [item.lower().strip() for item in headers_untagged]
    contents_tagged = soup.findAll('td')
    contents_runon = [item.text for item in contents_tagged]

    def divide_chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    contents_unstripped = list(divide_chunks(contents_runon, 3))
    contents = [ [element.strip() for element in item] for item in contents_unstripped]
    return contents
