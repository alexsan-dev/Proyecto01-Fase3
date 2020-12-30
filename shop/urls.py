from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='shop_login'),
    path('store/', views.store, name='shop_store')
]
