import twitter

def get_latest_tweets(foafprofile):
    for account in foafprofile.get_accounts():
        # Get rid of this after there are no None accounts
        if not account:
            continue
        if "twitter.com" in account["accountServiceHomepage"]:
            if "accountName" in account:
                username = account["accountName"]
            elif "accountProfilePage" in account:
                username = account["accountProfilePage"].split("/")[-1]
            elif "accountServiceHomepage" in account:
                username = account["accountServiceHomepage"].split("/")[-1]
            else:
                return None
            api = twitter.Api()
            return api.GetUserTimeline(username)
    return None
