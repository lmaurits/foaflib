import rdflib
from rdflib.Graph import ConjunctiveGraph as Graph
from urllib import urlopen

_SINGLETONS = """title name nick givenname firstName surname family_name
birthday gender homepage geekcode meyersBriggs dnaChecksum plan""".split()
_BASIC_MULTIS = """weblog schoolHomepage workplaceHomepage aimChatID
icqChatID jabberID msnChatID yahooChatID mbox mbox_sha1sum openid
img currentProject pastProject publications isPrimaryTopicOf  tipjar page
made
workInfoHomepage""".split()

class Person(object):

    def __init__(self, path=None):

        self._graph = Graph()
        if path:
            self._graph.parse(path)
        for name in _BASIC_MULTIS:
            setattr(self, "_get_%ss" % name, self._make_getter(name))
            setattr(Person, "%ss" % name, property(self._make_property_getter(name)))
            setattr(self, "add_%s" % name, self._make_adder(name))
            setattr(self, "del_%s" % name, self._make_deler(name))

    def _get_primary_topic(self):
        for topic in self._graph.objects(predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/primaryTopic')):
            return topic

    # Things you can only reasonably have one of - gender, birthday, first name, etc. - are termed
    # "singletons".  Singletion I/O is handled purely through __getattr__ and __setattr__, below.
    def __getattr__(self, name):
        if name in _SINGLETONS:
            for raw in self._graph.objects(predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/%s' % name)):
                return unicode(raw)
            return None
        raise AttributeError, name
            
    def __setattr__(self, name, value):
        if name in _SINGLETONS:
            self._graph.remove((None, rdflib.URIRef('http://xmlns.com/foaf/0.1/%s' % name), None))
            self._graph.add((self._get_primary_topic(), rdflib.URIRef('http://xmlns.com/foaf/0.1/%s' % name), value))
        else:
            object.__setattr__(self, name, value)

    # Stuff you might have more than one of - weblogs, accounts, friends, etc. - are handled by a
    # combination of the property decorator and add/del methods.

    def _make_getter(self, name):
        def method():
            return [unicode(x) for x in self._graph.objects(predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/%s' % name))]
        return method

    def _make_property_getter(self, name):
        def method(self):
            return [unicode(x) for x in self._graph.objects(predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/%s' % name))]
        return method

    def _make_adder(self, name):
        def method(value):
            self._graph.add((self._get_primary_topic(), rdflib.URIRef('http://xmlns.com/foaf/0.1/%s' % name), rdflib.URIRef(value)))
        return method

    def _make_deler(self, name):
        def method(value):
            self._graph.remove((self._get_primary_topic(), rdflib.URIRef('http://xmlns.com/foaf/0.1/%s' % name), rdflib.URIRef(value)))
        return method

    def _build_account(self, acct):
        result = {}
        if isinstance(acct, rdflib.URIRef):
            result["accountServiceHomepage"] = unicode(acct)
        elif isinstance(acct, rdflib.Literal):
            result["accountName"] = unicode(acct)
        elif isinstance(acct, rdflib.BNode):
            for pred, obj in self._graph.predicate_objects(acct):
                if pred == rdflib.URIRef("http://xmlns.com/foaf/0.1/accountServiceHomepage"):
                    result["accountServiceHomepage"] = unicode(obj)
                elif pred == rdflib.URIRef("http://xmlns.com/foaf/0.1/accountName"):
                    result["accountName"] = unicode(obj)
                elif pred == rdflib.URIRef("http://xmlns.com/foaf/0.1/accountProfilePage"):
                    result["accountProfilePage"] = unicode(obj)
        return result

    def _get_accounts(self):
        for raw_account in self._graph.objects(predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/holdsAccount')):
            account = self._build_account(raw_account)
            if account:
                yield account

    accounts = property(_get_accounts)

    def add_account(self, accountServiceHomepage, accountName, accountProfilePage=None):
        x = rdflib.BNode()
        self._graph.add((x, rdflib.URIRef("http://xmlns.com/foaf/0.1/accountServiceHomepage"), rdflib.URIRef(accountServiceHomepage)))
        self._graph.add((x, rdflib.URIRef("http://xmlns.com/foaf/0.1/accountName"), rdflib.URIRef(accountName)))
        if accountProfilePage:
            self._graph.add((x, rdflib.URIRef("http://xmlns.com/foaf/0.1/accountProfilePage"), rdflib.URIRef(accountProfilePage)))
        self._graph.add((self._get_primary_topic, rdflib.URIRef("http://xmlns.com/foaf/0.1/holdsAccount"), x))

    # Friend stuff
    def _build_friend(self, frnd):
        if isinstance(frnd, rdflib.URIRef):
            return Person(unicode(frnd))
        elif isinstance(frnd, rdflib.BNode):
            # If a "seeAlso gives us the URI of the friend's FOAF profile, use that
            for uri in self._graph.objects(subject=frnd, predicate=rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#seeAlso")):
                return Person(unicode(uri))
            # Otherwise just build up a graph of what we have and use that
            g = Graph()
            for triple in self._graph.triples((frnd, None, None)):
                g.add(triple)
            f = Person()
            f._graph = g
            return f 
        return None

    def _get_friends(self):
        for raw_friend in self._graph.objects(predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/knows')):
            friend = self._build_friend(raw_friend)
            if friend:
                yield friend

    friends = property(_get_friends)

    # Serialisation
    def get_xml_string(self):
        self._graph.serialize()

    def save_as_xml_file(self, filename):
        self._graph.serialize(filename)

    # Account stuff
