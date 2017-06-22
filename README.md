django-link-report
==========================

[![Build Status](https://travis-ci.org/mtchavez/python-package-boilerplate.png?branch=master)](https://travis-ci.org/mtchavez/python-package-boilerplate)

Extracts Django 404 reports from Sentry and displays them in a form that helps an admin prioritise and create redirects where appropriate. Has a list of built-in ignores for common crawlers and script-kiddie requests.

## Installation

Assumes Django 1.8+ and Raven are installed. Has a built-in admin panel that works with django-admin-tools but can easily be adapted if you don't use that (although you should because it's great). 

The only other requirement is the requests library. If you install via pip then setup.py should handle this for you

## Warning

Normal installation via pip is untested. We install via pip -e [github repo url] which does work. If someone wants to test and fix setup.py then pull requests are welcome.

Just install normally

## Example Settings

    LINK_REPORT_SENTRY_AUTH_TOKEN = "45g34tgerg345g3tgdgfheghdfghdgfhgrtg3455454g345g345gdfg"
    LINK_REPORT_BASE_URL = 'http://www.acme.com/'
    LINK_REPORT_SENTRY_API_BASE_URL = 'http://sentry.agency.com/api/0/'
    LINK_REPORT_SENTRY_ORGANIZATION_SLUG = 'agency'
    LINK_REPORT_SENTRY_PROJECT_SLUG = 'acme'
