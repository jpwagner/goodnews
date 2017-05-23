from django.test import TestCase
from django.core.urlresolvers import reverse

from goodnews.models import Article


class ArticleListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Article.objects.create(url='http://www.google.com', title='Google')

    def test_view_url_exists_at_desired_location(self): 
        resp = self.client.get('/') 
        self.assertEqual(resp.status_code, 200)  

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'home.html')
