# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ixxy_admin_utils.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        ('link_report', '0002_auto_20170203_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='IgnoredUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=2048)),
            ],
            bases=(ixxy_admin_utils.model_mixins.AdminUrlMixin, models.Model),
        ),
    ]
