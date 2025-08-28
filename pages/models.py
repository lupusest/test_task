from django.db import models
from content.models import Content

class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок страницы")
    content = models.ManyToManyField(
        Content,
        through='PageContent',
        related_name='pages',
        verbose_name="Контент"
    )

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['title']

    def __str__(self):
        return self.title

class PageContent(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['order']
