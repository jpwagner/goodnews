from django.test import TestCase
from django.core.urlresolvers import reverse

from goodnews.models import Article


class ArticleAPITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Article.objects.create(url='http://www.google.com', title='Google')

    def test_view_url_exists_at_desired_location(self): 
        resp = self.client.get('/api/v1.0/article/') 
        self.assertEqual(resp.status_code, 200)  
