from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model() 

# Create your models here.


class Game(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_player1')
    status_choices = [
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='waiting')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_winner', blank=True, null=True)

class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='round_game')
    player1_choice = models.CharField(max_length=20)
    computer_choice = models.CharField(max_length=20, blank=True, null=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='round_winner', blank=True, null=True)

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score_user')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    num_played = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} wins: {self.wins} outta {self.num_played} games.'



class Scoreboard(models.Model):
    user_score = models.IntegerField(default=0)
    computer_score = models.IntegerField(default=0)

    def __str__(self):
        return f"User: {self.user_score} - Computer: {self.computer_score}"


class RPS_Score(models.Model):
    levels = (
        ('level 1', 'Level 1'),
        ('level 2', 'Level 2'),
        ('level 3', 'Level 3'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rpsscore_user')
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)
    total_draws = models.IntegerField(default=0)
    total_played = models.IntegerField(default=0)
    win_percentage = models.FloatField(default=0.0)
    level = models.CharField(max_length=20, null=True, default='Beginner')

    def __str__(self):
        return f'{self.win_percentage}% win percentage outta {self.total_played} games.'
   
    def get_total_wins(self):
        return self.total_wins

    def get_total_losses(self):
        return self.total_losses

    def get_total_draws(self):
        return self.total_draws

    def get_total_played(self):
        return self.total_played

    def get_win_percentage(self):
        self.win_percentage = self.total_wins / self.total_played * 100 if self.total_played > 0 else 0
        return self.win_percentage

    class Meta:
        ordering = ('-win_percentage',)


class Gameboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_point')
    user_score = models.IntegerField(default=0)
    computer_score = models.IntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user} vs Computer: {self.user_score} : {self.computer_score}, {self.date_played}"


class RPSGameboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rpsuser_point')
    user_score = models.IntegerField(default=0)
    computer_score = models.IntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Player {self.user} vs Computer => {self.user_score} : {self.computer_score}, {self.date_played}"



class WinningStreak(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    length = models.PositiveIntegerField(default=0)
    start_date = models.DateField()

    def __str__(self):
        return f"{self.player.username}'s winning streak ({self.length})"

    class Meta:
        verbose_name_plural = "Winning streaks"
