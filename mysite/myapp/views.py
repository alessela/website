from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
import datetime

user = None


def login(request):
    global user
    user = None
    return render(request, 'login.html')


def main_view(request):
    global user
    if request.method != 'POST':
        return render(request, 'main_page.html', {'products': Product.objects.all(), 'user': user})
    if not User.objects.filter(username=request.POST['username'], password=request.POST['password']).exists():
        return render(request, 'login.html', {'msg': 'Incorrect username or passowrd'})
    user = User.objects.get(username=request.POST['username'], password=request.POST['password'])
    return render(request, 'main_page.html', {'products': Product.objects.all(), 'user': user})


def product_by_id(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product_details.html', {'product': product, 'user': user})


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    CartProduct.objects.create(user=user, product=product)
    return render(request, 'product_details.html',
                  {'product': product, 'user': user, 'msg': 'Command added successfully'})


def total_value_for_cart():
    return sum([cp.product.price for cp in CartProduct.objects.filter(user=user)])


def show_cart(request):
    if CartProduct.objects.filter(user=user).exists() is False:
        return render(request, 'empty_cart.html', {'user': user, 'msg': 'Your cart is empty. Go back to the main page'})
    return render(request, 'cart.html', {'user': user,
                                         'total_sum': total_value_for_cart(),
                                         'products': CartProduct.objects.filter(user=user)})


def remove_from_cart(request, product_id):
    CartProduct.objects.filter(pk=product_id).delete()
    return show_cart(request)


def buy(request):
    if request.method != 'POST':
        return main_view(request)
    if not BankAccount.objects.filter(iban=request.POST['iban']).exists():
        return render(request, 'cart.html', {'user': user,
                                             'total_sum': total_value_for_cart(),
                                             'products': CartProduct.objects.filter(user=user),
                                             'msg': 'Invalid IBAN!'})
    account = BankAccount.objects.get(iban=request.POST['iban'])
    if account.sum < total_value_for_cart():
        return render(request, 'cart.html', {'user': user,
                                             'total_sum': total_value_for_cart(),
                                             'products': CartProduct.objects.filter(user=user),
                                             'msg': 'Not enough money!'})
    account.sum -= total_value_for_cart()
    account.save()
    order = Order.objects.create(user=user, bank_account=account, address=request.POST['address'],
                                 phone_number=request.POST['phone_number'], date=datetime.datetime.now())
    for cp in CartProduct.objects.filter(user=user):
        OrderProduct.objects.create(order=order, product=cp.product)
    CartProduct.objects.filter(user=user).delete()
    return render(request, 'empty_cart.html', {'user': user, 'msg': 'Order made successfully! Continue shoping!'})


def history(request):
    return render(request, 'history.html', {'user': user,
                                            'orders': reversed(Order.objects.filter(user=user))})
