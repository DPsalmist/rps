from django import forms
from django.contrib.auth import get_user_model
from .models import SubscriptionPlan, Member

User = get_user_model()



class SubscriptionPlanForm(forms.Form):
	subscription_plan = forms.ModelChoiceField(queryset=SubscriptionPlan.objects.all(), 
		widget=forms.Select(attrs={'class': 'form-select'}))
	