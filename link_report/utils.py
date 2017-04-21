from fnmatch import fnmatch
from pprint import pprint

from link_report import link_report_settings
import requests
import time
from django.utils.dateparse import parse_datetime
from .models import Sentry404Event, Sentry404Issue


IGNORE_URLS = [
    
    '+%20$link.attr',
    
    '*.php*',
    '*.asp*',
    '*.htm*',
    '*.jsp*',

    '*/editor/editor/',
    '*/ckeditor/editor/',
    '*/fckeditor/editor/',
    '*/fck/editor/',
    '*/Fckeditornew/editor/',
    '*/Fckeditorold/editor/',
    '*/FCKeditor/editor/',
    '*/Fckeditornew/editor/',
    '*/Fckeditorold/editor/',

    '*/tiny_mce.js/',
    '*/uploadify.swf/',

    '*/InstallWizard.aspx/*',
    '*/phpmyadmin/*',
    
    '/.git/',
    '/a.attr/',
    '/android/',
    '/administrator/',
    '/apple-touch-icon-*.png/',
    '/feed/',
    '/ios/',
    '/js/mage/cookies.js/'
    '/mobile-app/',
    '/mysql/',
    '/rss/',
    '/sql/',
    '/user/register/',
    '/wordpress/',
    '/wp/',
    '/wp-admin/',
]

ACCEPT_USER_AGENTS = [
    'Amazon Silk',
    'AppleMail',
    'Chrome',
    'Chrome Mobile',
    'Edge',
    'Facebook',
    'Firefox',
    'Iceweasel',
    'IE',
    'Lynx',
    'Mobile Safari',
    'Opera',
    'Opera Mini',
    'Pinterest',
    'Safari',
    'WebKit Nightly',
]


def check_issue_is_valid(issue_params):
    invalid = False
    url = issue_params['url'].replace(link_report_settings.BASE_URL, '')  # Strip host
    invalid = invalid or any(fnmatch(url, pat) for pat in IGNORE_URLS)
    return not invalid


def check_event_is_valid(event_params):
    valid = all([
        event_params['browser_type'] is None or any(fnmatch(event_params['browser_type'], pat) for pat in ACCEPT_USER_AGENTS),
    ])
    return valid


def update_sentry_404s():
    Sentry404Issue.objects.all().delete()
    Sentry404Event.objects.all().delete()
        
    # Query Params:
    #
    # query=logger%3Ahttp404
    # sort=date|freq|new
    # statsPeriod=24h|14d
    # shortIdLookup=0|1
    # limit=[int]

    api_url = u'{}projects/{}/{}/issues/?query={}&sort=date&limit={}'.format(
        link_report_settings.API_BASE_URL,
        link_report_settings.ORGANIZATION_SLUG,
        link_report_settings.PROJECT_SLUG,
        'logger:http404',
        200,
    )
    headers = {'Authorization': 'Bearer ' + link_report_settings.AUTH_TOKEN}
    issues_response = requests.get(api_url, headers=headers)
    issues = issues_response.json()
    issues = sorted(issues, key=lambda k: k['lastSeen'])
    next_page_url = issues_response.headers['Link'].split(',')[1].split(';')[0][2:-1]  # TODO
    for issue in issues:
        time.sleep(0.5)  # If we request too frequent, it can some times bring down a sentry instance
        api_url = u'{}issues/{}/events/'.format(
            link_report_settings.API_BASE_URL,
            issue['id']
        )
        
        headers = {'Authorization': 'Bearer ' + link_report_settings.AUTH_TOKEN}
        events = []
        while not (events and 'tags' in events[0]):
            events_response = requests.get(api_url, headers=headers)
            events = events_response.json()
            if events and 'detail' in events and events.get('detail', None) == 'Internal Error':
                events = None
                time.sleep(60)

            if not (events and 'tags' in events[0]):
                print 'retrying'
                time.sleep(60)
                continue

        # Issue 'culprit' doesn't include query strings
        # However the url we extract from the issue title is truncated if too long
        # The best we can do is pick the longer of the two:
        url_from_culprit = issue.get('culprit', '')
        url_from_title = issue['title'].replace('Page Not Found: ', '')
        if len(url_from_culprit) < len(url_from_title):
            url = url_from_title
        else:
            url = url_from_culprit
        # Once we get the first event for this issue we can grab the url from there
        
        issue_params = dict(
            sentry_id=issue['id'],
            url=url,
            first_seen=parse_datetime(issue['firstSeen']),
            last_seen=parse_datetime(issue['lastSeen']),
        )
        
        if check_issue_is_valid(issue_params):

            event_params_list = []
            for event in events:

                tags = {x['key']: x['value'] for x in event['tags']}
                browser = tags.get('browser', None)
    
                referer = None
                for entry in event['entries']:
                    if entry['data'].get('headers', False):
                        headers = {x[0]: x[1] for x in entry['data']['headers']}
                        referer = headers.get('Referer', None)
                        break

                # Replace the issue url with the better version in the headers
                request_uri = headers.get('Forwarded-Request-Uri', '')
                if len(request_uri):
                    issue_params['url'] = request_uri
                else:
                    raise Exception("No Forwarded-Request-Uri found in headers")
                # If we wanted just the querystring: event['entries'][1]['data']['query']

                referer_domain = None
                if referer:
                    referer_parts = referer.split('/')
                    if len(referer_parts) >= 3:
                        referer_domain = referer_parts[2]
    
                browser_type = None
                if browser:
                    parts = browser.split()
                    if len(parts) > 1:
                        browser_type = u' '.join(parts[:-1])
                    else:
                        browser_type = parts[0]

                # # Remove the slash added by common middleware as it's misleading
                # if referer and link_report_settings.BASE_URL in referer:
                #     referer_path = None
                #     if referer:
                #         path_parts = referer.split('?')
                #         path_no_qs = path_parts[0]
                #         if len(path_parts) == 1:
                #             path_qs = ''
                #         elif len(path_parts) == 2:
                #             path_qs = path_parts[1]
                #         elif len(path_parts) > 2:
                #             raise Exception("Multiple '?' in querystring")
                #         # No protocol or domain but always add a trailing slash before the querystring
                #         referer_path = u'{}/'.format(u'/'.join(path_no_qs.split('/')[3:]))
                #         if path_qs:
                #             referer_path += '?' + path_qs
                #     referer_path = referer_path.replace(link_report_settings.BASE_URL, '')
                #     if referer_path == url.replace(link_report_settings.BASE_URL, ''):
                #         print referer_path

                event_params = dict(
                        date_created=parse_datetime(event.get('dateCreated')),
                        sentry_id=event['id'],
                        referer=referer,
                        referer_domain=referer_domain,
                        user_agent=headers.get('User-Agent'),
                        browser=browser,
                        browser_type=browser_type,
                        device=tags.get('device', None),
                        os=tags.get('os', None),
                        user=tags.get('user', None),
                    )
                
                if check_event_is_valid(event_params):
                    event_params_list.append(event_params)
            
            if event_params_list:
                # Only create issue if it has some valid events
                issue_instance = Sentry404Issue.objects.create(**issue_params)
                Sentry404Event.objects.bulk_create(
                    [Sentry404Event(issue=issue_instance, **params) for params in event_params_list]
                )
