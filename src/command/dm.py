# All methods will return the appropriate reply (and None if invalid input).

from general import action_items
from quiz import *


def exit_action(author):
    if author in action_items:
        action_items.pop(author)
        reply = "Your progress has been successfully aborted :gun:"
    else:
        reply = "You have nothing to exit :face_with_monocle:"

    return reply


def create(author):
    if author in action_items:
        reply = "You cannot start a new action whilst you have another ongoing!"
    else:
        action_items[author] = CreateQuiz()

        reply = "Okay, lets get started! We're entering **create mode**. " \
                "You can exit this at any time with `?drop`, but your progress will not be saved.\n" \
                "Firstly, we need to name your quiz! Use `?name [quiz_name]` to do so.\n" \
                "Try something like:\n" \
                "> \"Luke's Quiz 28-07-2001\""

    return reply


def set_name(author, input_name):
    action = action_items.get(author)

    if isinstance(action, CreateQuiz):
        if input_name != "":
            action.set_name(input_name)
            reply = "Your quiz has been named :tada:\nStart your first round by using `?round [round_name]`!"
            print("A quiz named " + input_name + " has been initialised by " + author.name)
        else:
            reply = "Please pick a name for your quiz!\nUsage: `?name [quiz_name]`."
    else:
        reply = None

    return reply


def set_round(author, round_name):
    action = action_items.get(author)

    if isinstance(action, CreateQuiz):
        # Ensures quiz is named first.
        if action.name == "":
            reply = "Please pick a name for your quiz!\nUsage: `?name [quiz_name]`."
        else:
            # Ensures empty rounds cannot be created.
            if action.current_round is None or len(action.current_round.questions) > 0:
                # Ensures answer to previous question has been submitted.
                if action.current_question == "":
                    if round_name != "":
                        action.next_round(round_name)
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
    else:
        reply = None

    return reply


def set_round_music(author):
    action = action_items.get(author)

    if isinstance(action, CreateQuiz):
        if action.current_round is not None:
            action.toggle_music()
            if action.current_round.is_music:
                reply = "This round is now a music round! Use `?music` again if you change your mind :musical_note:"
            else:
                reply = "This round is no longer a music round :musical_note:"
        else:
            reply = "Start your round using `?round [round_name]` first before setting it as a music round " \
                    ":musical_note:"
    else:
        reply = None

    return reply


def set_question(author, question):
    action = action_items.get(author)

    if isinstance(action, CreateQuiz):
        # Ensures answer to previous question has been submitted.
        if action.current_question == "":
            if question != "":
                action.create_question(question)
                reply = "Question recorded, now give me the answer using `?answer [answer]` - I won't tell :wink:"
            else:
                reply = "Tell me what the question is!\nUsage: `?question [question]`."
        else:
            reply = "Give me the answer to the last question first, silly :stuck_out_tongue:"
    else:
        reply = None

    return reply


def set_answer(author, answer):
    action = action_items.get(author)

    if isinstance(action, CreateQuiz):
        if action.current_question != "":
            if answer != "":
                action.add_question(answer)
                reply = "I'll keep that a secret, promise :eyes:\n" \
                        "From here, you can use `?question`, `?round` or `?finish` :thumbsup:"
            else:
                reply = "Tell mw what the answer is!\nUsage: `?answer [answer]`."
        else:
            reply = "I don't know what this is the answer to :upside down:"
    else:
        reply = None

    return reply


def finish(author):
    action = action_items.get(author)

    if isinstance(action, CreateQuiz):
        current_round = action.current_round
        if current_round is not None and len(current_round.questions) > 0:
            action.finish()
            reply = "All done! Your quiz is locked and loaded :sunglasses:"
            print(author.name + " has completed a quiz which has been saved.")
            action_items.pop(author)
        else:
            reply = "You haven't added any questions, dafty :nerd:"
    else:
        reply = None

    return reply


def channel_create():
    reply = "Use `?create` in the DMs to get started :wink:"

    return reply


def channel_edit():
    reply = "This feature hasn't been implented yet, shagger :wink:"

    return reply
