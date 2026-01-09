import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

broker_transport_options = {
    "visibility_timeout": 3600,
    "retry_on_timeout": True,
    "socket_keepalive": True,
}