This is how you are supposed to be able to read a FOAF profile using foaflib. If you follow the instructions here and something goes wrong, it may be a bug! Let me know.

The profile we access in this example is the same one we create in the example on the CreateProfile page.

```
>>> from foaflib.classes.person import Person

>>> # Read profile from URI
>>> bill = Person("http://www.bill.bloggs.net/foaf.rdf")

>>> # Access basic attributes
>>> print bill.name
Bill Bloggs

>>> # Iterate over people the person foaf:knows (as Person objects)
>>> for friend in bill.friends:
>>>     print friend.name
Belinda Bloggs

>>> # Iterate over the accounts the person foaf:holdsAccounts (as OnlineAccount objects)
>>> for account in bill.accounts:
>>>     print account.accountName + "@" + account.accountServiceHomepage
bbloggs42@http://www.twitter.com
```