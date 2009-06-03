import rdflib
from rdflib.Graph import ConjunctiveGraph as Graph
from urllib import urlopen

from foaflib.classes.agent import Agent

_SINGLETONS = "title name nick givenname firstName surname family_name homepage geekcode meyersBriggs dnaChecksum plan".split()
_BASIC_MULTIS = "schoolHomepage workplaceHomepage img currentProject pastProject publications isPrimaryTopicOf page made workInfoHomepage interest".split()

class Person(Agent):

    def __init__(self, path=None):

	Agent.__init__(self)
        for name in _BASIC_MULTIS:
            setattr(self, "_get_%ss" % name, self._make_getter(name))
            setattr(Person, "%ss" % name, property(self._make_property_getter(name)))
            setattr(self, "add_%s" % name, self._make_adder(name))
            setattr(self, "del_%s" % name, self._make_deler(name))

        self._graph = Graph()
        if path:
            self._graph.parse(path)
        else:
            self._setup_profile()

    def _setup_profile(self):
        x = rdflib.BNode()
        self._graph.add((x, rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.URIRef('http://xmlns.com/foaf/0.1/PersonalProfileDocument')))
        self._graph.add((x, rdflib.URIRef('http://webns.net/mvcb/generatorAgent'), rdflib.URIRef('http://code.google.com/p/foaflib')))
        self._graph.add((x, rdflib.URIRef('http://xmlns.com/foaf/0.1/primaryTopic'), rdflib.URIRef('#me')))
        self._graph.add((rdflib.URIRef('#me'), rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.URIRef('http://xmlns.com/foaf/0.1/Person')))

    # Things you can only reasonably have one of - gender, birthday, first name, etc. - are termed
    # "singletons".  Singletion I/O is handled purely through __getattr__ and __setattr__, below.
    def __getattr__(self, name):
        if name in _SINGLETONS:
            for raw in self._graph.objects(predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/%s' % name)):
                return unicode(raw)
            return None
        return Agent.__getattr__(self, name)
            
    def __setattr__(self, name, value):
        if name in _SINGLETONS:
            self._graph.remove((None, rdflib.URIRef('http://xmlns.com/foaf/0.1/%s' % name), None))
            self._graph.add((self._get_primary_topic(), rdflib.URIRef('http://xmlns.com/foaf/0.1/%s' % name), value))
        else:
            Agent.__setattr__(self, name, value)

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
    def get_xml_string(self, format="rdf/xml"):
        return self._graph.serialize(format=format)

    def save_as_xml_file(self, filename, format="rdf/xml"):
        self._graph.serialize(filename, format=format)
