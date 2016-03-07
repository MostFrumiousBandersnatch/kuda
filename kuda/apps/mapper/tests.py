#!/usr/bin/env python
import unittest
import functools
import StringIO

from django.db import models
from django.conf import settings

from parser import CallBackXMLParser
from model_mapper import ModelMapper, FieldBinding


class SaxParserTest(unittest.TestCase):
    def test_attribute(self):
        feed = StringIO.StringIO("""<?xml version="1.0" encoding="utf8"?>
<feed version="1.1">
    <a d="e">
        <b>c</b>
    </a>
</feed>
""")
        res = {'context': None}

        def cb(res, context):
            res['context'] = context

        p = CallBackXMLParser()
        p.register_cb('a', functools.partial(cb, res))
        p.run(feed)
        self.assertEqual(res['context']['b'], 'c')
        self.assertEqual(res['context']['@d'], 'e')

    def test_list(self):
        feed = StringIO.StringIO("""<?xml version="1.0" encoding="utf8"?>
<feed version="1.1">
    <a>
        <b>c</b>
        <b>d</b>
    </a>
</feed>
""")
        res = {'context': None}

        def cb(res, context):
            res['context'] = context

        p = CallBackXMLParser()
        p.register_cb('a', functools.partial(cb, res))
        p.run(feed)
        self.assertEqual(res['context'], [u'c', u'd'])

    def test_sensivity(self):
        feed = StringIO.StringIO("""<?xml version="1.0" encoding="utf8"?>
<feed version="1.1">
    <a d="e">
        <b>c</b>
    </a>
    <a>
        <b>f</b>
    </a>
</feed>
""")
        res_a = {
            'cnt': 0,
        }

        res_f = {
            'cnt': 0,
        }

        def cb(res, context):
            res['cnt'] += 1

        p = CallBackXMLParser()
        p.register_cb('a', functools.partial(cb, res_a))
        p.register_cb('f', functools.partial(cb, res_f))
        p.run(feed)
        self.assertEqual(res_a['cnt'], 2)
        self.assertEqual(res_f['cnt'], 0)

if __name__ == '__main__':
    unittest.main()
