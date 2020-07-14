class Player:
    def __init__(self, user):
        """
        Initialises a quiz player.

        :param user: user associated with the new player.
        """
        self.user = user
        self.points = 0
        self.has_set_round_score = False

    def update_points(self, change):
        """
        Updates the user's points total.

        :param change: user's points from previous round.
        """
        self.points += change

    def reset_has_set_score(self):
        """
        Resets tracker than ensures user has set their score for previous round.
        """
        self.has_set_round_score = False
