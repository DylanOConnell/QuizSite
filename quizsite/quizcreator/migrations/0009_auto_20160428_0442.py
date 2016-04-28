# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quizcreator', '0008_auto_20160427_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizresult',
            name='user',
            field=models.ForeignKey(default=datetime.datetime(2016, 4, 28, 4, 42, 22, 440577, tzinfo=utc), to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
