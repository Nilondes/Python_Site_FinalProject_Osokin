from django.test import TestCase
from app.models import Ad, Order, Transaction, AdComments, Category
from django.contrib.auth.models import User
from app.views import (create_ad,
                       pending_ads,
                       pending_comments,
                       approve_ad,
                       approve_comment,
                       view_user_ads,
                       remove_ad,
                       edit_ad,
                       search_ads,
                       view_ad,
                       order_ad)
from django.urls import reverse
import os


image_path = 'media/products/' + os.listdir('media/products/')[0]

class CreateAdTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.user.save()
        login = self.client.login(username='test_user', password='12345')
        self.cat = Category.objects.create(name='test_category')

    def test_ad_creation(self):
        with open(image_path, 'rb') as fp:
            resp = self.client.post(reverse('create_ad'), {'name': 'Test Ad',
                                                           'description': 'test description',
                                                           'price': 10.12,
                                                           'category': [str(self.cat.pk)],
                                                           'location': 'London',
                                                           'start_date': '2024-01-01',
                                                           'end_date': '2024-02-01',
                                                           'phone': '123456789',
                                                           'image': fp,
                                                           })
        ad = Ad.objects.get(name='Test Ad')
        self.assertEqual(ad.name, 'Test Ad')
        self.assertRedirects(resp, reverse('home'))


class PendingAdsCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_user', password='12345')
        user.is_staff = True
        user.save()
        login = self.client.login(username='test_user', password='12345')
        self.cat = Category.objects.create(name='test_category')

        self.ad = Ad.objects.create(name='Test Ad',
                                 description='test_description',
                                 price=10,
                                 image='path',
                                 location='test location',
                                 start_date='2024-01-01',
                                 end_date='2024-02-01',
                                 user=user,
                                 phone='123456789'
                                 )

        self.ad.category.set([self.cat.pk])


    def test_pending_ads_list(self):
        resp = self.client.get(reverse('pending_ads'))
        self.assertEqual(resp.status_code, 200)

    def test_approve_ad(self):
        resp = self.client.get(reverse('approve_ad', kwargs={'pk': self.ad.pk}))
        approved_ad = Ad.objects.get(pk=self.ad.pk)
        self.assertTrue(approved_ad.is_approved)
        self.assertRedirects(resp, reverse('pending_ads'))


class PendingCommentsCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_user', password='12345')
        user.is_staff = True
        user.save()
        login = self.client.login(username='test_user', password='12345')
        self.cat = Category.objects.create(name='test_category')
        self.ad = Ad.objects.create(name='Test Ad',
                                 description='test_description',
                                 price=10,
                                 image='path',
                                 location='test location',
                                 start_date='2024-01-01',
                                 end_date='2024-02-01',
                                 user=user,
                                 phone='123456789'
                                 )
        self.ad.category.set([self.cat.pk])
        self.comm = AdComments.objects.create(user=user,
                                         ad=self.ad,
                                         comment='test comment',
                                         )

    def test_pending_comments_list(self):
        resp = self.client.get(reverse('pending_comments'))
        self.assertEqual(resp.status_code, 200)

    def test_approve_comment(self):
        resp = self.client.get(reverse('approve_comment', kwargs={'pk': self.comm.pk}))
        approved_comm = AdComments.objects.get(pk=self.comm.pk)
        self.assertTrue(approved_comm.is_approved)
        self.assertRedirects(resp, reverse('pending_comments'))


class UserAdsCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.user.save()
        self.client.login(username='test_user', password='12345')
        self.cat = Category.objects.create(name='test_category')
        self.ad = Ad.objects.create(name='Test Ad',
                                 description='test_description',
                                 price=10,
                                 image='path',
                                 location='test location',
                                 start_date='2024-01-01',
                                 end_date='2024-02-01',
                                 user=self.user,
                                 phone='123456789'
                                 )
        self.ad.category.set([self.cat.pk])

    def test_user_ads_list(self):
        resp = self.client.get(reverse('user_ads'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_ad(self):
        resp_1 = self.client.get(reverse('edit_ad', kwargs={'pk': self.ad.pk}))
        self.assertEqual(resp_1.status_code, 200)
        with open(image_path, 'rb') as fp:
            resp_2 = self.client.post(reverse('edit_ad', kwargs={'pk': self.ad.pk}), {'name': self.ad.name,
                                                           'description': 'new description',
                                                           'price': 15,
                                                           'category': [str(self.cat.pk)],
                                                           'location': 'London',
                                                           'start_date': '2024-01-01',
                                                           'end_date': '2024-02-01',
                                                           'phone': '123456789',
                                                           'image': fp,
                                                           })
        ad = Ad.objects.get(pk=self.ad.pk)
        self.assertEqual(ad.description, 'new description')
        self.assertRedirects(resp_2, reverse('user_ads'))

    def test_remove_ad(self):
        resp = self.client.get(reverse('remove_ad', kwargs={'pk': self.ad.pk}))
        with self.assertRaises(Exception):
            Ad.objects.get(pk=self.ad.pk)
        self.assertRedirects(resp, reverse('user_ads'))


class SearchAdsCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.user.save()
        login = self.client.login(username=self.user, password='12345')
        self.cat = Category.objects.create(name='test_category')

        self.ad1 = Ad.objects.create(name='First Ad',
                                 description='test_description',
                                 price=10,
                                 image='path',
                                 location='test location',
                                 start_date='2024-01-01',
                                 end_date='2024-02-01',
                                 user=self.user,
                                 phone='123456789',
                                 is_approved=True
                                 )
        self.ad2 = Ad.objects.create(name='Second Ad',
                                    description='test_description',
                                    price=15,
                                    image='path',
                                    location='test location',
                                    start_date='2024-01-01',
                                    end_date='2024-02-01',
                                    user=self.user,
                                    phone='123456789'
                                    )

        self.ad1.category.set([self.cat.pk])
        self.ad2.category.set([self.cat.pk])

    def test_ads_list(self):
        resp_1 = self.client.get(reverse('search_ads'))
        self.assertEqual(resp_1.status_code, 200)
        resp_2 = self.client.post(reverse('search_ads'), {'min_price': 9})
        self.assertEqual(resp_2.status_code, 200)

    def test_view_ad(self):
        resp = self.client.get(reverse('view_ad', kwargs={'pk': self.ad1.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_post_comment(self):
        resp = self.client.post(reverse('view_ad', kwargs={'pk': self.ad1.pk}), {'comment': 'test comment'})
        comm = AdComments.objects.get(user=self.user)
        self.assertEqual(comm.comment, 'test comment')
        self.assertRedirects(resp, reverse('view_ad', kwargs={'pk': self.ad1.pk}))

    def test_order_ad(self):
        resp_1 = self.client.get(reverse('order_ad', kwargs={'pk': self.ad1.pk}))
        self.assertEqual(resp_1.status_code, 200)
        resp_2 = self.client.post(reverse('order_ad',kwargs={'pk': self.ad1.pk}), {'start_date': '2024-01-05',
                                                              'end_date': '2024-01-10',
                                                              'quantity': 5,
                                                              'comment': 'test comment'})
        self.assertRedirects(resp_2, reverse('view_ad', kwargs={'pk': self.ad1.pk}))
        order = Order.objects.get(user=self.user)
        transaction = Transaction.objects.get(user=self.user)
        self.assertEqual(order.comment, 'test comment')
        self.assertEqual(transaction.total_price, 50)
