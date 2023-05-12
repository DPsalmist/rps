from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile

User = get_user_model() 


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'any_referral_code', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        referral_code = cleaned_data.get('any_referral_code')
        if referral_code:
            try:
                referral = User.objects.get(referral_code=referral_code)
            except User.DoesNotExist:
                raise forms.ValidationError('Invalid referral code')
            else:
                cleaned_data['referred_by'] = referral
                print(f'cleaned_data of user that exist {cleaned_data}')
        return cleaned_data


class UserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')



class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['first_name', 'last_name', 'image', 'bio','banner_image', 'gender', 'dob', 'phone_no', 'address', 'lga', 'state', 'nationality']


