from django.urls import path 
from .views import signup, home, index, dashboard, profile, update_profile, players, \
	player_detail, follow, unfollow, connections_view, \
    landing, login_view, signup, test_dashboard


urlpatterns = [
	path('', index, name='index'),
	path('home/', landing, name='home'),
	path('dashboard/', dashboard, name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    #path('accounts/signup1/', signup, name='signup1'),
	#path('accounts/signup1/<str:referral_code>/', signup, name='signup1'),
    #path('login1/', login_view1, name='login'),
    path('accounts/profile/update', update_profile, name='update-profile'),
    path('players/', players, name='players'),
    path('player/<int:pk>/', player_detail, name='player-detail'),
    path('follow/<str:username>/', follow, name='follow'),
    path('unfollow/<str:username>/', unfollow, name='unfollow'),
    path('player-connections/', connections_view, name='my-connections'),

    # New Templates
    path('landing/', landing, name='landing'),
    path('dashboard-test/', test_dashboard, name='test_dashboard'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/signup/<str:referral_code>/', signup, name='signup'),
]