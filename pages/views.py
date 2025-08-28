from rest_framework import generics
from .models import Page
from .serializers import PageListSerializer, PageDetailSerializer
from content.tasks import increment_content_counters

class PageListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer

class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer

    def get_object(self):
        obj = super().get_object()
        content_ids = list(obj.content.values_list('id', flat=True))
        if content_ids:
            increment_content_counters.delay(content_ids)
        return obj
