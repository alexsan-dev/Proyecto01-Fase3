from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('accounts/', views.accounts, name='accounts'),
    path('transactions/own/',
         views.own_transactions, name='own_transactions'),
    path('transactions/third/', views.third_transactions,
         name='third_transactions'),
    path('payments/', views.payments, name='payments'),
    path('checks/', views.checks, name='checks'),
    path('loans/', views.loans, name='loans'),
    path('states/', views.states, name='states'),
    path('spreads/', views.spreads, name='spreads'),
    path('cards/', views.cards, name='cards')
]
