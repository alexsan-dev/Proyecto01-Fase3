from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signing/', views.signing, name='signing'),
    path('signing/business/', views.business_signing, name='business_signing'),
    path('accounts/', views.accounts, name='accounts'),
    path('admin/', views.admin, name='admin')
]
