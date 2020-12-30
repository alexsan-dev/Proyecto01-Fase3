from django.urls import path

from . import views

urlpatterns = [
    path('accounts/', views.accounts, name='admin_accounts'),
    path('signing/', views.signing, name='admin_signing'),
    path('checks/change/', views.change_checks, name='admin_change_checks'),
    path('deposits/', views.deposits, name='admin_deposits'),
    path('checks/', views.checks, name='admin_checks'),
    path('loans/', views.loans, name='admin_loans'),
    path('cards/', views.cards, name='admin_cards'),
    path('business_signing/', views.business_signing,
         name='admin_business_signing')
]
