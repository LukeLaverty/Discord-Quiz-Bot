import message


# Note: 'help' is protected.
def get_help():
    """
    Gets help message.

    :return: the help message.
    """
    reply = message.help_message()

    return reply


def exit_action(author, action_items):
    """
    Exits the user's current action.

    :param author: the user who's action is to be aborted.
    :param action_items: the dict of action items.
    :return: reply to user.
    """
    if author in action_items:
        action_items.pop(author)
        reply = "Your progress has been successfully aborted :gun:"
    else:
        reply = "You have nothing to exit :face_with_monocle:"

    return reply
