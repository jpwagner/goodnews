from django.test import TestCase

from goodnews.models import Article


class ArticleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Article.objects.create(url='http://www.google.com', title='Google')

    def test_title_label(self):
        article = Article.objects.get(id=1)
        field_label = article._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')
