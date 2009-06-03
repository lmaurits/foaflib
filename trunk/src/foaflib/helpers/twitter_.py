import twitter

def get_latest_tweets(foafprofile):
    for account in foafprofile.accounts:
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
