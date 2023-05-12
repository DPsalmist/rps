from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile
from .utils import generate_referral_code

User = get_user_model()

#We want a user profile to be created for each new user rather than going through the admin
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

	print('its created:', created)

#saves the new user profile
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()


# saves a referral code for the new user
@receiver(post_save, sender=User)
def add_referral_code(sender, instance, created, **kwargs):
    if created:
        referral_code = generate_referral_code()
        instance.referral_code = referral_code
        instance.save()


'''
@receiver(pre_save, sender=User)
def set_referred_by(sender, instance, created, **kwargs):
    if created and instance.referral_code:
        try:
            referred_by = User.objects.get(referral_code=instance.referral_code)
            referred_by.referred_by = instance
            referred_by.save()
        except User.DoesNotExist:
            pass
            print('The user is not found!')
'''

@receiver(pre_save, sender=User)
def set_referred_by(sender, instance, **kwargs):
    if not instance.pk: # user is being created, not updated
        referral_code = instance.referral_code
        if referral_code:
            try:
                referred_by_user = User.objects.get(referral_code=referral_code)
                instance.referred_by = referred_by_user
            except User.DoesNotExist:
                pass
                print('The user is not found!')
