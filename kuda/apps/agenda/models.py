from __future__ import unicode_literals

from django.db import models


class Event(models.Model):
    CONCERT = 'concert'
    LECTURE = 'lecture'
    THEATRE = 'theatre'
    ART = 'art'
    OTHER = 'other'

    KINDS = (
        (CONCERT, CONCERT),
        (LECTURE, LECTURE),
        (THEATRE, THEATRE),
        (ART, ART),
        (OTHER, OTHER)
    )

    RESTR = (
        (0, '0+'),
        (6, '6+'),
        (12, '12+'),
        (16, '16+'),
        (18, '18+'),
        (21, '21+')
    )

    kind = models.CharField(choices=KINDS, max_length=7)
    title = models.CharField(max_length=256)
    restriction = models.PositiveSmallIntegerField(choices=RESTR, null=True)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='events')
    places = models.ManyToManyField('Place', through='ScheduleItem')


class Place(models.Model):
    title = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    description = models.TextField()
    url = models.URLField()
    tags = models.ManyToManyField('tag', related_name='places')


class Tag(models.Model):
    value = models.CharField(max_length=24, db_index=True)


class ScheduleItem(models.Model):
    event = models.ForeignKey(to=Event)
    place = models.ForeignKey(to=Place)
    when = models.DateTimeField(db_index=True)
