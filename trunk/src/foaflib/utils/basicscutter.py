import rdflib
from foaflib.classes.person import Person

class BasicScutter(object):

    def __init__(self, seed_uris=None): 
        if seed_uris is None:
            seed_uris = []
        self.current_list = seed_uris
        self.next_list = []
        self.seen_uris = []

    def get_people(self):
        while self.current_list:
            for uri in self.current_list:
                if uri in self.seen_uris:
                    continue
                try:
                    p = Person(uri)
                    self.seen_uris.append(uri)
                except:
                    print "Skipping bad URI"
                    continue
                for friend in p._graph.objects(predicate=rdflib.URIRef('http://xmlns.com/foaf/0.1/knows')):
                    for uri in p._graph.objects(subject=friend, predicate=rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#seeAlso")):
                        self.next_list.append(uri)
                        break
                yield p
            self.current_list = self.next_list[:]
            self.next_list = []
