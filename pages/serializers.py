from rest_framework import serializers
from model_utils.managers import InheritanceManager
from .models import Page
from content.models import Content, Video, Audio
from django.urls import reverse

class RelativeHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.pk is None:
            return None
        return reverse(view_name, kwargs={'pk': obj.pk})

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'title', 'counter', 'video_file_url', 'subtitles_file_url')

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ('id', 'title', 'counter', 'text_content')

class ContentPolymorphicSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ('id', 'title', 'counter', 'content_type')

    def get_content_type(self, obj):
        return obj.__class__.__name__.lower()

    def to_representation(self, instance):
        if isinstance(instance, Video):
            return VideoSerializer(instance).data
        elif isinstance(instance, Audio):
            return AudioSerializer(instance).data
        return super().to_representation(instance)

class PageListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='page-detail', lookup_field='pk')

    class Meta:
        model = Page
        fields = ('id', 'title', 'url')

class PageDetailSerializer(serializers.ModelSerializer):
    content_list = serializers.SerializerMethodField()
    class Meta:
        model = Page
        fields = ('id', 'title', 'content_list')

    def get_content_list(self, obj):
        ordered_content_ids = list(obj.pagecontent_set.order_by('order').values_list('content_id', flat=True))
        content_subclasses = list(Content.objects.filter(id__in=ordered_content_ids).select_subclasses())
        content_map = {content.id: content for content in content_subclasses}
        sorted_content = [content_map[id] for id in ordered_content_ids if id in content_map]
        return ContentPolymorphicSerializer(sorted_content, many=True).data
