from pprint import pprint

import requests
from django.utils.dateparse import parse_datetime
from .link_report_settings import API_BASE_URL, PROJECT_SLUG, AUTH_TOKEN, ORGANIZATION_SLUG
from .models import Sentry404Event, Sentry404Issue


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
    
    url = u'{}projects/{}/{}/issues/?query={}&sort=date&limit={}'.format(
        API_BASE_URL,
        ORGANIZATION_SLUG,
        PROJECT_SLUG,
        'logger:http404',
        200,
    )
    headers = {'Authorization': 'Bearer ' + AUTH_TOKEN}
    issues_response = requests.get(url, headers=headers)
    issues = issues_response.json()
    issues = sorted(issues, key=lambda k: k['lastSeen'])
    next_page_url = issues_response.headers['Link'].split(',')[1].split(';')[0][2:-1]
    
    for issue in issues:
        
        url = u'{}issues/{}/events/'.format(
            API_BASE_URL,
            issue['id']
        )
        
        headers = {'Authorization': 'Bearer ' + AUTH_TOKEN}
        events_response = requests.get(url, headers=headers)
        events = events_response.json()
        
        issue_instance = Sentry404Issue.objects.create(
            sentry_id=issue['id'],
            url=issue['culprit'],
            first_seen=parse_datetime(issue['firstSeen']),
            last_seen=parse_datetime(issue['lastSeen']),
            # count=issue['count'],
        )
        
        for event in events:
            tags = {x['key']: x['value'] for x in event['tags']}
            browser = tags.get('browser', None)
            for entry in event['entries']:
                if entry['data'].get('headers', False):
                    headers = {x[0]: x[1] for x in entry['data']['headers']}
                    referer = headers.get('Referer', None)
                    break
            else:
                referer = None
            if browser:
                parts = browser.split()
                if len(parts) > 1:
                    browser_type = u' '.join(parts[:-1])
                else:
                    browser_type = parts[0]
            else:
                browser_type = None
            
            Sentry404Event.objects.create(
                
                issue=issue_instance,
                
                date_created=parse_datetime(event.get('dateCreated')),
                sentry_id=event['id'],
                
                referer=referer,
                referer_domain=referer.split('/')[2] if referer else None,
                user_agent=headers.get('User-Agent'),
                
                browser=browser,
                browser_type=browser_type,
                device=tags.get('device', None),
                os=tags.get('os', None),
                user=tags.get('user', None),
            )
