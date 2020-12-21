from django.urls import path

from . import views

urlpatterns = [
    path('accounts/', views.accounts, name='admin_accounts'),
    path('signing/', views.signing, name='admin_signing'),
    path('business_signing/', views.business_signing,
         name='admin_business_signing')
]
