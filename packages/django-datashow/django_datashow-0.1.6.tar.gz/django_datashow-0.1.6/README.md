# django-datashow

A Django app to show SQLite datasets as tables with configurable features:

- column value formatting
- column sorting
- column facets and filters
- searching via SQLite's FTS5
- pagination
- exporting to CSV
- row-level detail view.

This app is designed for read-only (or rarely updated) datasets that you want to publish on the web and where you control and trust the content.

## Installation

```
pip install django-datashow
```

Add `datashow` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'datashow',
    ...
]
```

Hook up the `datashow` URLs in your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('data/', include('datashow.urls')),
    ...
]
```


## Settings

You can configure the following settings in your `settings.py`:

- `DATASHOW_DB_CACHE_PATH`: Path to the SQLite database cache directory. If not set, uses a temporary directory. When the SQLite file needs to be read, it gets copied from your MEDIA storage to this cache path. A new dataset version invalidates the cache.
- `DATASHOW_STORAGE_BACKEND`: The Django storage backend name to use for storing the SQLite files. Default is `"default"`.
