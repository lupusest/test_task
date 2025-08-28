from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from .models import Page, PageContent

class PageContentInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PageContent
    extra = 1

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title__startswith',)
    inlines = (PageContentInline,)
