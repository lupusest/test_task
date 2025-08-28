from django.contrib import admin
from .models import Video, Audio

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'counter', 'created_at')
    search_fields = ('title__startswith',)
    readonly_fields = ('counter',)

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'counter', 'created_at')
    search_fields = ('title__startswith',)
    readonly_fields = ('counter',)
