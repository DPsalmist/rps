from django.contrib import admin
from .models import Scoreboard, Score, Round, Game, Gameboard, RPS_Score, RPSGameboard, WinningStreak

# Register your models here.
admin.site.register(Game)
admin.site.register(Scoreboard)
admin.site.register(Score)
admin.site.register(Round)
admin.site.register(Gameboard)
admin.site.register(WinningStreak)

admin.site.register(RPSGameboard)

@admin.register(RPS_Score)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'total_wins', 'total_draws', 'total_losses', 'total_played', 'win_percentage', 'level')
	list_filter = ('user', 'total_wins', 'level')
	search_fields = ('user',)
	ordering = ('-win_percentage',)
