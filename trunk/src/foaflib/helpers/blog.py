from urllib import urlopen
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup
from feedparser import parse

def get_latest_entries(foafprofile):
    entries = []
    if not foafprofile.get_weblogs():
        return None
    for blog in foafprofile.get_weblogs():
        u = urlopen(blog)
        blogpage = u.read()
        u.close()

        bs = BeautifulSoup(blogpage)
        feeds = bs.findAll("link",{"type":"application/rss+xml"})
        for feed in feeds:
            feed_url = urljoin(blog, feed["href"])
            try:
                entries.extend(parse(feed_url)["entries"])
                break
            except:
                PASS
    return entries
