# Local modules.
import quiz
import message


def join(author, action_items):
    """
    Joins user to ongoing quiz.

    :param author: user to be added to quiz.
    :param action_items: the dict of action_items.
    :return: reply to user.
    """
    action = action_items.get(author)
    if isinstance(action, quiz.Quiz):
        reply = "No need to join your own quiz, {0.author.mention} :wink:"

    else:
        current_quiz = quiz.get_ongoing_quiz(action_items)

        if current_quiz is not None:
            current_quiz.add_player(author)
            current_quiz.round_scores_entered += 1  # Ensures quiz is allowed to start.
            reply = "{0.author.mention} is in :sunglasses:"

        else:
            reply = None

    return reply


def start(current_action):
    """
    Starts a quiz.

    :param current_action: the user's current action.
    :return: reply to user.
    """
    if isinstance(current_action, quiz.Quiz):

        if current_action.current_round > -1:
            reply = "The quiz has already started pal."

        else:
            reply = current_action.start()

    else:
        reply = None

    return reply


# Note: 'next' is protected.
def quiz_next(current_action, content):
    """
    Takes the next action in the ongoing quiz.

    :param current_action: the user's current action.
    :param content: possible 'force' flag.
    :return: reply to user.
    """
    if content != "" and "force".startswith(content):
        is_force = True

    else:
        is_force = False

    if isinstance(current_action, quiz.Quiz):
        reply = current_action.next(is_force)

    else:
        reply = None

    return reply


def points(author, action_items, score_add):
    """
    Adds round points to user's total.

    :param author: user who is inputting round's points.
    :param action_items: the dict of action items.
    :param score_add: user's score for the round.
    :return: reply to user.
    """
    current_quiz = quiz.get_ongoing_quiz(action_items)

    if current_quiz is not None:
        player = current_quiz.contains_player(author)

        if player is not None:
            try:
                score = float(score_add)
            except ValueError:
                score = -1

            if score >= 0:
                if player.has_set_round_score is False:
                    player.update_points(score)
                    player.has_set_round_score = True
                    current_quiz.round_scores_entered += 1
                    reply = "Your score has been updated {0.author.mention} - your new total is " \
                            + str(player.points) + " :brain:"

                else:
                    reply = "I already have your score, {0.author.mention} :eyes:"

            else:
                reply = "Please enter a valid score {0.author.mention} :confused:"

        else:
            reply = "You're not registered for this quiz, {0.author.mention} :eyes:"

    else:
        reply = None

    return reply


def leaderboard(action_items):
    """
    Displays the quiz leaderboard.

    :param action_items: the dict of action items.
    :return: reply to user.
    """
    current_quiz = quiz.get_ongoing_quiz(action_items)

    if current_quiz is not None:
        current_quiz.sort_players()
        reply = message.show_leaderboard(current_quiz.players)

    else:
        reply = None

    return reply


def create():
    """
    Prompts user to check DMs to create quiz.

    :return: reply to user.
    """
    reply = "I'll slide into your DMs, {0.author.mention}, and we can cook up a quiz :wink:"

    return reply


def edit():
    """
    Prompts user to check DMs to edit quiz.

    :return: reply to user.
    """
    reply = "Check your DMs for instructions on how to mix things up, {0.author.mention} :call_me:"

    return reply


def play(author, action_items):
    """
    Initialises a new quiz.

    :param author: user initialising quiz.
    :param action_items: the dict of action items.
    :return: reply to user.
    """
    if author in action_items:
        reply = "You cannot start a new action whilst you have another ongoing, {0.author.mention}"
    else:
        action_items[author] = quiz.SelectQuiz()
        reply = message.available_quizzes()

    return reply


def select_quiz(author, action_items, command):
    """
    Allows user to select quiz from numbered list.

    :param author: user selecting quiz.
    :param action_items: the dict of action items.
    :param command: the user's parameter input for number selection.
    :return:
    """
    action = action_items.get(author)

    if isinstance(action, quiz.SelectQuiz):
        file_no = command[1:]

        try:
            file_no = int(file_no)
        except ValueError:
            file_no = ""

        if isinstance(file_no, int):
            files = message.get_files()

            if file_no <= len(files):
                action_items[author] = quiz.Quiz(files[file_no - 1])
                reply = "We are ready to go, @everyone, use `?join` to add yourself to the quiz!\n" \
                        "When we're ready to go, the quiz-master can use `?start` :call_me:"

            else:
                reply = "Please select a file number within the range displayed."

        else:
            reply = "Please select a quiz from the list using its number :upside_down:"

    else:
        reply = None

    return reply
