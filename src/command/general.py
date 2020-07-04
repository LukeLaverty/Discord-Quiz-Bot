# All methods will return the appropriate reply (and None if invalid input).

from message import help_message

# Dictionary associates each user with an action class.
action_items = {}


# Note: 'help' is protected.
def get_help():
    reply = help_message()

    return reply
