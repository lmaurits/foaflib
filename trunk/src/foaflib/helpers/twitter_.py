from foaflib.utils.activitystreamevent import ActivityStreamEvent

try:
    import twitter
    _CAN_DO_ = True
except ImportError:
    _CAN_DO_ = False

def get_latest(foafprofile):
    if not _CAN_DO_:
	return []

    results = []
    for account in foafprofile.accounts:
        if "twitter.com" in account.accountServiceHomepage:
            tweets = get_latest_tweets_by_account(account)
            results.extend(tweets)
    return results

def get_latest_by_account(account):
    if account.accountName:
        username = account.accountName
    elif account.accountProfilePage:
        username = account.accountProfilePage.split("/")[-1]
    elif account.accountServiceHomepage:
        username = account.accountServiceHomepage.split("/")[-1]
    else:
        return []

    api = twitter.Api()
    tweets = []
    for tweet in api.GetUserTimeline(username):
        event = ActivityStreamEvent()
        event.type = "Tweet"
        event.detail = tweet.text
        tweets.append(event)
    return tweets
