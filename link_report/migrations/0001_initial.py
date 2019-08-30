# -*- coding: utf-8 -*-


from django.db import migrations, models
import ixxy_admin_utils.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        ('redirects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sentry404Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField()),
                ('sentry_id', models.PositiveIntegerField()),
                ('referer', models.CharField(max_length=1024, null=True, blank=True)),
                ('referer_domain', models.CharField(max_length=128, null=True, blank=True)),
                ('user_agent', models.CharField(max_length=512, null=True, blank=True)),
                ('browser', models.CharField(max_length=128, null=True, blank=True)),
                ('browser_type', models.CharField(max_length=128, null=True, blank=True)),
                ('device', models.CharField(max_length=128, null=True, blank=True)),
                ('os', models.CharField(max_length=128, null=True, blank=True)),
                ('user', models.CharField(max_length=128, null=True, blank=True)),
            ],
            bases=(ixxy_admin_utils.model_mixins.AdminUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Sentry404Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=2048)),
                ('first_seen', models.DateTimeField()),
                ('last_seen', models.DateTimeField()),
                ('sentry_id', models.PositiveIntegerField()),
            ],
            bases=(ixxy_admin_utils.model_mixins.AdminUrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RedirectFacade',
            fields=[
            ],
            options={
                'verbose_name': 'Redirect',
                'proxy': True,
            },
            bases=(ixxy_admin_utils.model_mixins.AdminUrlMixin, 'redirects.redirect'),
        ),
        migrations.AddField(
            model_name='sentry404event',
            name='issue',
            field=models.ForeignKey(related_name='events', to='link_report.Sentry404Issue', on_delete=models.CASCADE),
        ),
    ]
