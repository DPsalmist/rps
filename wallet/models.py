from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model() 


# Create your models here.
class Wallet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_wallet')
	balance = models.FloatField(default=0.0)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.balance)


class GPoint(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_points')
	quantity = models.FloatField()
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.quantity)

