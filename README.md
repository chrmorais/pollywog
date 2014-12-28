## Pollywog

Syntactic sugar for working with regular expressions in Python. Based on a [blog post](http://charlesleifer.com/blog/playing-with-python-magic-methods-to-make-a-nicer-regex-api/).

### Examples

In the following examples we will use these regular expressions to capture URLs:

```python

from pollywog import R

simple_url_re = '(https?://)([^/]+)(/[\S]*)?'
url_re = '(?P<scheme>https?://)(?P<host>[^/]+)(?P<path>/[\S]*)?'
```

#### Checking if a match exists

```python

url = raw_input('Enter a URL: ')
if R/simple_url_re/url:
    print 'You entered a valid URL'
else:
    print 'That URL appears to be invalid.'
```

#### Extracting data from a match

By default, the `search()` method will return a `tuple`.

```python

url = raw_input('Enter a URL: ')
result = (R/simple_url_re/url).search()
if result:
    scheme, host, path = result
    print 'Scheme:', scheme
    print 'Host:', host
    print 'Path:', path
```

By using named parameters, the `search()` method can also return a `dict`.

```python

url = raw_input('Enter a URL: ')
result = (R/url_re/url).search(as_dict=True)
if result:
    print 'Scheme:', result['scheme']
    print 'Host:', result['host']
    print 'Path:', result['path']
```

#### Iterating over matches

The default iterator will return tuples:

```python

sample = """
    This is a test. Visit http://charlesleifer.com/ for more examples.
    Also check out my GitHub at https://github.com/coleifer/
"""
for scheme, host, path in R/url_re/sample:
    print host + path
```

Though it is also possible to iterate over dictionaries:

```python

sample = """
    This is a test. Visit http://charlesleifer.com/ for more examples.
    Also check out my GitHub at https://github.com/coleifer/
"""
result = R/url_re/sample
for url_dict in result.iter_dicts():
    print url_dict['host'] + url_dict['path']
```

#### Search and Replace

To perform a replacement, just tack on another slash followed by the replacement expression:

```python

print R/'(person)'/'hello person!'/'charlie'
# Prints: "hello charlie!"

print R/'(person)'/'I love you person!'/'baby huey'
# Prints: "I love you baby huey!"
```

Another example using references to capture-groups:

```python

# US phone number with area code, e.g. (555) 123-4567
phone_re = '\((\d{3})\)[-\s](\d{3})-(\d{4})'

# Normalize phone number to use dots.
replacement = r'\1.\2.\3'

print R/phone_re/'(555) 123-4567'/replacement
# Prints: 555.123.4567
```
