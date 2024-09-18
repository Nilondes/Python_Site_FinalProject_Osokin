from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ManyToManyField('Category')
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    comment = models.TextField()
    quantity = models.IntegerField()


    def __str__(self):
        return f'{self.user} - {self.ad}'


class Transaction(models.Model):
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
