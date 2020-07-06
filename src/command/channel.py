# All methods will return the appropriate reply (and None if invalid input).

from general import action_items
from message import *
from quiz import *


def exit_action(author):
    if author in action_items:
        action_items.pop(author)
        reply = "Your progress has been successfully aborted :gun:"
    else:
        reply = "You have nothing to exit :face_with_monocle:"

    return reply


def join(author):
    action = action_items.get(author)

    if isinstance(action, Quiz):
        reply = "No need to join your own quiz, {0.author.mention} :wink:"
    else:
        quiz = get_ongoing_quiz(action_items)
        if quiz is not None:
            quiz.add_player(author)
            reply = "{0.author.mention} is in :sunglasses:"
        else:
            reply = None

    return reply


def start(author):
    action = action_items.get(author)

    if isinstance(action, Quiz):
        if action.current_round > -1:
            reply = "The quiz has already started pal."
        else:
            reply = action.start()
    else:
        reply = None

    return reply


# Note: 'next' is protected.
def quiz_next(author):
    action = action_items.get(author)

    if isinstance(action, Quiz):
        reply = action.next()
    else:
        reply = None

    return reply


def points(author, score_add):
    quiz = get_ongoing_quiz(action_items)

    if quiz is not None:
        player = quiz.contains_player(author)
        if player is not None:
            try:
                score = float(score_add)
            except ValueError:
                score = -1
            if score >= 0:
                player.update_points(score)
                reply = "Your score has been updated {0.author.mention} - your new total is " \
                        + str(player.points) + " :brain:"
            else:
                reply = "Please enter a valid score {0.author.mention} :confused:"
        else:
            reply = "You're not registered for this quiz, {0.author.mention} :eyes:"
    else:
        reply = None

    return reply


def leaderboard():
    quiz = get_ongoing_quiz(action_items)

    if quiz is not None:
        quiz.sort_players()
        reply = show_leaderboard(quiz.players)
    else:
        reply = None

    return reply


def create():
    reply = "I'll slide into your DMs, {0.author.mention}, and we can cook up a quiz :wink:"

    return reply


def edit():
    reply = "Check your DMs for instructions on how to mix things up, {0.author.mention} :call_me:"

    return reply


def play(author):
    if author in action_items:
        reply = "You cannot start a new action whilst you have another ongoing, {0.author.mention}"
    else:
        action_items[author] = SelectQuiz()
        reply = available_quizzes()

    return reply


def select_quiz(author, command):
    action = action_items.get(author)

    if isinstance(action, SelectQuiz):
        file_no = command[1:]

        try:
            file_no = int(file_no)
        except ValueError:
            file_no = ""

        if isinstance(file_no, int):
            files = get_files()
            if file_no <= len(files):
                action_items[author] = Quiz(files[file_no - 1])
                reply = "We are ready to go, @everyone, use `?join` to add yourself to the quiz!\n" \
                        "When we're ready to go, the quiz-master can use `?start` :call_me:"
            else:
                reply = "Please select a file number within the range displayed."
        else:
            reply = "Please select a quiz from the list using its number :upside_down:"

    else:
        reply = None

    return reply
