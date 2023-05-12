from django.shortcuts import render
from console.models import RPS_Score
from django.contrib.auth import get_user_model
from console.game_logic import calc_wallet
from .models import Wallet

User = get_user_model()

# Create your views here.

'''
Level 1: 
	gpts is wins/2 === wallet_balance
	games_played >= 0 and <= 5000 
	win_percentage >= 0 and <= 50 
Level 2: 
	gpts is == wins === wallet_balance
	games_payed >= 5000 and <= 100000
	win_percentage >= 50 and <= 70
Level 3: 
	gpts is wins * 2 === wallet_balance
	games_payed >= 10000
	win_percentage >= 70
'''

def get_wallet(request):
	current_user = request.user
	user_deets = RPS_Score.objects.filter(user=current_user).first()
	wallet, created = Wallet.objects.get_or_create(user=current_user)
	
	if user_deets:
		get_user_level = user_deets.level
		user_wins = user_deets.total_wins
		wallet = Wallet.objects.filter(user=current_user).first()
		print(f'wallets returned: {wallet}')
		#wallet = Wallet.objects.filter(user=current_user).first()

		print(f'{current_user} deets is in level {get_user_level} and has {user_wins} wins')
		result = calc_wallet(get_user_level)
	
	
		if result == 'equal':
			gpoints = user_wins
			print(f'gpoints:{gpoints}')
			wallet.balance = gpoints
			wallet.save()
		elif result == 'addition':
			gpoints = user_wins + (user_wins / 2)
			wallet.balance = gpoints
			wallet.save()
		elif result == 'multiply':
			gpoints = user_wins * 2
			wallet.balance = gpoints
			wallet.save()
		elif result == 'exponential':
			gpoints = user_wins * 3
			wallet.balance = gpoints
			wallet.save()
		print(f'{current_user} is in level {get_user_level} with a balance of N{wallet.balance}')
		ctx = {
		'user_deets': get_user_level, 'wallet':wallet
		}
		return render(request,'my_wallet.html', ctx)
	else: 
		print('No level found!!!')
		user_deets = ''
		return render(request,'my_wallet.html')

		
	

def check_level(request):
	return render(request,'my_wallet.html')