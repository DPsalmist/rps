from django.urls import path
from .views import subscribe, subscribtion_succes, cancel_subscription, update_subscription


urlpatterns = [
	path('subscribe/', subscribe, name='subscribe'),
	path('summary/', subscribtion_succes, name='subscription-success'),
	path('subscribtion-cancelled/', cancel_subscription, name='cancel-subscribtion'),
	path('subscribtion-updated/', update_subscription, name='update-subscribtion'),
]