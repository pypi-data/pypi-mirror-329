import validators
import requests
from bs4 import BeautifulSoup


def getRootUrl(url):
    slpitter = "/"
    splittedUrl = [e + slpitter for e in url.split(slpitter) if e]
    cleanedUrl = splittedUrl[:2]
    finalUrl = "/".join(cleanedUrl)

    if validators.url(finalUrl):
        return(finalUrl)
    else:
        print(f'getRootUrl - Error: Cleaned url: {finalUrl} is not valid.')

def getFaviconUrl(url):
    rootUrl = getRootUrl(url)
    faviconUrl = rootUrl + "favicon.ico"
    if validators.url(faviconUrl):
        return(faviconUrl)
    else:
        print(f'getFaviconUrl - Error: Favicon url: {faviconUrl} is not valid.')


def getUrlByWebsearch(query):
    print('getUrlByWebsearch - Scrapping url...')
    browser = 'https://duckduckgo.com/html/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
    }
    parameters = {
        'q': query
    }

    response = requests.get(browser, params=parameters, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        firstResult = soup.find('a', class_='result__a')

        if firstResult:
            url = firstResult['href']
            print(f'First link found: {url}')
            print('-  Done')
            return url
        else:
            return "getUrlByWebsearch: Link not found"
    else:
        return f"getUrlByWebsearch - Error: Request failed: {response.status_code}"

