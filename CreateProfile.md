This is how you are _supposed_ to be able to create a FOAF profile using foaflib.  If you follow the instructions here and something goes wrong, it may be a bug!  Let me know.

The profile we create in this example is the same one we access in the example on the ReadProfile page.

```
from foaflib.classes.person import Person
from foaflib.classes.onlineaccount import OnlineAccount

# Create a new person
me = Person()

# Set basic attributes
me.name = "Bill Bloggs"
me.gender = "male"
me.homepage = "http://www.bill.bloggs.net"
me.add_mbox("mailto:bill@bloggs.net")
me.add_mbox("mailto:bill@megacorp.com")

# Add a friend (someone you foaf:know), from scratch
wife = Person()
wife.name = "Belinda Bloggs"
wife.gender = "female"
wife.homepage = "http://www.belinda.bloggs.net"
wife.add_mbox("mailto:belinda@bloggs.net")
me.add_friend(wife)

# Add a friend who already has a FOAF profile
friend = Person("http://www.john.johnson.net/foaf.rdf")
me.add_friend(friend)

# Add an account
twitter = OnlineAccount()
twitter.accountServiceHomepge = "http://www.twitter.com"
twitter.accountName = "bbloggs42"
me.add_account(twitter)

# Save file
me.save_as_xml_file("my_foaf.rdf")
```