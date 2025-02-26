from django.conf import settings

DATASHOW_DB_CACHE_PATH = getattr(settings, "DATASHOW_DB_CACHE_PATH", None)
DATASHOW_STORAGE_BACKEND = getattr(settings, "DATASHOW_STORAGE_BACKEND", "default")
