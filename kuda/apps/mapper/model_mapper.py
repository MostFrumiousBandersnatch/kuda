import six
import logging
from django.db import models, transaction

logger = logging.getLogger(__package__)

VOID = object()


class FieldBinding(object):
    def __init__(self, key):
        self.key = key
        self.nullable = False
        self.m2m = False

    def extract(self, context):
        if callable(self.key):
            try:
                value = self.key(context)
            except Exception as e:
                value = VOID
                logger.warn(e)
        else:
            value = context.get(self.key, VOID)

        if value is VOID and not self.nullable:
            raise ValueError('no value in %s' % self.key)

        return value


class ModelMapperMeta(type):
    def __new__(cls, name, bases, attrs):
        if 'meta' in attrs:
            model = attrs['meta'].model

            assert issubclass(model, models.Model)
            fields = {}
            for name, field in attrs.items():
                if isinstance(field, FieldBinding):
                    model_field = model._meta.get_field(name)
                    if model_field.many_to_many is None:
                        field.nullable = model_field.null

                    field.m2m = bool(model_field.many_to_many)
                    fields[name] = field

            attrs.update(fields=fields)

        return type.__new__(cls, name, bases, attrs)


class ModelMapper(six.with_metaclass(ModelMapperMeta)):
    """
        Maps an arbitrary data structure to a flat (almost) map, may be easily
        converted to model instance
    """
    def extract(self, context):
        self.extracted = {}
        self.m2m_extracted = {}

        for name, field in self.fields.iteritems():
            try:
                value = field.extract(context)
            except ValueError as e:
                raise ValueError('%s: %s' % (name, e))

            if value is not VOID:
                if not field.m2m:
                    self.extracted[name] = value
                else:
                    self.m2m_extracted[name] = value

        return True

    @transaction.atomic
    def save(self):
        if self.extracted:
            inst = self.meta.model.objects.create(
                **self.extracted
            )

        if self.m2m_extracted:
            self.save_m2m(inst, self.m2m_extracted)

        self.extracted = None
        self.m2m_extracted = None

        return inst

    def save_m2m(self, inst, m2m_data):
        pass
