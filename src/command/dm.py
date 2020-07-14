import re
# Local modules.
import quiz


def create(author, action_items):
    """
    Creates a new quiz for the user.

    :param author: the user for whom the quiz is created.
    :param action_items: the dict of action items.
    :return: reply to user.
    """
    if author in action_items:
        reply = "You cannot start a new action whilst you have another ongoing!"
    else:
        action_items[author] = quiz.CreateQuiz()

        reply = "Okay, lets get started! We're entering **create mode**. " \
                "You can exit at any time with `?drop`, but your progress will not be saved.\n" \
                "Firstly, we need to name your quiz! Use `?name [quiz_name]` to do so. Try something like:\n" \
                "> Luke's Quiz 28-07-2001"

    return reply


def set_name(author, current_action, input_name):
    """
    Sets the name of the user's quiz.

    :param author: the user creating the quiz.
    :param current_action: the current action of the user.
    :param input_name: the user's parameter input for name.
    :return: reply to user.
    """
    if input_name != "":

        # Checks filename is valid for Windows file system.
        pattern = re.compile("[<>:\"/\\|?*]")

        if pattern.search(input_name) is not None:
            reply = "Please ensure your file name avoids the following illegal characters: `<>:\"/\\|?*`"

        else:
            current_action.set_name(input_name)
            reply = "Your quiz has been named :tada:\nStart your first round by using `?round [round_name]`!"

            print("A quiz named " + input_name + " has been initialised by " + author.name)

    else:
        reply = "Please pick a name for your quiz!\nUsage: `?name [quiz_name]`."

    return reply


def set_round(current_action, round_name):
    """
    Creates a new round in a quiz.

    :param current_action: the current action of the user.
    :param round_name: the user's parameter input for round name.
    :return: reply to user.
    """
    if current_action.name == "":
        reply = "Please pick a name for your quiz!\nUsage: `?name [quiz_name]`."

    else:
        # Ensures empty rounds cannot be created.
        if current_action.current_round is None or len(current_action.current_round.questions) > 0:

            # Ensures answer to previous question has been submitted.
            if current_action.current_question == "":

                # Ensures round name is not empty.
                if round_name != "":
                    current_action.next_round(round_name)
                    reply = "A round named " + round_name + " has been created.\n" \
                                                            "Use `?question [content]` to add questions, then, use `?answer [content]` to add " \
                                                            "the answer. Use `?round [round_name]` to move to the next round or `?finish` to " \
                                                            "finish.\n" \
                                                            "If this round is a music round, use `?music` before you continue! :musical_note:"

                else:
                    reply = "Please name your round! Try again :smile:\nUsage: `?round [round_name]`"

            else:
                reply = "Please answer your previous question before continuing :thumbsup:"

        else:
            reply = "Your round has no questions! Use `?question [content]` to add some :wink:"

    return reply


def set_round_music(current_action):
    """
    Toggles the current round as a music round (or not).

    :param current_action: the current action of the user.
    :return: reply to user.
    """
    if current_action.current_round is not None:
        current_action.toggle_music()

        if current_action.current_round.is_music:
            reply = "This round is now a music round! Use `?music` again if you change your mind :musical_note:"
        else:
            reply = "This round is no longer a music round :musical_note:"

    else:
        reply = "Start your round using `?round [round_name]` first before setting it as a music round " \
                ":musical_note:"

    return reply


def set_question(current_action, question):
    """
    Creates a new question in the quiz.

    :param current_action: the current action of the user.
    :param question: the user's parameter input for question content.
    :return: reply to user.
    """
    if current_action.current_question == "":

        if question != "":
            current_action.create_question(question)
            reply = "Question recorded, now give me the answer using `?answer [answer]` - I won't tell :wink:"

        else:
            reply = "Tell me what the question is!\nUsage: `?question [question]`."

    else:
        reply = "Give me the answer to the last question first, silly :stuck_out_tongue:"

    return reply


def set_answer(current_action, answer):
    """
    Sets the answer to previously input question.

    :param current_action: the current action of the user.
    :param answer: the user's parameter input for the question answer.
    :return: reply to user.
    """
    if current_action.current_question != "":

        if answer != "":
            current_action.add_question(answer)
            reply = "I'll keep that a secret, promise :eyes:\n" \
                    "From here, you can use `?question`, `?round` or `?finish` :thumbsup:"

        else:
            reply = "Tell me what the answer is!\nUsage: `?answer [answer]`."

    else:
        reply = "I don't know what this is the answer to :upside down:"

    return reply


def finish(author, action_items):
    """
    Finishes a quiz and commits it to file.

    :param author: the user completing the quiz.
    :param action_items: the dict of action items.
    :return: reply to user.
    """
    action = action_items.get(author)

    current_round = action.current_round
    # Ensures quiz is not empty.
    if current_round is not None and len(current_round.questions) > 0:
        action.finish()
        action_items.pop(author)
        reply = "All done! Your quiz is locked and loaded :sunglasses:"

        print(author.name + " has completed a quiz which has been saved.")

    else:
        reply = "You haven't added any questions, dafty :nerd:"

    return reply


def channel_create():
    """
    Sends initial DM to user after requesting to create quiz.

    :return: reply to user.
    """
    reply = "Use `?create` in the DMs to get started :wink:"

    return reply


def channel_edit():
    """
    Sends initial DM to user after requesting to edit quiz.

    :return: reply to user.
    """
    reply = "This feature hasn't been implented yet, shagger :wink:"

    return reply
