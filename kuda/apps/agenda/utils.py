from datetime import datetime
from mapper.parser import ModelAwareXMLParser
from mapper.model_mapper import ModelMapper, FieldBinding
from models import Event, Tag, Place, ScheduleItem

from django.utils.timezone import make_aware


class EventMapper(ModelMapper):
    class meta:
        model = Event

    id = FieldBinding('@id')
    kind = FieldBinding('@type')
    title = FieldBinding('title')
    restriction = FieldBinding(lambda c: c['age_restricted'][:-1])
    description = FieldBinding('text')
    tags = FieldBinding('tags')

    def save_m2m(self, inst, m2m_data):
        for tag in m2m_data['tags']:
            inst.tags.add(Tag.objects.get_or_create(value=tag)[0])


class PlaceMapper(ModelMapper):
    class meta:
        model = Place

    id = FieldBinding('@id')
    title = FieldBinding('title')
    description = FieldBinding('text')
    url = FieldBinding('url')
    tags = FieldBinding('tags')

    def save_m2m(self, inst, m2m_data):
        for tag in m2m_data['tags']:
            inst.tags.add(Tag.objects.get_or_create(value=tag)[0])


class ScheduleMapper(ModelMapper):
    class meta:
        model = ScheduleItem

    event_id = FieldBinding('@event')
    place_id = FieldBinding('@place')
    when = FieldBinding(
        lambda c: make_aware(datetime.strptime('%(@date)s %(@time)s' % c, '%Y-%m-%d %H:%M'))
    )


def import_feed(feed):
    p = ModelAwareXMLParser()
    p.register_mapper('event', EventMapper())
    p.register_mapper('place', PlaceMapper())
    p.register_mapper('session', ScheduleMapper())
    p.run(feed)
