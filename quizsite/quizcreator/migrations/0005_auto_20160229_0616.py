# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizcreator', '0004_auto_20160229_0520'),
    ]

    operations = [
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.CharField(default=b'usr', max_length=3, choices=[(b'adm', b'Admin'), (b'usr', b'User')])),
            ],
        ),
        migrations.RemoveField(
            model_name='questions',
            name='answers',
        ),
        migrations.AlterField(
            model_name='answer_results',
            name='question',
            field=models.ForeignKey(to='quizcreator.question'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(to='quizcreator.question'),
        ),
        migrations.AlterField(
            model_name='quiz_results',
            name='user',
            field=models.ForeignKey(to='quizcreator.user'),
        ),
        migrations.DeleteModel(
            name='questions',
        ),
        migrations.DeleteModel(
            name='users',
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, to='quizcreator.question', null=True),
        ),
    ]
