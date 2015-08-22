The [FOAF project](http://www.foaf-project.org/) brings social networking into the semantic web.  By publishing information about yourself, your interests, projects and friends in machine readable RDF files, you can participate in a completely decentralised social network, maintaining complete ownership and control of your personal data.

foaflib is a Python library built on the [rdflib](http://www.rdflib.net/) library and designed to make it easy to do things like:
  * Create FOAF files
  * Read FOAF files
  * Use people's FOAF profiles to access their blogs, Twitter feeds, etc.

foaflib is really new and under heavy development.  Assume that nothing works at all, that way you'll be pleasantly surprised when some things do.

The following Wiki pages give short and clear examples that demonstrate how to do everyday FOAF things with foaflib:
  * CreateProfile - How to create a FOAF profile and save it as an XML file.
  * ReadProfile - How to read someone's FOAF profile from a URI into a Python object.
  * ActivityStream - How to use someone's FOAF profile to watch their online activity.
  * [Scuttering](http://code.google.com/p/foaflib/wiki/Scuttering) - How to harvest FOAF profiles by following `foaf:knows` links.

I am rather new to working with FOAF and RDF so comments and contributions from more semantically savvy people are 100% welcome!