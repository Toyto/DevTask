from decimal import Decimal

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser, User

from product.models import Product, Comment


class SingleProductTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='Jeans', slug='js',
            description='Nice cloth', price=Decimal(50))
        self.comment = Comment.objects.create(
            product=self.product, text='I just had to comment this product.')
        self.user = User.objects.create_user(
            username='Admin', password='secret')

    def test_page_exists(self):
        """ Test if page showed correctly. """
        response = self.client.get(reverse('single_product', args=(self.product.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)
        self.assertContains(response, self.product.price)

    def test_comment_exists(self):
        """ Test if comments showed correctly. """
        response = self.client.get(reverse('single_product', args=(self.product.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.comment.text)

    def test_commenting(self):
        """ Test commenting from the product page. """
        response = self.client.post(
            reverse('single_product',
            args=(self.product.slug,)), 
            {'text': 'New Comment', 'product_slug': self.product.slug})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('single_product', args=(self.product.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Comment')

    def test_like(self):
        """ Test likes engine. """
        self.product.likes.add(self.user)
        response = self.client.get(reverse('single_product', args=(self.product.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Likes: 1')
