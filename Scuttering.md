# What's a scutter? #

"Scutter" is the FOAF community's term for what is usually called a "spider" in a web context.  A scutter is a piece of software which follows the `foaf:knows` links from an initial list of FOAF profiles to find more profiles - then it follows the links at _those_ profiles to find even more, and so on, spreading out over FOAFspace like a spider weaving a web.   Scutters can do various things with the profiles they collect, like save them to a local file, or drop them into a database, or compute statistics about FOAF users, etc.

I suspect but haven't confirmed that the name "scutter" is a reference to Red Dwarf.

# How do I use foaflib's scutters? #

foaflib provides a range of scutters for a range of tasks.  You can find an up to date list of available scutters at the ScuttersList page.  All of the scutters are subclasses of `foaflib.utils.basicscutter` so they all behave the same way on the surface:

```
from foaflib.utils.basicscutter import BasicScutter

# List of starting or "seed" uris - you need at least one.
seeds = ["http://www.bill.bloggs.net/foaf.rdf"]

# Create scutter
scutter = BasicScutter(seeds)

# Get 20 FOAF profiles (or less if we run out)
for person in scutter.scutter(uri_limit=20):
    # Each value of person is a Person object
    print person.name
```

Every scutter class has a `scutter` method which takes optional `uri_limit` (maximum number of distinct `People` to yield) and `depth_limit` (maximum number of links to follow from the seed URIs) arguments.  If you don't specify either kind of limit, the scutter will keep going indefinitely, or until it runs out of links to follow.  If you specify both a URI _and_ a depth limit, it will stop after hitting whichever limit it hits first, or until it runs out of links to follow.

Every scutter class' `scutter` method returns an iterator over `Person` objects.  The `BasicScutter` class does nothing else.  Other classes may do something with the Person object before yielding it, like saving it to a file.  For these scutters you don't actually have to do anything with the `Person` objects if all you want to do is save them:

```
# Just save people endlessly and silently
for person in scutter.scutter():
    pass
```

# How do I write new and exciting scutters? #

See the WritingScutters page for details on how to subclass `BasicScutter` to create your own scutter classes.