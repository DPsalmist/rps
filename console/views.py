from django.shortcuts import render, redirect
from .game_logic import determine_winner, get_level
from .models import Scoreboard, Score, Round, Game, Gameboard, RPS_Score, RPSGameboard, WinningStreak
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model 
from django.urls import reverse
from datetime import date
import random

User = get_user_model()

# Create your views here.

@login_required
def play_game(request):
    # Get the current user
    current_user = request.user

    # Get the user's Score & Game object or create one if it doesn't exist
    score, created = RPS_Score.objects.get_or_create(user=current_user)
    print(f'user_score:{score}')
    game, created = RPSGameboard.objects.get_or_create(user=current_user) 

    # Increment the total_played field
    score.total_played += 1

    # Play the game and determine the result
    #player_choice = request.POST.get('player_choice')
    if request.method == 'POST':
        player_choice = request.POST['user_choice']
        computer_choice = random.choice(['rock', 'paper', 'scissors'])

        # save computer choice #if game and score:
        request.session['computer_choice'] = computer_choice
        request.session['player_choice'] = player_choice

        result = determine_winner(player_choice, computer_choice)

        # If the player wins, increment the total_wins field
        if result == 'user':
            score.total_wins += 1
            game.user_score += 2

            # update winning streak
            try:
                streak = WinningStreak.objects.get(player=request.user)
                streak.length += 1
                streak.save()
            except WinningStreak.DoesNotExist:
                WinningStreak.objects.create(player=request.user, length=1, start_date=date.today())

        # If the player loses, increment the total_losses field
        elif result == 'computer':
            score.total_losses += 1
            game.computer_score +2

        # else it's a draw
        elif result == 'tie':
            score.total_draws +=1            

        # Get user_deets
        games_played = score.total_played
        win_percentage = score.win_percentage
        check_user_level = get_level(games_played, win_percentage)

        # Level logic
        if check_user_level == 'Beginner':
            print(f'{current_user} is in 1')
            score.level = 'Beginner'
            #user_deets.save()
        elif check_user_level == 'Intermediate':
            print(f'{current_user} is in 2')
            score.level = 'Intermediate'
            #user_deets.save()
        elif check_user_level == 'Advanced':
            print(f'{current_user} is in 3')
            score.level = 'Advanced'
            #user_deets.save()
        else:
            print(f'{current_user} is in Level None')
            score.level = 'Expert'
            print(f'{current_user} is in 4')
            #user_deets.save()


        # Save the Score & game object
        win_percentage = score.total_wins / score.total_played * 100
        score.win_percentage = round(win_percentage, 2)
        score.save()
        game.save()
        return redirect(reverse('game-results') + '?result=' + result)
        #return render(request, 'game_interface.html', {'score':score})
    else:
        return render(request, 'game_interface.html')
        # Render the game results template with the result and choices
        #return render(request, 'game_results.html', {'result': result, 'player_choice': player_choice, 'computer_choice': computer_choice})


@login_required
def game_results(request):
    scores = RPS_Score.objects.filter(user=request.user).last()
    ranks = RPS_Score.objects.all()[:3]
    games_played = RPS_Score.objects.order_by('total_played')[:5]
    player_ranks = RPS_Score.objects.all().order_by('-win_percentage')
    position = 0
    print('results socre from game_results;', games_played)

    # Rank logic
    for rank in player_ranks:
        position += 1
        if rank.user == scores.user:
            print(f'player_position; {position}')
            break

    total_wins = scores.get_total_wins()
    total_losses = scores.get_total_losses()
    total_draws = scores.get_total_draws()
    total_played = scores.get_total_played()
    winner = request.GET.get('result')
    print(f'game _results winner is: {winner}')

    computer_choice = request.session.get('computer_choice')
    user_choice = request.session.get('player_choice')
    ctx = {
            'winner': winner, 'scores': scores, 
            'computer_choice':computer_choice, 'position':position,
            'user_choice':user_choice, 'total_wins':total_wins,
            'total_losses':total_losses, 'total_draws':total_draws,
            'total_played':total_played, 'ranks':ranks, 'games_played':games_played
        }
    return render(request, 'game_results.html', ctx)
