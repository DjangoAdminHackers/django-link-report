# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_report', '0003_ignoredurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ignoredurl',
            name='url',
            field=models.CharField(max_length=512),
        ),
    ]
