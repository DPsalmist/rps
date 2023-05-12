from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Member, SubscriptionPlan
from django.utils import timezone

User = get_user_model()


''
@receiver(post_save, sender=User)
def set_free_membership(sender, instance, created, **kwargs):
    if created:
        print(f'created successfully with id {created}')
        free_plan = SubscriptionPlan.objects.get(name='Free')
        print(f'assigned plan is {free_plan}')
        free_member = Member.objects.create(
            user=instance, subscription_plan=free_plan,
            subscription_start_date=timezone.now(),
            subscription_end_date=timezone.now() + timezone.timedelta(days=free_plan.duration))
        free_member.save()

        print(f'free_membership for {instance} => {free_member}')
        instance.save()
