from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    description = models.CharField(max_length=256)
    image = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name} - {self.price} lei'


class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


class BankAccount(models.Model):
    iban = models.CharField(max_length=40)
    sum = models.FloatField()

    def __str__(self):
        return self.iban


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    bank_account = models.ForeignKey('BankAccount', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=16)
    date = models.DateTimeField()

    def __str__(self):
        return f'Order {self.pk}: Bank account: {self.bank_account.iban}; Address: {self.address}; ' \
               f'Phone number: {self.phone_number}; Date: {self.date}; Total_cost: {self.total_cost()} lei'

    def total_cost(self):
        return sum([op.product.price for op in OrderProduct.objects.filter(order=self)])

    def list_of_products(self):
        return [op.product for op in OrderProduct.objects.filter(order=self)]


class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.RESTRICT)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT)

    def __str__(self):
        return f'Order {self.order.pk} - {self.product.name}'
