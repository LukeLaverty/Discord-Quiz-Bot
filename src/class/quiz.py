import json
# Local modules.
import message
import player


def get_ongoing_quiz(action_items):
    """
    Checks for and returns any ongoing quiz.

    :param action_items: the dict of action items.
    :return: any ongoing quiz.
    """
    for key in action_items:
        item = action_items[key]
        if isinstance(item, Quiz):
            return item
        else:
            return None


class Quiz:
    def __init__(self, name):
        """
        Initialises a quiz object.

        :param name: file name of the quiz.
        """
        self.name = name
        self.players = []
        self.round_scores_entered = 0  # Ensures all players have entered their score before progressing.
        self.rounds = self.__read_file()
        self.current_round = -1
        self.current_question = -1

    def start(self):
        """
        Starts a quiz.

        :return: reply to user.
        """
        if len(self.players) >= 2:
            reply = message.clear_chat()
            self.current_round += 1
            reply += "*From here on out, use `?next` to move through the quiz!*\n"
            reply += self.next(False)

        else:
            reply = "You need at least 2 players to join your quiz, {0.author.mention} :family:"

        return reply

    def next(self, is_force):
        """
        Takes the next action in the quiz.

        :param is_force: true if action is to bypass certain checks.
        :return: reply to user.
        """
        if self.current_round > -1:

            if self.current_round < len(self.rounds):

                if self.current_question == -1:

                    if self.round_scores_entered >= len(self.players) or is_force:

                        self.round_scores_entered = 0
                        # Resets attribute for all players.
                        for p in self.players:
                            p.reset_has_set_score()

                        reply = "> **Round " + str(self.current_round + 1) + ": " + \
                                self.rounds[self.current_round].name + "**\n "
                        self.current_question += 1

                    else:
                        reply = "Be careful, not all players have entered their scores yet :eyes:\n" \
                                "To bypass this use `?next force`."

                # Displays question:
                elif self.current_question < len(self.rounds[self.current_round].questions):
                    question = self.rounds[self.current_round].questions[self.current_question].get("question")

                    # Checks if current round is music round:
                    if self.rounds[self.current_round].is_music is True:
                        reply = str(self.current_question + 1) + ": *now playing* :musical_note:"

                    else:
                        reply = str(self.current_question + 1) + ": " + question

                    self.current_question += 1

                    # Finishes round:
                    if self.current_question == len(self.rounds[self.current_round].questions):
                        reply += "\nThe round is over! Please post your answers - my next message will be the correct" \
                                 " answers :thumbsup:\n "

                # Displays answers:
                else:
                    reply = message.round_answers(self.rounds[self.current_round].questions)
                    self.current_question = -1
                    self.current_round += 1

            else:

                if self.round_scores_entered >= len(self.players) or is_force:
                    self.sort_players()
                    reply = "We're all done! Lets check in with the final standings:\n"
                    reply += message.show_leaderboard(self.players)
                    reply += "Congratulations to " + str(self.players[0].user.display_name) + " :tada:\n"
                    reply += "You can see the leaderboard again using `?leaderboard`. To finish, use `?drop`!"

                else:
                    reply = "Be careful, not all players have entered their scores yet :eyes:\n" \
                            "To bypass this use `?next force`."

        else:
            reply = "The quiz hasn't started yet, {0.author.mention} :upside_down:"

        return reply

    def add_player(self, user):
        """
        Adds a player to the quiz.

        :param user: user to be added.
        """
        new_player = player.Player(user)
        self.players.append(new_player)

    def contains_player(self, user):
        """
        Checks if given player is part of quiz.

        :param user: user to be checked.
        :return: player object if part of quiz - None if not.
        """
        for p in self.players:
            if p.user == user:
                return p

        return None

    def sort_players(self):
        """
        Sorts players into descending score order.
        """
        self.players.sort(key=lambda p: p.points, reverse=True)

    def __read_file(self):
        """
        Reads the quiz file.

        :return: rounds of the quiz.
        """
        filename = message.quiz_dir + "/" + self.name

        with open(filename) as data:
            raw = data.read()

        quiz_data = json.loads(raw)

        rounds = []

        for quiz_round in quiz_data:
            name = quiz_round["name"]
            is_music = quiz_round["is_music"]
            questions = []
            for question in quiz_round["questions"]:
                question_dict = question
                questions.append(question_dict)

            rounds.append(_Round(name, questions, is_music))

        return rounds


class _Round:
    def __init__(self, name, questions, is_music):
        """
        Initialises a quiz round.

        :param name: name of round.
        :param questions: list of round questions (each a dict of "question" and "answer" attributes).
        :param is_music: whether the round is a music round.
        """
        if questions is not None:
            self.questions = questions
        else:
            self.questions = []

        self.name = name
        self.is_linking = False

        if is_music is not None:
            self.is_music = is_music
        else:
            self.is_music = False

    def add_question(self, question_text, answer):
        """
        Adds a question to the round.

        :param question_text: the question content.
        :param answer: the question answer.
        """
        self.questions.append({"question": question_text, "answer": answer})

    # TODO: edit and remove questions functionality.


class CreateQuiz:
    def __init__(self):
        """
        Initialises an object to temporarily hold a quiz at the creation stage.
        """
        self.name = ""
        self.rounds = []
        self.current_round = None
        self.current_question = ""

    def set_name(self, name):
        """
        Sets the name of the quiz.

        :param name: the name of the quiz.
        """
        self.name = name

    def create_question(self, question_text):
        """
        Adds a question (without answer) to the quiz.

        :param question_text: the content of the question.
        """
        self.current_question = question_text

    def add_question(self, answer):
        """
        Commits a question to the round by adding its answer.

        :param answer: the answer to the previous question.
        """
        self.current_round.add_question(self.current_question, answer)
        self.current_question = ""

    def toggle_music(self):
        """
        Toggles whether the round is a music round.
        """
        self.current_round.is_music = not self.current_round.is_music

    def next_round(self, name):
        """
        Commits the previous round and creates a new one.

        :param name: the name of the new round.
        """
        self.__finish_round()
        self.current_round = _Round(name, None, None)

    def __finish_round(self):
        """
        Commits the current round to the quiz.
        """
        if self.current_round is not None:
            self.rounds.append(self.current_round)

    def finish(self):
        """
        Commits the created quiz to storage.
        """
        self.__finish_round()

        filename = message.quiz_dir + "/" + self.name + ".quiz"

        rounds = []

        # Note: 'round' is a protected attribute.
        for quiz_round in self.rounds:
            round_dict = {
                "name": quiz_round.name,
                "is_music": quiz_round.is_music,
                "questions": quiz_round.questions
            }

            rounds.append(round_dict)

        with open(filename, "a+") as file:
            json.dump(rounds, file, indent=2)


# Necessary to allow user select state.
class SelectQuiz:
    pass
