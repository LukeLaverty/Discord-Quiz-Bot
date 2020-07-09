import os

quiz_dir = "../quiz"


def get_files():
    return os.listdir(quiz_dir)


def help_message():
    message = "Here's what you can do, {0.author.mention}:\n" \
              ">>> " \
              "__From anywhere:__\n" \
              "  `?help` will show you this screen, duh.\n" \
              "  `?drop` will cancel any ongoing actions - including your quiz.\n" \
              "__From a channel:__\n" \
              "  `?create` will prompt you in your DMs to create a new quiz.\n" \
              "  `?edit` will prompt you in your DMs to edit a quiz.\n" \
              "  `?quiz` will allow you to play your quiz.\n" \
              "__During a quiz:__\n" \
              "  `?join` will add you to the quiz.\n" \
              "  `?next` will display the next question, answers if at the end of the round, and next round.\n" \
              "  `?points` allows each user to input their score for each round.\n" \
              "  `?leaderboard` will display the current leaderboard.\n" \
              "__From your direct messages:__\n" \
              "  `?create` will prompt you to create a new quiz.\n" \
              "  `?edit` will allow you to edit a pre-existing quiz.\n"
    return message


def available_quizzes():
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
    ans_list = []
    for question in answers:
        ans_list.append(question.get("answer"))

    reply = "> **Answers:**\n"

    counter = 1
    for ans in ans_list:
        reply += str(counter) + ": " + ans + "\n"
        counter += 1

    # Ensures new line is taken.
    reply += " "

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
        counter = 1

        for player in players:
            reply += str(counter) + ". " + __sanitise_markdown(player.user.display_name) + " - " + str(player.points) \
                     + "\n"
            counter += 1
        reply += "```\n"

    return reply


def __sanitise_markdown(string):
    return string.replace("#", "")\
        .replace("*", "")\
        .replace(">", "")\
        .replace("+", "")\
        .replace("`", "")
