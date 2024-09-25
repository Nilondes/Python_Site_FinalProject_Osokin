from django.test import TestCase
from app.models import Ad, Order, Transaction, AdComments, Category
from django.contrib.auth.models import User


class CreateAd(TestCase):
    def test_ad_creation(self):
        user = User.objects.create_user(username='test user')
        ad = Ad.objects.create(name='Test Ad',
                               description='test_description',
                               price=10,
                               image='path',
                               location='test location',
                               start_date='2024-01-01',
                               end_date='2024-02-01',
                               user=user,
                               phone='123456789'
                               )
        self.assertEqual(ad.name, 'Test Ad')


class CreateCategory(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='test category')
        self.assertEqual(category.name, 'test category')


class CreateOrder(TestCase):
    def test_order_creation(self):
        user = User.objects.create_user(username='test user')
        ad = Ad.objects.create(name='Test Ad',
                               description='test_description',
                               price=10,
                               image='path',
                               location='test location',
                               start_date='2024-01-01',
                               end_date='2024-02-01',
                               user=user,
                               phone='123456789'
                               )
        order = Order.objects.create(user=user,
                                     ad=ad,
                                     start_date='2024-01-01',
                                     end_date='2024-02-01',
                                     comment='test comment',
                                     quantity=1
                                     )
        self.assertEqual(order.comment, 'test comment')


class CreateTransaction(TestCase):
    def test_transaction_creation(self):
        user = User.objects.create_user(username='test user')
        ad = Ad.objects.create(name='Test Ad',
                               description='test_description',
                               price=10,
                               image='path',
                               location='test location',
                               start_date='2024-01-01',
                               end_date='2024-02-01',
                               user=user,
                               phone='123456789'
                               )
        order = Order.objects.create(user=user,
                                     ad=ad,
                                     start_date='2024-01-01',
                                     end_date='2024-02-01',
                                     comment='test comment',
                                     quantity=2
                                     )
        transaction = Transaction.objects.create(user=user,
                                                 order=order,
                                                 total_price=order.quantity*ad.price)
        self.assertEqual(transaction.total_price, 20)


class CreateAdComment(TestCase):
    def test_ad_comment_creation(self):
        user = User.objects.create_user(username='test user')
        ad = Ad.objects.create(name='Test Ad',
                               description='test_description',
                               price=10,
                               image='path',
                               location='test location',
                               start_date='2024-01-01',
                               end_date='2024-02-01',
                               user=user,
                               phone='123456789'
                               )
        comm = AdComments.objects.create(user=user,
                                            ad=ad,
                                            comment='test comment',
                                            )
        self.assertEqual(comm.comment, 'test comment')
