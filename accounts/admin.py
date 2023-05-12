from django.contrib import admin
from .models import Profile, Follow, CustomUser

# Register your models here.
admin.site.register(Follow)
#admin.site.register(CustomUser)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ( 'first_name', 'last_name', 'banner_image', 'gender', 'dob', 'phone_no', \
		'address', 'lga', 'state', 'nationality')
	list_filter = ('lga', 'state')
	search_fields = ('lga',)
	#ordering = ('user',)



@admin.register(CustomUser)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ( 'username', 'email', 'referral_code', 'referred_by', 'is_online', 'is_active', 'date_created')
	list_filter = ('email', 'username', 'referral_code')
	search_fields = ('username', 'referral_code')
	ordering = ('-username',)
