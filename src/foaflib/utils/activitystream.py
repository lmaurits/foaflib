import foaflib.helpers.blog as blog
import foaflib.helpers.identica as identica
import foaflib.helpers.twitter_ as twitter

class ActivityStream(object):

    def __init__(self, foafperson):
        self.person = foafperson

    def get_latest_events(self, count=10):
        events = []
        events.extend(blog.get_latest(self.person))
        for helper in [identica, twitter]:
            events.extend(helper.get_latest(self.person))
        events.sort()
        events.reverse()
        return events[0:count+1]
