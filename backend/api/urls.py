from django.urls import path, include
from . import views

urlpatterns = [
    path('users/', views.create_user, name='create_user'),
    path('login/', views.custom_obtain_auth_token, name='login'),
    path('accounts/', views.create_account, name='create_account'),
    path('get_accounts/', views.account_list, name='account_list'),
    path('get_accounts_by_id/', views.get_accounts_by_id, name='get_accounts_by_id'),
    path('banks/', views.banks_list, name='banks_list'),
    path('add_balance/', views.add_balance, name='add_balance'),
    path('subtract_balance/', views.subtract_balance, name='subtract_balance'),
    path('get_balance_by_account/', views.get_balance_by_account, name='get_balance_by_account'),
    path('get_activity_by_user/', views.get_activity_by_user, name='get_activity_by_user'),
]

