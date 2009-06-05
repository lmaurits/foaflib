from feedparser import parse

def get_latest_posts(foafperson):
    entries = []
    for account in foafperson.accounts:
        if "informati.ca" in account["accountServiceHomepage"]:
            username = account["accountName"]
            url = "https://identi.ca/api/statuses/user_timeline/%s.atom" % username
            try:
                entries.extend(parse(url)["entries"])
            except:
                pass
    return entries
