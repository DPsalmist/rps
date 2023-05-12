from django.urls import path
from .views import check_level, get_wallet

urlpatterns = [
    path('', get_wallet , name='my-wallet'),
    path('check_level/', check_level, name='check-level'),
]