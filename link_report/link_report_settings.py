from django.conf import settings


BASE_URL = settings.LINK_REPORT_BASE_URL
AUTH_TOKEN = settings.LINK_REPORT_SENTRY_AUTH_TOKEN
API_BASE_URL = settings.LINK_REPORT_SENTRY_API_BASE_URL
ORGANIZATION_SLUG = settings.LINK_REPORT_SENTRY_ORGANIZATION_SLUG
PROJECT_SLUG = settings.LINK_REPORT_SENTRY_PROJECT_SLUG
IGNORE_MISSING_FORWARDED_REQUEST_URI = getattr(settings, 'LINK_REPORT_IGNORE_MISSING_FORWARDED_REQUEST_URI', True)
DISABLE_UPDATE_SENTRY_CRON = getattr(settings, 'LINK_REPORT_DISABLE_UPDATE_SENTRY_CRON', False)
