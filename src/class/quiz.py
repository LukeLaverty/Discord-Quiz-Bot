import json
from message import quiz_dir, round_answers, show_leaderboard
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
        self.rounds = self.__read_file()
        self.current_round = -1
        self.current_question = -1

    def start(self) -> str:
        self.current_round += 1
        reply = "*From here on out, use `?next` to move through the quiz!*\n"
        reply += self.next()
        return reply

    def next(self) -> str:
        if self.current_round < len(self.rounds):
            # Initialises round:
            if self.current_question == -1:
                reply = "> **Round " + str(self.current_round + 1) + ": " + self.rounds[self.current_round].name + \
                        "**\n "
                self.current_question += 1

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
            elif self.current_question == len(self.rounds[self.current_round].questions):
                reply = "The round is over! Please input your answers using `?score [score]` - my next message will" \
                        " be the correct answers :thumbsup:\n "
                self.current_question += 1  # Allows bot to know round is finished.

            # Displays answers:
            else:
                reply = round_answers(self.rounds[self.current_round].questions)
                self.current_question = -1
                self.current_round += 1

        else:
            reply = "We're all done! Lets check in with the final standings:\n"
            reply += show_leaderboard(self.players)
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

    def __read_file(self):
        filename = quiz_dir + "/" + self.name

        with open(filename) as data:
            raw = data.read()

        quiz_data = json.loads(raw)

        rounds = []

        for quiz_round in quiz_data:
            round_data = quiz_data[quiz_round]
            name = round_data["name"]
            is_music = round_data["is_music"]
            questions = []
            for question in round_data["questions"]:
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

        filename = quiz_dir + "/" + self.name + ".quiz"
        tab = "    "

        with open(filename, "a+") as file:
            file.write("{" + "\n")

            round_counter = 1
            # Note: 'round' is a protected attribute.
            for quiz_round in self.rounds:
                if round_counter != 1:
                    file.write(",\n")

                file.write(tab)
                file.write("\"round " + str(round_counter) + "\": {")
                file.write("\n")

                file.write(tab * 2)
                file.write("\"name\": \"" + quiz_round.name + "\",")
                file.write("\n")

                file.write(tab * 2)
                file.write("\"is_music\": " + str(quiz_round.is_music).lower() + ",")
                file.write("\n")

                file.write(tab * 2)
                file.write("\"questions\": [")
                file.write("\n")

                question_counter = 1
                for question in quiz_round.questions:
                    if question_counter != 1:
                        file.write(",\n")
                    file.write(tab * 3)
                    json.dump(question, file)
                    question_counter += 1

                file.write("\n" + tab * 2 + "]" + "\n" + tab + "}")
                round_counter += 1

            file.write("\n}")


# Necessary to allow user select state.
class SelectQuiz:
    pass
