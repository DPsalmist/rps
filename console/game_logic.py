def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "tie"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
    (user_choice == "paper" and computer_choice == "rock") or \
    (user_choice == "scissors" and computer_choice == "paper"):
        return "user"
    else:
        return "computer"

'''
be: 0 - 20
in: 21 - 49
ad: 50 - 69
ex: 70 >

'''

def get_level(games_played, win_percentage):
    if games_played < 15 and win_percentage < 30.0: # 0 -> 49
        return 'Beginner'
    elif games_played >= 15 and 30.0 < win_percentage <= 50.0: # 50 -> 99
        return 'Intermediate'
    elif games_played >= 50 and 51 <= win_percentage <= 75.0: # 100 -> 199
        return 'Advanced'
    elif games_played >= 100 and win_percentage > 75.0: # 200 -> ...
        return 'Expert'
    else:
        return 'Beginner'
 

def calc_wallet(get_user_level):
    if get_user_level == 'Beginner':
        return 'equal'
    elif get_user_level == 'Intermediate':
        return 'addition'
    elif get_user_level == 'Advanced':
        return 'multiply'
    else:
        return 'exponential'