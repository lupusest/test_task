from celery import shared_task
from django.db.models import F
from .models import Content

@shared_task
def increment_content_counters(content_ids):
    if content_ids:
        Content.objects.filter(id__in=content_ids).update(counter=F('counter') + 1)
