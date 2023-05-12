from django.urls import path
from .views import play_game, game_results

urlpatterns = [
    path('play-game/', play_game, name='play-game'),
    path('game-results/', game_results, name='game-results'),
]