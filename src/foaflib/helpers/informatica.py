from foaflib.utils.activitystreamevent import ActivityStreamEvent

try:
    from feedparser import parse
    _CAN_DO_ = True
except ImportError:
    _CAN_DO_ = False

def get_latest(foafperson):
    entries = []
    for account in foafperson.accounts:
        if "informati.ca" in account.accountServiceHomepage:
            entries.extend(get_latest_by_account(account))
    return entries

def get_latest_by_account(account):
    if not _CAN_DO_:
        return []

    posts = []
    username = account.accountName
    url = "https://identi.ca/api/statuses/user_timeline/%s.atom" % username
    try:
        feedentries = parse(url)["entries"]
        for entry in feedentries:
            event = ActivityStreamEvent()
            event.type = "Informati.ca"
            event.detail = entry["title"]
            event.timestamp = entry["published_parsed"]
            posts.append(event)
    except:
        pass
    return posts
