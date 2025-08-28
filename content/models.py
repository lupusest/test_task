from django.db import models
from model_utils.managers import InheritanceManager

class Content(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    counter = models.PositiveIntegerField(default=0, verbose_name="Счетчик просмотров")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # ДОБАВЬТЕ ЭТУ СТРОКУ
    objects = InheritanceManager()

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Video(Content):
    video_file_url = models.URLField(max_length=500, verbose_name="Ссылка на видеофайл")
    subtitles_file_url = models.URLField(max_length=500, verbose_name="Ссылка на субтитры")

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

class Audio(Content):
    text_content = models.TextField(verbose_name="Текст", blank=True)

    class Meta:
        verbose_name = "Аудио"
        verbose_name_plural = "Аудио"
