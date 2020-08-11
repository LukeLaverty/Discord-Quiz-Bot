import os

# Quiz save directory.
quiz_dir = "../quiz"


def get_files():
    """
    Gets list of files from save directory ending with '.quiz'.

    :return: list of files in save directory.
    """
    raw_list = os.listdir(quiz_dir)
    quiz_list = []
    for file in raw_list:
        if file.endswith(".quiz"):
            quiz_list.append(file)

    return quiz_list


def help_message():
    """
    Generates user help message as string.

    :return: user help message.
    """
    message = "Here's what you can do, {0.author.mention}:\n" \
              ">>> " \
              "__From anywhere:__\n" \
              "  `?help` will show you this screen, duh.\n" \
              "  `?drop` will cancel any ongoing actions - including your quiz.\n" \
              "__From a channel:__\n" \
              "  `?create` will prompt you in your DMs to create a new quiz.\n" \
              "  `?edit` will prompt you in your DMs to edit a quiz.\n" \
              "  `?play` will allow you to play your quiz.\n" \
              "__During a quiz:__\n" \
              "  `?join` will add you to the quiz.\n" \
              "  `?next` will display the next question, answers if at the end of the round, and next round.\n" \
              "  `?points` allows each user to input their score for each round.\n" \
              "  `?leaderboard` will display the current leaderboard.\n" \
              "  `?quit` allows you to leave a quiz midway.\n" \
              "__From your direct messages:__\n" \
              "  `?create` will prompt you to create a new quiz.\n" \
              "  `?edit` will allow you to edit a pre-existing quiz.\n"
    return message


def available_quizzes():
    """
    Generates a numbered list of available quizzes for user to select from.

    :return: list of available quizzes.
    """
    avail_files = get_files()

    counter = 1

    file_list = "```md\n"
    for file in avail_files:
        name = os.path.splitext(file)[0]
        name = __sanitise_markdown(name)
        file_list += str(counter) + ". " + name + "\n"
        counter += 1
    file_list += "```\n"

    reply = "Okay, {0.author.mention}, you're the quiz-master, lets get this party started!\n" \
            "These are the quizzes available to you:\n" \
            + file_list + \
            "Please select a number using `?[number]` :thumbsup:"

    return reply


def round_answers(answers):
    """
    Generates a string of round answers.

    :param answers: the answers to the round.
    :return: the string of answers.
    """
    ans_list = []
    for question in answers:
        ans_list.append(question.get("answer"))

    reply = "> **Answers:**\n"

    counter = 1
    for ans in ans_list:
        reply += str(counter) + ": " + ans + "\n"
        counter += 1

    # Ensures new line is taken.
    reply += "\nPlease enter your score using `?points [points]` :brain:"

    return reply


def show_leaderboard(players):
    """
    Generates a leaderboard in text.

    :param players: list of player objects sorted in descending order of points.
    :return: string display of leaderboard.
    """
    reply = "The current standings:\n"

    if len(players) == 0:
        reply += "` `\n "
    else:
        reply += "```md\n"

        for i in range(len(players)):
            pos = i + 1
            while i - 1 > 0 and players[i - 1].points == players[i]:
                pos -= 1

            reply += str(pos) + ". " + __sanitise_markdown(players[i].user.display_name) + " - " + \
                     str(players[i].points) + "\n"

        reply += "```\n"

    return reply


def clear_chat():
    """
    Prints a series of new lines to clear 'pub-quiz' channel before new quiz.

    :return: string series of new lines.
    """
    reply = ".\n" * 60
    return reply


def __sanitise_markdown(string):
    """
    Sanitises string of characters reserved in markdown.

    :param string: the string to be sanitised.
    :return: sanitised string.
    """
    return string.replace("#", "") \
        .replace("*", "") \
        .replace(">", "") \
        .replace("+", "") \
        .replace("`", "")
