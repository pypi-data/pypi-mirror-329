import requests

import getUrls

def getIconByUrl(url, output):
    faviconUrl = getUrls.getFaviconUrl(url)
    if output:
        Name = output
    else:
        Name = faviconUrl.split("/")[-1]

    r = requests.get(faviconUrl, allow_redirects=True)
    open(Name, 'wb').write(r.content)


def getIconByName(name, output):
    url = getUrls.getUrlByWebsearch(name)
    getIconByUrl(url, output)

