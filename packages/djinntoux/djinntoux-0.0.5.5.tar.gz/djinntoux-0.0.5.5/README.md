# djinntoux 🐧
Generic reusable bits for Django projects

## Disclaimer
This package is only intended for my own personal use, install at your own risk

## Rebuild
Assumes `twine` is installed and an API token is stored in a `.pypirc` file:

```bash
rm -rfv dist/ && python -m build && twine upload --verbose dist/*
```

## Installation
```bash
pip install djinntoux
```

## Usage

### Environment Variables
The following are expected to be set in your environment, a `.env` file, or a `.envrc` file:
```bash
DATABASE_URL            # no default
DJANGO_SECRET_KEY       # no default
DJANGO_DEBUG            # defaults to false
DJANGO_ENV_NAME         # defaults to prod
DJANGO_ADMIN_HEADER_BG  # defaults to red
```

### dproj

#### settings_reuse
In your own project settings, use like so:
```python
from djinntoux.dproj.settings_reuse import *  # noqa

...

INSTALLED_APPS = BASE_APPS + []
```

This reusable settings module expects `DJANGO_SECRET_KEY` to be set in your environment. For example, if you are just running your project locally, you could use an `.envrc` file for your development environment ...
```bash
...
export 'DJANGO_SECRET_KEY'='django-insecure-321-do-not-use-this!!!'
...
```
... and then use a `systemd` unit file for a mock production environment ...
```ini
...
[Service]
Environment='DJANGO_SECRET_KEY'='django-insecure-321-do-not-use-this!!!'
...
```

#### urls_reuse
In your project root URLconf, use like so:
```python
urlpatterns = [
    path('', include('djinntoux.dproj.urls_reuse')),
    ...
]
```

### Abstract Models
https://github.com/venteto/djinntoux/blob/main/djinntoux/abstract/ab_mod.py

As an example in a `models.py` file:

```python
from djinntoux.abstract.ab_mod import EditLink, Timestamps, UUIDpk7

...

class Account(Timestamps, EditLink):
```

#### EditLink
Set `ADMIN_PATH` in project settings (do not add a leading slash), e.g. to keep the Django default path without using an environment variable:
```python
ADMIN_PATH = 'admin/'
```

Then in templates you can use like so:
```django
<a target="_blank" href="{{ obj.get_edit_path }}">Edit</a>
```

### Custom Users App
https://github.com/venteto/djinntoux/tree/main/djinntoux/dapp_users

In project settings add `djinntoux.dapp_users` to `INSTALLED_APPS` and set `AUTH_USER_MODEL = 'zy_users.User'`

The `admin.py` file is copied verbatim from [upstream](https://github.com/django/django/tree/main/django/contrib/auth), tweaked to replace the stock `first_name` and `last_name` conventions from with slightly more international options, lightly inspired by the [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django/blob/master/{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/users/models.py#L27) project. The custom user model also includes a new timezone field.

### Renames
https://github.com/venteto/djinntoux/blob/main/djinntoux/dproj/rename.py

In project settings make sure `INSTALLED_APPS` reflects something akin to this:
```python
    'djinntoux.dproj.rename.ContribAuth',   # replaces 'django.contrib.auth',
    'djinntoux.dproj.rename.ContribSites',  # replaces 'django.contrib.sites',
```

### Scraping
https://github.com/venteto/djinntoux/blob/main/djinntoux/utils/scrape.py

```python
from djinntoux.utils.scrape import get_host_and_title
```

Then use like so:
```python
    def save(self, *args, **kwargs):
        if not self.link_title:
            self.link_title = get_host_and_title(self)[1]
        super(Link, self).save(*args, **kwargs)
```

## TODO (Includes, But Not Limited To)
- dapp_ttags (or make dproj itself an app in addition to a project directory?)
- templates dir (including admin overrides)
- static files? or just link to a pseudo-CDN in base template?
    - compressor?
- robots.txt view
- error views
- favicon view
- aggregation util
- abstract view and admin classes

## See Also
https://github.com/venteto/djinntoux/blob/main/READMORE.md