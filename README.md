django-link-report
==========================

[![Build Status](https://travis-ci.org/mtchavez/python-package-boilerplate.png?branch=master)](https://travis-ci.org/mtchavez/python-package-boilerplate)

Extracts Django 404 reports from Sentry and displays them in a form that helps an admin prioritise and create redirects where appropriate. Has a list of built-in ignores for common crawlers and script-kiddie requests.

## Installation

Assumes Django 1.8+ and Raven are installed. The only other requirement is the requests library. If you install via pip then setup.py should handle this for you

## Warning

Normal installation via pip is untested. We install via pip -e [github repo url] which does work. If someone wants to test and fix setup.py then pull requests are welcome.

After installing to your virtualenv, add the settings below and add link_report to installed apps. You'll need to also ensure contrib.redirects is active.

I'm working on a nice dashboard module for djano admin tools but in the meantime I just have:

    self.children.append(modules.ModelList(
        _('Link Report'),
        models=(
            'link_report.models.RedirectFacade',
            'link_report.models.Sentry404Issue',
        ),
    ))
    
If you're not using django admin tools then do whatever archaic thing people do with their Django admin index screen nowadays.

RedirectFacade is just a thin wrapper around contrib.redirect.Redirect to allow us to hide site and old_path fields, so it's simpler and suited specifically to the task at hand

## Example Settings

    LINK_REPORT_SENTRY_AUTH_TOKEN = "45g34tgerg345g3tgdgfheghdfghdgfhgrtg3455454g345g345gdfg"
    LINK_REPORT_BASE_URL = 'http://www.acme.com/'
    LINK_REPORT_SENTRY_API_BASE_URL = 'http://sentry.agency.com/api/0/'
    LINK_REPORT_SENTRY_ORGANIZATION_SLUG = 'agency'
    LINK_REPORT_SENTRY_PROJECT_SLUG = 'acme'
