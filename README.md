# conftodict
Python module to convert Cisco IOS config to a python dictionary
Built and tested with Python 3. Python 2 not tested at this time

###Example Usage:
```python
from conftodict import ConfToDict
from configaudit import search_keys, search_values

c = ConfToDict('tests/test.txt', from_file=True)
config = c.to_dict()

commands = ['voice rtp send-recv', 'sccp local Loopback0', 'voice service voip']
result = search_keys(config, commands)

result.ok
False

result.error
'extra key(s) found'

result.extra
['interface GigabitEthernet1/0',
 'mgcp profile default',
 'line vty 5 15',
 'voice class codec 1',
 'service password-encryption',
 'ip cef',
 'dspfarm profile 2 conference',
 'interface Vlan1',
 ...]

commands = ['no ip address', 'shutdown', 'duplex auto', 'speed auto']
result = search_values(config['interface GigabitEthernet0/1'], commands)

result.ok
True
```