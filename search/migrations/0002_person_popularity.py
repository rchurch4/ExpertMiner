# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='popularity',
            field=models.IntegerField(default=b'0'),
            preserve_default=True,
        ),
    ]
