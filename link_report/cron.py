# This file works with our fork of django-cron.
# It's use is optional
# Use any means you like to run scheduled jobs.


from django_cron import cronScheduler
from django_cron import Job
from django_cron import DAY
from link_report.utils import update_sentry_404s


class RunUpdateSentry404s(Job):

        run_every = DAY
        unreliable = DAY * 3

        def job(self):
            update_sentry_404s()

cronScheduler.register(RunUpdateSentry404s)
