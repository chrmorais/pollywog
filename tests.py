import sys
import unittest

from pollywog import R


class PollywogTestCase(unittest.TestCase):
    simple = R/'(foo|bar)(?P<baz>\d+)'
    url_re = '(?P<scheme>https?://)(?P<host>[^/]+)(?P<path>/[\S]*)?'

    def test_bool(self):
        valid = (
            'foo99',
            'bar1',
            'xfoo2y',
            'barfoo3')
        invalid = (
            'foo',
            'bar',
            'foox1',
            '')

        for test_str in valid:
            self.assertTrue(self.simple/test_str)

        for test_str in invalid:
            self.assertFalse(self.simple/test_str)

    def test_iteration(self):
        sample = (
            'This is a test. Visit http://charlesleifer.com/ for more '
            'examples.\n'
            'Also check out my GitHub: https://github.com/coleifer/')
        result = R/self.url_re/sample
        self.assertEqual(list(result), [
            ('http://', 'charlesleifer.com', '/'),
            ('https://', 'github.com', '/coleifer/')])

        self.assertEqual(list(result.iter_dicts()), [
            {'scheme': 'http://', 'host': 'charlesleifer.com', 'path': '/'},
            {'scheme': 'https://', 'host': 'github.com', 'path': '/coleifer/'},
        ])

        self.assertEqual(list(result.iter_dicts(start_idx=40)), [
            {'scheme': 'https://', 'host': 'github.com', 'path': '/coleifer/'},
        ])
        self.assertEqual(list(result.iter_dicts(end_idx=50)), [
            {'scheme': 'http://', 'host': 'charlesleifer.com', 'path': '/'},
        ])

    def test_replace(self):
        self.assertEqual(self.simple/'foo99'/'nugget', 'nugget')
        self.assertEqual(self.simple/'hey foo2s'/'nugget', 'hey nuggets')
        self.assertEqual(self.simple/'foo bar2s'/'nugget', 'foo nuggets')

        # No match, so no replacement.
        self.assertEqual(self.simple/'hey foos'/'nugget', 'hey foos')
        self.assertEqual(self.simple/'bar foo barf'/'nugget', 'bar foo barf')

    def test_search(self):
        self.assertEqual(
            (self.simple/'foo99').search(),
            ('foo', '99'))
        self.assertEqual(
            (self.simple/'xxfoo99yy').search(),
            ('foo', '99'))
        self.assertEqual(
            (self.simple/'foo99').search(as_dict=True),
            {'baz': '99'})
        result = self.simple/'foo3 bar2 foo1'
        self.assertEqual(result.search(), ('foo', '3'))
        self.assertIsNone((self.simple/'fooxx').search())

    def test_search_byref(self):
        result = {}
        R/self.url_re/'http://charlesleifer.com/blog/'>>result
        self.assertEqual(result, {
            'scheme': 'http://',
            'host': 'charlesleifer.com',
            'path': '/blog/',
        })

        result = []
        R/self.url_re/'http://charlesleifer.com/blog/'>>result
        self.assertEqual(result, ['http://', 'charlesleifer.com', '/blog/'])

    def test_split(self):
        self.assertEqual(R/'\d+'-'h39x fo0o', ['h', 'x fo', 'o'])


if __name__ == '__main__':
    unittest.main(argv=sys.argv)
