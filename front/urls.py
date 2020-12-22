from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('accounts/<str:username>', views.accounts, name='accounts'),
    path('transactions/own/<str:username>',
         views.own_transactions, name='own_transactions'),
    path('transactions/third/<str:username>', views.third_transactions,
         name='third_transactions'),
    path('payments/<str:username>', views.payments, name='payments'),
    path('checks/<str:username>', views.checks, name='checks'),
    path('loans/<str:username>', views.loans, name='loans'),
    path('states/<str:username>', views.states, name='states'),
    path('spreads/<str:username>', views.spreads, name='spreads')
]
