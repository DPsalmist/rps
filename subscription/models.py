from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

User = get_user_model()

# Create your models here.
class SubscriptionPlan(models.Model):
	name = models.CharField(max_length=30, blank=True)
	description = models.CharField(max_length=300, blank=True)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	duration = models.PositiveIntegerField(default=30)

	def __str__(self):
		return self.name

	def get_default_plan():
		default_plan_name = getattr(settings, 'DEFAULT_SUBSCRIPTION_PLAN', 'Free')
		# 	return SubscriptionPlan.objects.get(name='Free')
		try:
			default_plan = SubscriptionPlan.objects.get(name=default_plan_name)
		except SubscriptionPlan.DoesNotExist:
			default_plan = SubscriptionPlan(name=default_plan_name, description='Default plan', duration=30, price=0)
			default_plan.save()
		return default_plan


class Member(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, default='Free')
	subscription_start_date = models.DateTimeField(null=True)
	subscription_end_date = models.DateTimeField(null=True)

	def __str__(self):
		return str(self.subscription_plan)
