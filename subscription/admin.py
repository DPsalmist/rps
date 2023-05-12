from django.contrib import admin
from .models import SubscriptionPlan, Member

# Register your models here.

@admin.register(SubscriptionPlan)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'description', 'price', 'duration')
	list_filter = ('name', 'price')
	search_fields = ('name',)


@admin.register(Member)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ( 'user','subscription_plan', 'subscription_start_date', 'subscription_end_date')
	list_filter = ('subscription_plan', 'subscription_start_date', 'subscription_end_date')
	search_fields = ('subscription_plan',)


