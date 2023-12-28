from django.urls import path
from .views import *


urlpatterns = [
    path('user_list', UserListView.as_view(), name='user_list'),
    path('block_user/<int:user_id>/', BlockUser.as_view(), name='block-user'),
    path('unblock_user/<int:user_id>/', UnBlockUser.as_view(), name='block-user'),

    path('chefs_list', ChefsListView.as_view(), name='chefs_list'),
    path('total_revenue', TotalRevenueView.as_view(), name='total_revenue'),
    path('all_transactions/', AllTransactionsView.as_view(), name='all_transactions'),
    path('all_categories/', AllCategoriesView.as_view(), name='all_categories'),

]