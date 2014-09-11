# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_reviewrequest_diff'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrequest',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 11, 14, 15, 48, 228676), auto_now_add=True),
            preserve_default=False,
        ),
    ]
