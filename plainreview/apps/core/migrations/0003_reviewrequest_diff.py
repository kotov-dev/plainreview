# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20140911_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrequest',
            name='diff',
            field=models.TextField(default=datetime.date(2014, 9, 11)),
            preserve_default=False,
        ),
    ]
