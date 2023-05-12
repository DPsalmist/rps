from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .forms import ProfileUpdateForm, UserUpdateForm, UserRegistrationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from console.models import RPSGameboard, RPS_Score, WinningStreak
from console.game_logic import get_level
from wallet.models import Wallet 
from django.contrib import messages
from .models import Profile, Follow, CustomUser
from subscription.models import Member

User = get_user_model()


# Create your views here.
def index(request):
    return redirect('home')

def landing(request):
    top_players = RPS_Score.objects.order_by('-win_percentage')[:3]
    my_queryset_length = len(top_players)
    print(f'my_qs_len => {my_queryset_length}')
        
    print(f'top three: {top_players}')
    ctx = {'top_players': top_players, 'my_queryset_length':my_queryset_length}
    return render(request, 'landing.html', ctx)

def test_dashboard(request):
    return render(request, 'dashboard_base.html')


def home(request):
    users = User.objects.all().count()
    games = RPSGameboard.objects.all().count()
    return render(request, 'home.html', {'users':users, 'games':games})

# conscious presence of God in our services, favour for  the building project.

def signup(request, referral_code=None):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        pwd=request.POST.get('password')
        referral_code = request.POST.get('get_referral_code')
        print(f'initial reffered_by => {referral_code}')

        if referral_code:
            try:
                the_referral = User.objects.filter(referral_code=referral_code).first()
                if the_referral:
                    user = User.objects.create_user(
                        username=username, email=email, 
                        referred_by=the_referral, 
                        is_online=True,
                        password=pwd)
                    
                    user.save()
                    login(request, user)
                    return redirect('login')
            except AttributeError:
                return HttpResponse('<h2>No User with such referral code exist!</h2>')
        else:
            user = User.objects.create_user(
                    username=username, email=email, is_online=True, password=pwd)
                    
            user.save()
            login(request, user)
            return redirect('login')
    return render(request, 'signup2.html')



def login_view(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        pwd=request.POST.get('password')
        print(f'{username} and {pwd} here')
        user=authenticate(request, username=username, password=pwd)
        #form = AuthenticationForm(request, data=request.POST)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse('This user is not found!!!')
            print(f'User is not found!')
    return render(request, 'login2.html')



@login_required
def dashboard(request):
    users = User.objects.all().count()
    games = RPSGameboard.objects.all().count()
    current_user = request.user
    current_user_code = current_user.referral_code
    player_membership = Member.objects.filter(user=current_user).first()
    print(f'player membership => {player_membership}')
    my_referrals = User.objects.filter(referred_by=current_user).count()

    # top players
    top_players = RPS_Score.objects.order_by('-win_percentage')[:3]
    for t in top_players:
        print(f'top=> {t.user}')


    player_wallet = Wallet.objects.filter(user=current_user).first()
    print(f'player_wallet => {player_wallet}')
    try:
        player_wallet_balance = player_wallet.balance
    except AttributeError:
        player_wallet_balance = 0
    print(f'this player membership => {player_membership.subscription_plan},with balance => \
        #{player_wallet_balance} and referral_code => {my_referrals}')
    
    # Get the last login time of the user
    last_login_time = current_user.last_login
    print(f'user last_login, {last_login_time}')
    if timezone.now() - last_login_time <= timezone.timedelta(minutes=5):
        # User is considered online if their last login was less than 5 minutes ago
        print("User is online")
    else:
        print("User is offline")

    online_status = 'x'
    my_ref_link = current_user.get_referral_link()
    print(f'referaal link: {my_ref_link}')
    followers = current_user.followers.all().count()
    following = current_user.following.all().count()
    user_deets = RPS_Score.objects.filter(user=current_user).first()
    player_ranks = RPS_Score.objects.all().order_by('-win_percentage')
    position = 0
    
    # Scores logic
    if user_deets == None:
        user_deets = ''
        total_wins = 0
        total_losses = 0 
        total_draws = 0
        total_played = 0
        win_percentage = 0
        print(f'this user_deets - {user_deets}')
    else:
        total_wins = user_deets.get_total_wins()
        total_losses = user_deets.get_total_losses()
        total_draws = user_deets.get_total_draws()
        total_played = user_deets.get_total_played()
        win_percentage = user_deets.get_win_percentage()
        win_percentage = round(win_percentage, 2)

        # Get user_deets
        games_played = user_deets.total_played
        win_percentage = user_deets.win_percentage
        check_user_level = get_level(games_played, win_percentage)

        print(f'{current_user} deets are ==> {games_played} games and {win_percentage}%')
        print(f'user_level {check_user_level}')

        '''
        # Level logic
        if check_user_level == 'Beginner':
            print(f'{current_user} is in 1')
            user_deets.level = 'Beginner'
            #user_deets.save()
        elif check_user_level == 'Intermediate':
            print(f'{current_user} is in 2')
            user_deets.level = 'Intermediate'
            #user_deets.save()
        elif check_user_level == 'Advanced':
            print(f'{current_user} is in 3')
            user_deets.level = 'Advanced'
            #user_deets.save()
        else:
            print(f'{current_user} is in Level None')
            user_deets.level = 'Expert'
            print(f'{current_user} is in 4')
            #user_deets.save() 
        '''

        # Rank logic
        for rank in player_ranks:
            position += 1

            if rank.user == user_deets.user:
                print(f'player_position; {position}')
                break
        request.session['position'] = position

        user_deets.save()
        print(f'new user level {user_deets.level}')
    
    print(f'current_user scores:{user_deets}')
    #ranks = RPS_Score.objects.order_by('-win_percentage')[:3]
    ranks = RPS_Score.objects.all()[:5]
    games_played = RPS_Score.objects.order_by('-total_played')[:5]
    winner = request.GET.get('result')
    ctx = {
        'users':users, 'games':games, 'total_played':total_played,
        'total_wins':total_wins, 'total_draws':total_draws, 
        'total_losses':total_losses, 'win_percentage':win_percentage,
        'ranks':ranks, 'games_played':games_played, 'followers':followers,
        'following':following, 'user_deets':user_deets, 'position':position,
        'my_ref_link':my_ref_link,'player_membership':player_membership,
        'player_wallet_balance':player_wallet_balance, 'my_referrals':my_referrals,
        'top_players':top_players
    }
    return render(request, 'dashboard.html', ctx)


    
@login_required
def update_profile(request):
    current_user = request.user
    #user_role = current_user.groups.all()[0].name

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect ('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
    'u_form':u_form,
    'p_form':p_form,
    #'user_role':user_role
    }   
    return render(request, 'update_profile.html', context)


@login_required
def profile(request):
    current_user = request.user
    return render(request, 'profile.html')


@login_required
def players(request):
    players = User.objects.all()
    # Pagination
    page = request.GET.get('page')
    paginator = Paginator(players, 6)

    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)
    
    return render(request, 'players.html', {'players':players})


@login_required
def player_detail(request, pk):
    player = User.objects.get(id=pk)
    player_deet = RPS_Score.objects.filter(user=player).first()
    current_user = request.user
    tot_followers = player.followers.all().count()

    print(f'current_player:{player} vs loggedin user: {current_user}')

    p_followers = Follow.objects.filter(followed=player).values_list('follower__username', flat=True)
    follower_list = [f for f in p_followers]
    check2 = current_user.username in follower_list
    print('check2=',check2)
    print(f'the followers of player {player} are:', follower_list)
    
    scores = RPS_Score.objects.filter(user=player).last()
    player_ranks = RPS_Score.objects.all().order_by('-win_percentage')

    position = 0
    request.session['player_id'] = player.id
        
    if scores == None:
        scores = 0
        total_wins = scores
        total_losses = scores 
        total_draws = scores
        total_played = scores
        win_percentage = scores
    else:
        total_wins = scores.get_total_wins()
        total_losses = scores.get_total_losses()
        total_draws = scores.get_total_draws()
        total_played = scores.get_total_played()
        win_percentage = scores.get_win_percentage()
        win_percentage = round(win_percentage, 2)

        for rank in player_ranks:
            position += 1

            if rank.user == scores.user:
                print(f'player_position; {position}')
                break

    ctx = {
        'player':player, 'total_wins':total_wins, 
        'win_percentage':win_percentage, 'total_played':total_played,
        'position':position, 'tot_followers':tot_followers, 'follower_list':follower_list,
        'player_deet':player_deet
        }
    return render(request, 'player_detail.html', ctx)


@login_required
def follow(request, username):
    follower = request.user
    followed = User.objects.get(username=username)
    print(f'followed={followed}')
    Follow.objects.create(follower=follower, followed=followed)
    return redirect('dashboard')


@login_required
def unfollow(request, username):
    follower = request.user
    followed = User.objects.get(username=username)
    follow = Follow.objects.get(follower=follower, followed=followed)
    follow.delete()
    return redirect('dashboard',)


def connections_view(request):
    user = request.user
    # get the followers and following of the user
    followers = Follow.objects.filter(followed=user)
    following = Follow.objects.filter(follower=user)
    tot_followers = followers.count()
    tot_following = following.count()

    context = {
        'followers': followers,
        'following': following,
        'tot_followers':tot_followers,
        'tot_following':tot_following
    }
    return render(request, 'player_connections.html', context)