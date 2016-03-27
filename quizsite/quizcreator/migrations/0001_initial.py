# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('correct_type', models.CharField(default=b'FULL_W', max_length=6, choices=[(b'COR', b'Correct'), (b'PART_W', b'Partly Wrong'), (b'FULL_W', b'Fully Wrong')])),
            ],
        ),
        migrations.CreateModel(
            name='Answer_results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selected', models.BooleanField()),
                ('answer', models.ForeignKey(to='quizcreator.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz_results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('quiz', models.ForeignKey(to='quizcreator.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.CharField(default=b'usr', max_length=3, choices=[(b'adm', b'Admin'), (b'usr', b'User')])),
            ],
        ),
        migrations.AddField(
            model_name='quiz_results',
            name='user',
            field=models.ForeignKey(to='quizcreator.User'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(blank=True, to='quizcreator.Quiz', null=True),
        ),
        migrations.AddField(
            model_name='answer_results',
            name='question',
            field=models.ForeignKey(to='quizcreator.Question'),
        ),
        migrations.AddField(
            model_name='answer_results',
            name='quiz',
            field=models.ForeignKey(to='quizcreator.Quiz'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, to='quizcreator.Question', null=True),
        ),
    ]
