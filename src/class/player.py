class Player:
    def __init__(self, user):
        self.user = user
        self.points = 0

    def update_points(self, change):
        self.points += int(change)
