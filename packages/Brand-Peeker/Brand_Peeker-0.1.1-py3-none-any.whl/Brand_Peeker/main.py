import requests

import getUrls

def getIconByUrl(url):
    faviconUrl = getUrls.getFaviconUrl(url)
    outputFileName = faviconUrl.split("/")[-1]

    r = requests.get(faviconUrl, allow_redirects=True)
    open(outputFileName, 'wb').write(r.content)


def getIconByName(name):
    url = getUrls.getUrlByWebsearch(name)
    getIconByUrl(url)

