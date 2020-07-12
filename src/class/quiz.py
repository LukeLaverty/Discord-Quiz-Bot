import json
import message
from player import *


def get_ongoing_quiz(action_items):
    for key in action_items:
        item = action_items[key]
        if isinstance(item, Quiz):
            return item
        else:
            return None


class Quiz:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.round_scores_entered = 0  # Ensures all players have entered their score before progressing.
        self.rounds = self.__read_file()
        self.current_round = -1
        self.current_question = -1

    def start(self) -> str:
        if len(self.players) >= 2:
            reply = message.clear_chat()
            self.current_round += 1
            reply += "*From here on out, use `?next` to move through the quiz!*\n"
            reply += self.next()
        else:
            reply = "You need at least 2 players to join your quiz, {0.author.mention} :family:"

        return reply

    def next(self):
        if self.current_round < len(self.rounds):
            if self.current_question == -1:
                if self.round_scores_entered == len(self.players):
                    self.round_scores_entered = 0
                    reply = "> **Round " + str(self.current_round + 1) + ": " + self.rounds[self.current_round].name + \
                            "**\n "
                    self.current_question += 1
                else:
                    reply = "Be careful, not all players have entered their scores yet :eyes:"

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
                    reply += "The round is over! Please post your answers - my next message will be the correct " \
                             "answers :thumbsup:\n "

            # Displays answers:
            else:
                reply = message.round_answers(self.rounds[self.current_round].questions)
                self.current_question = -1
                self.current_round += 1

        else:
            self.sort_players()
            reply = "We're all done! Lets check in with the final standings:\n"
            reply += message.show_leaderboard(self.players)
            reply += "Congratulations to " + str(self.players[0].user.display_name) + " :tada:\n"
            reply += "You can see the leaderboard again using `?leaderboard`. To finish, use `?drop`!"

        return reply

    def add_player(self, player):
        new_player = Player(player)
        self.players.append(new_player)

    def contains_player(self, player):
        for p in self.players:
            if p.user == player:
                return p

        return None

    def sort_players(self):
        self.players.sort(key=lambda p: p.points, reverse=True)

    def __read_file(self):
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
        self.questions.append({"question": question_text, "answer": answer})

    # TODO: edit and remove questions functionality.


class CreateQuiz:
    def __init__(self):
        self.name = ""
        self.rounds = []
        self.current_round = None
        self.current_question = ""

    def set_name(self, name):
        self.name = name

    def create_question(self, question_text):
        self.current_question = question_text

    def add_question(self, answer):
        self.current_round.add_question(self.current_question, answer)
        self.current_question = ""

    def toggle_music(self):
        self.current_round.is_music = not self.current_round.is_music

    def next_round(self, name):
        self.__finish_round()
        self.current_round = _Round(name, None, None)

    def __finish_round(self):
        if self.current_round is not None:
            self.rounds.append(self.current_round)

    def finish(self):
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
