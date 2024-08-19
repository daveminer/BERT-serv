import json
import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.http import HttpResponse
from sentiment.views import SentimentCreate

class SentimentCreateTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = SentimentCreate.as_view()

    @patch('sentiment.tasks.run_sentiment.s')
    @patch('sentiment.tasks.send_webhook.s')
    def test_post_with_callback_url(self, mock_send_webhook, mock_run_sentiment):

        request_body = json.dumps([
            {'article_id': 1, 'tags': ['news'], 'text': 'Some content here'},
            {'article_id': 2, 'tags': ['sports'], 'text': 'Another content'}
        ])
        request = self.factory.post('/sentiment/new?callback_url=http://example.com/callback', request_body, content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        mock_run_sentiment.assert_called_once_with(
            [(1, ['news'], 'Some content here'), (2, ['sports'], 'Another content')]
        )
        mock_send_webhook.assert_called_once_with('http://example.com/callback')

    @patch('sentiment.tasks.run_sentiment.s')
    def test_post_without_callback_url(self, mock_run_sentiment):
        request_body = json.dumps([
            {'article_id': 1, 'tags': ['news'], 'text': 'Some content here'},
            {'article_id': 2, 'tags': ['sports'], 'text': 'Another content'}
        ])
        request = self.factory.post('/sentiment/new', request_body, content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        mock_run_sentiment.assert_called_once_with(
            [(1, ['news'], 'Some content here'), (2, ['sports'], 'Another content')]
        )