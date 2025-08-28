import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

from pages.models import Page, PageContent
from content.models import Video, Audio

class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to seed the database...'))

        # 1. Создание суперпользователя admin/admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" with password "admin" created.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists.'))

        # 2. Очистка старых данных (опционально, но удобно для тестов)
        Page.objects.all().delete()
        Video.objects.all().delete()
        Audio.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Old data cleared.'))

        fake = Faker('ru_RU')

        # 3. Создание объектов контента
        videos = []
        for i in range(5):
            video = Video.objects.create(
                title=f'Видеоролик "{fake.catch_phrase()}"',
                video_file_url=f'https://example.com/video_{i+1}.mp4',
                subtitles_file_url=f'https://example.com/subs_{i+1}.srt'
            )
            videos.append(video)

        audios = []
        for i in range(5):
            audio = Audio.objects.create(
                title=f'Аудиодорожка "{fake.bs()}"',
                text_content='\n'.join(fake.paragraphs(nb=3))
            )
            audios.append(audio)
            
        self.stdout.write(self.style.SUCCESS(f'Created {len(videos)} videos and {len(audios)} audios.'))
        
        all_content = videos + audios

        # 4. Создание 15 страниц для демонстрации пагинации
        for i in range(15):
            page = Page.objects.create(title=f'Страница новостей №{i+1}')
            
            # Привязка случайного количества контента (от 1 до 4)
            content_to_add = random.sample(all_content, k=random.randint(1, 4))
            
            for order, content_item in enumerate(content_to_add):
                PageContent.objects.create(
                    page=page,
                    content=content_item,
                    order=order
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded 15 pages with related content.'))
