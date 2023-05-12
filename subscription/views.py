from django.shortcuts import render, redirect
from .models import SubscriptionPlan, Member
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import SubscriptionPlanForm
from django.conf import settings

User = get_user_model()

# Create your views here.

@login_required
def subscribe(request):
	current_user = request.user
	if request.method == 'POST':
		form = SubscriptionPlanForm(request.POST)
		if form.is_valid():
			plan_id = form.cleaned_data['subscription_plan']
			#plan_id = request.POST.get('plan_id')
			plan = SubscriptionPlan.objects.get(pk=plan_id.pk)
			#form.save()
			player_membership = Member.objects.filter(user=current_user).first()
			player_membership.subscription_plan = plan
			player_membership.subscription_start_date = timezone.now()
			player_membership.subscription_end_date = timezone.now() + timezone.timedelta(days=plan.duration)


			# create new member instance for the plan
			# member = Member(
			# 	user=current_user,
			# 	subscription_plan=plan,
			# 	subscription_start_date=timezone.now(),
			# 	subscription_end_date=timezone.now() + timezone.timedelta(days=plan.duration)
			# )
			#member.set_password(request.POST.get('password'))
			player_membership.save()
			print(f'new membership => {player_membership}')
			messages.success(request, 'You have successfully subscribed!')
			return redirect('subscription-success')
	else:
		form = SubscriptionPlanForm()
		plan = SubscriptionPlan.objects.all()
	return render(request, 'subscription_form.html', {'plans':plan, 'form':form})

@login_required
def subscribtion_succes(request):
	current_user = request.user
	member = Member.objects.filter(user=current_user).first()
	print(f'members_plan => {member}')
	subscription_start_date = member.subscription_start_date
	subscription_end_date = member.subscription_end_date
	member = member.subscription_plan
	ctx = {
		'subscription_end_date':subscription_end_date,
		'member_plan':member,
		'subscription_start_date':subscription_start_date,
		
	}
	return render(request, 'player_subscription_success.html',ctx)


@login_required
def cancel_subscription(request):
    member = request.user
    default_plan_name = getattr(settings, 'DEFAULT_SUBSCRIPTION_PLAN', 'Free')
    plan = SubscriptionPlan.objects.get(plan=default_plan_name)
    member.subscription_plan = None
    member.subscription_start_date = None
    member.subscription_end_date = None
    member.save()
    return redirect('cancel-subscription')


@login_required
def update_subscription(request):
    member = request.user
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        plan = SubscriptionPlan.objects.get(pk=plan_id)
        member.subscription_plan = plan
        member.subscription_start_date = timezone.now()
        member.subscription_end_date = timezone.now() + timezone.timedelta(days=plan.duration)
        member.save()
        return redirect('subscription_success')
    else:
        plans = SubscriptionPlan.objects.all()
        return render(request, 'update_subscription.html', {'member': member, 'plans': plans})