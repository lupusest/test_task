from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from pages.models import Page, PageContent
from content.models import Video, Audio

class PageAPITests(APITestCase):
    def setUp(self):
        self.page1 = Page.objects.create(title="Test Page 1")
        self.page2 = Page.objects.create(title="Test Page 2")
        self.video1 = Video.objects.create(
            title="Test Video",
            video_file_url="http://example.com/video.mp4",
            subtitles_file_url="http://example.com/subs.srt"
        )
        self.audio1 = Audio.objects.create(
            title="Test Audio", 
            text_content="Это тестовый текст для аудио."
        )
        PageContent.objects.create(page=self.page1, content=self.video1, order=0)
        PageContent.objects.create(page=self.page1, content=self.audio1, order=1)

    def test_get_page_list(self):
        url = reverse('page-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Page.objects.count()) 
        self.assertLessEqual(len(response.data['results']), 10)
        self.assertIn('url', response.data['results'][0])

    @patch('content.tasks.increment_content_counters.delay')
    def test_get_page_detail_and_task_call(self, mock_task):
        url = reverse('page-detail', kwargs={'pk': self.page1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.page1.title)
        self.assertEqual(len(response.data['content_list']), 2)
        self.assertIn('video_file_url', response.data['content_list'][0])
        self.assertIn('text_content', response.data['content_list'][1])
        mock_task.assert_called_once()
        called_with_ids = mock_task.call_args[0][0]
        self.assertCountEqual(called_with_ids, [self.video1.id, self.audio1.id])
