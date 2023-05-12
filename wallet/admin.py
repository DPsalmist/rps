from django.contrib import admin
from .models import Wallet

# Register your models here.
@admin.register(Wallet)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'balance', 'date_created')
	list_filter = ('user',)
	search_fields = ('user',)
	ordering = ('-balance',)
