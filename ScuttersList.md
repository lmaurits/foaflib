# List of scutter classes #

See the [Scuttering](http://code.google.com/p/foaflib/wiki/Scuttering) page for how to use these classes

## BasicScutter ##

`foaflib.utils.basicscutter`

The class from which all other scutter classes inherit.  Does nothing but yield `Person` objects.

## FileStorageScutter ##

`foflib.utils.filestoragescutter`

Requires a directory name as a constructor argument.  Saves FOAF profiles in RDF/XML format in that directory before yielding the corresponding `Person` object.  The filename for each profile is computed by running some details about the profile (name, homepage, mbox and mbox\_sha1sum values) through the SHA1 hash algorithm.