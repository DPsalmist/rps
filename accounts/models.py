from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.contrib.auth.models import User
from .managers import CustomUserManager
from django.core.validators import RegexValidator
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode
from PIL import Image
# Create your models here.

phone_regex = RegexValidator(regex=r"^[0]\d{10}$", message="must be a valid phone number")

class CustomUser(AbstractUser):
	username = models.CharField(max_length=20, null=False, unique=True, error_messages={
            'unique': 'A user with that username already exists.'},)
	email = models.EmailField(unique=True)
	referral_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
	referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
	any_referral_code = models.CharField(max_length=7, null=True, blank=True)
	is_online = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	#objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.username

	def get_referral_link(self):
		if self.referral_code:
			return reverse('signup', kwargs={'referral_code': self.referral_code})
			# url = reverse('signup')
			#params = urlencode({'referral_code': self.referral_code})
			#return f"{url}?{params}"
		else:
			return reverse('signup')

	

class Profile(models.Model):
	gender = (
			('Select Gender', 'Select Gender'),
			('Male','Male'),
			('Female','Female'),
		)
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	banner_image = models.ImageField(default='profile-bg.jpg', upload_to='banner_pics', null=True)
	bio = models.CharField(max_length=60, blank=True, null=True)
	first_name = models.CharField(max_length=60, blank=True, null=True)
	last_name = models.CharField(max_length=60, blank=True, null=True)
	image = models.ImageField(default='default.jpeg', upload_to='profile_pics', null=True)
	gender = models.CharField(max_length=30, choices=gender, default='Select Gender')
	dob = models.DateField(null=True)
	phone_no = models.CharField(unique=True, null=True, validators=[phone_regex], max_length=11)
	address = models.TextField(max_length=150, null=True)
	lga = models.CharField(max_length=30, null=True)
	state = models.CharField(max_length=30, null=True)
	nationality = models.CharField(max_length=30, default='Nigerian')


	def __str__(self): 	
		return f'{self.user.username} profile'

	#To resize the image though the save method exist in the parent class, we'll create ours.
	#In order to override the default save, you'll have to use *args & *kwargs	
	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def get_followers(self):
    	return self.follower

    def __str__(self):
    	return str(self.follower)

    # def __str__(self):
    # 	return f'Followers of {self.followed} include {self.follower}'

			