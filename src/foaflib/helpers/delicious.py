from foaflib.helpers.basehelper import BaseHelper
from foaflib.utils.activitystreamevent import ActivityStreamEvent

class Delicious(BaseHelper):

    def __init__(self):

        try:
            import deliciousapi
            self.deliciousapi = deliciousapi
            self._supported = True
        except ImportError:
            self._supported = False

    def _accept_account(self, account):

        homepage = account.accountServiceHomepage
        return "del.icio.us" in homepage or "delicious.com" in homepage

    def _handle_account(self, account):

        events = []
        username = account.accountName
        print username
        if not username:
            return events
        api = self.deliciousapi.DeliciousAPI()
        user = api.get_user(username)
        for bookmark in user.bookmarks:
            event = ActivityStreamEvent()
            event.type = "Del.icio.us"
            event.detail = "Bookmarked: %s" % bookmark[2]
            event.link = bookmark[0]
            event.timestamp = bookmark[4].timetuple()
            events.append(event)
        return events 
