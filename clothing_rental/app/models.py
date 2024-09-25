from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class AdManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(user=user)


class Ad(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    image = models.ImageField(upload_to='products/')
    category = models.ManyToManyField('Category')
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    objects = AdManager()

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
    quantity = models.IntegerField(validators=[MinValueValidator(1)])


    def __str__(self):
        return f'{self.user} - {self.ad}'


class Transaction(models.Model):
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.date} - {self.order}'


class AdComments(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.created_at} - {self.ad}'
