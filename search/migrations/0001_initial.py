# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('current_affiliation', models.CharField(max_length=30)),
                ('most_recent_university_studied', models.CharField(max_length=50)),
                ('field_of_study', models.CharField(max_length=25)),
                ('subfield1', models.CharField(max_length=25)),
                ('subfield2', models.CharField(max_length=25)),
                ('subfield3', models.CharField(max_length=25)),
                ('most_recent_modification', models.DateTimeField(verbose_name=b'most_recent_modification')),
                ('most_recent_modifier', models.CharField(max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
