# conftodict
Python module to convert Cisco IOS config to a python dictionary

###Example Usage:
```python
from conftodict import ConfToDict
from configaudit import search_dict
c = ConfToDict('tests/test.txt', from_file=True)
stuff = c.to_dict()
things = ['priority percent 20', 'set ip dscp ef']
blah = search_dict(stuff['policy-map QOS_CATEGORIES'], 'class QOS_VOICE_RTP', things)
blah.ok
True
```