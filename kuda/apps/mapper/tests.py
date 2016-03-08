#!/usr/bin/env python
import functools
import StringIO

from django.db import models
from django.conf import settings
from django.core.management import call_command
from django.apps import apps
from django.test import TestCase

from parser import CallBackXMLParser
from model_mapper import ModelMapper, FieldBinding

from test_app.models import TestModel


class SaxParserTest(TestCase):
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


class ModelMapperTestCase(TestCase):
    apps = ('mapper.test_app.apps.TestAppConfig',)

    def _pre_setup(self):
        self._original_installed_apps = list(settings.INSTALLED_APPS)
        for app in self.apps:
            settings.INSTALLED_APPS.append(app)
        apps.ready = False
        apps.app_configs = {}
        apps.populate(settings.INSTALLED_APPS)
        call_command('migrate', interactive=False, verbosity=0)
        super(TestCase, self)._pre_setup()

    def _post_teardown(self):
        super(TestCase, self)._post_teardown()
        settings.INSTALLED_APPS = self._original_installed_apps

    def setUp(self):
        class TestMapper(ModelMapper):
            class meta:
                model = TestModel

            field1 = FieldBinding('binding_for_field1')
            field2 = FieldBinding('binding_for_field2')

        self.mapper_class = TestMapper

    def test_nullable_fields(self):
        self.assertTrue(self.mapper_class.fields['field1'].nullable)
        self.assertFalse(self.mapper_class.fields['field2'].nullable)

    def test_instance_creation_success(self):
        m = self.mapper_class()
        m.extract({
            'binding_for_field1': '1',
            'binding_for_field2': 'qwerty'
        })
        self.assertEqual(m.extracted['field1'], '1')
        self.assertEqual(m.extracted['field2'], 'qwerty')

        i = m.save()
        i.refresh_from_db()
        self.assertEqual(i.field1, 1)
        self.assertEqual(i.field2, 'qwerty')

    def test_instance__partial_creation_success(self):
        m = self.mapper_class()
        m.extract({
            'binding_for_field2': 'qwerty'
        })
        self.assertEqual(m.extracted['field2'], 'qwerty')

        i = m.save()
        i.refresh_from_db()
        self.assertEqual(i.field1, None)
        self.assertEqual(i.field2, 'qwerty')

    def test_instance_creation_failure(self):
        m = self.mapper_class()
        c = {
            'binding_for_field1': '1',
        }
        self.assertRaisesMessage(
            ValueError, 'no value in binding_for_field2', m.extract, c
        )

