from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('app', views.main_view, name='main_view'),
    path('product_<int:product_id>', views.product_by_id, name='product_by_id'),
    path('product_<int:product_id>/ok', views.add_to_cart, name='add_to_cart'),
    path('cart', views.show_cart, name='show_cart'),
    path('cart/remove_<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('cart/buy', views.buy, name='buy'),
    path('history', views.history, name='history')
]
