# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_report', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='redirectfacade',
            options={'verbose_name': '404 Redirect'},
        ),
        migrations.AlterModelOptions(
            name='sentry404event',
            options={'verbose_name': '404 Report'},
        ),
        migrations.AlterModelOptions(
            name='sentry404issue',
            options={'verbose_name': '404 Issue'},
        ),
    ]
