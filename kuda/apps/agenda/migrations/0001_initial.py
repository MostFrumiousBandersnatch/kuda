# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-07 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('concert', 'concert'), ('lecture', 'lecture'), ('theatre', 'theatre'), ('art', 'art'), ('other', 'other')], max_length=7)),
                ('title', models.CharField(max_length=256)),
                ('restriction', models.PositiveSmallIntegerField(choices=[(0, '0+'), (6, '6+'), (12, '12+'), (16, '16+'), (18, '18+'), (21, '21+')], null=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(db_index=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.Event')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.Place')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=24)),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='tags',
            field=models.ManyToManyField(related_name='places', to='agenda.Tag'),
        ),
        migrations.AddField(
            model_name='event',
            name='places',
            field=models.ManyToManyField(through='agenda.ScheduleItem', to='agenda.Place'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(related_name='events', to='agenda.Tag'),
        ),
    ]
