# Usage #

The `ActivityStream` class makes it easy to keep track of things your friends do online, like making blog posts and Twitter updates, etc.  It's super simple:

```
from foaflib.classes.person import Person
from foaflib.utils.activitystream import ActivityStream

# Fetch the FOAF profile of the friend to watch
p = Person("http://www.bill.bloggs.net/foaf.rdf")

# Create an ActivityStream object for that friend
stream = ActivityStream(p)

# Iterate over the latest things they've done:
for event in stream.get_latest_events():
    event_handler(event)
```

Each value of `event` in that final loop is an instance of the `AcctivityStreamEvent` class.  This is a very simple class with four attributes:

  * `type` - A string conveying what type of event this is - like "Blog post" or "Twitter", etc.
  * `detail` - A string that explains the gist of the event - like the title of a blog post, or a Twitter status, etc.
  * `link` - A string holding the URL for this event - like the URL of a blog post
  * `timestamp` - A `time.struct_time` instance representing the time of the event

That's all there is to it!

# How does this work? #

The `ActivityStream` object makes use of the `weblog` property of a FOAF profile to pull in blog posts, and `OnlineAccount`s specified by the `holdsAccount` property of a FOAF profile to pull in things like Twitter statuses.  If a certain FOAF profile does not have a specified `weblog` or some `OnlineAccounts` then an `ActivityStream` object for that profile will return an empty list of events every time.

Blog posts are pulled in on the basis of the `weblog` property by using the [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) library to parse the HTML of the blog page and look for `<link type="rel"/>` tags that include the addresses of RSS or Atom feeds.  These feeds are then parsed using the [feedpraser](http://www.feedparser.org/) library.

Everything else is pulled in on the basis of a `holdsAccount` property using something called a _helper_.  foaflib comes with a number of helpers which use either third party Python libraries (like [code.google.com/p/python-twitter/ Python Twitter]) or foaflib-developed code to create `ActivityStreamEvent` objects.  You can find a complete list of current foaflib helpers at the HelpersList page, and you can find instructions on how to write your own helper for a currently unsupported service at the WritingHelpers page.