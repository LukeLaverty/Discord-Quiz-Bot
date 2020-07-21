import discord
import re
# Local modules.
import quiz
from command import general, channel, dm

TOKEN = "NzI0Mjc5ODAxNjk4ODQ0NzIz.XxCCMA.tDM9uFv7Y9AL9RAmJucgyPljS5M"
client = discord.Client()

# Dictionary associates each user with an action class.
action_items = {}

# Pattern to check message is a bot command.
cmd_pattern = re.compile("\\?.+")


@client.event
async def on_message(msg):
    """
    Initial message handling.

    :param msg: content of the message.
    """
    quiz_channel = discord.utils.get(client.get_all_channels(), name="pub-quiz")  # Name of channel for bot.

    # Splits user input into command message and command content.
    splits = msg.content.split(" ", 1)
    command = splits[0].lower()
    if len(splits) > 1:
        content = splits[1]
    else:
        content = ""

    # Ensures message is of the command format.
    if cmd_pattern.search(command) is not None:

        author = msg.author

        # Checks if message is direct message.
        if isinstance(msg.channel, discord.DMChannel):

            # General commands.
            if "?help".startswith(command):
                message = general.get_help()

            elif "?drop".startswith(command):
                message = general.exit_action(author, action_items)

            else:

                current_action = action_items.get(author)

                # Commands when creating a quiz.
                if isinstance(current_action, quiz.CreateQuiz):

                    if "?name".startswith(command):
                        message = dm.set_name(author, current_action, content)

                    elif "?round".startswith(command):
                        message = dm.set_round(current_action, content)

                    elif "?music".startswith(command):
                        message = dm.set_round_music(current_action)

                    elif "?picture".startswith(command):
                        message = dm.set_round_picture(current_action)

                    elif "?question".startswith(command):
                        message = dm.set_question(current_action, content)

                    elif "?answer".startswith(command):
                        message = dm.set_answer(current_action, content)

                    elif "?finish".startswith(command):
                        message = dm.finish(author, action_items)

                    else:
                        message = "You can't use this command while creating a quiz :upside_down:"

                else:

                    if "?create".startswith(command):
                        message = dm.create(author, action_items)

                    else:
                        message = "You can't use that command here :disappointed_relieved:\nSee `?help`."

            if message is None:
                message = "That command is invalid :disappointed_relieved:\nSee `?help`."

            await send_dm(msg.author, message)

        # Else, ensures will only respond to messages from channel named "pub-quiz".
        elif msg.channel == quiz_channel:

            message = None

            # General commands:
            if "?help".startswith(command):
                reply = general.get_help()

            elif "?drop".startswith(command):
                reply = general.exit_action(author, action_items)

            else:

                current_action = action_items.get(author)

                # Commands during ongoing quiz:
                if quiz.get_ongoing_quiz(action_items) is not None:

                    if "?start".startswith(command):
                        reply = channel.start(current_action)

                    elif "?join".startswith(command):
                        reply = channel.join(author, action_items)

                    elif "?quit".startswith(command):
                        reply = channel.leave(author, action_items)

                    elif "?next".startswith(command):
                        reply = channel.quiz_next(current_action, content)

                    elif "?points".startswith(command):
                        reply = channel.points(author, action_items, content)

                    elif "?leaderboard".startswith(command):
                        reply = channel.leaderboard(action_items)

                    else:
                        reply = "You cannot use this command during a quiz :upside_down:"

                # Commands when no quiz is ongoing:
                else:

                    if "?create".startswith(command):
                        reply = channel.create()
                        message = dm.channel_create()

                    elif "?edit".startswith(command):
                        reply = channel.create()
                        message = dm.channel_edit()

                    elif "?play".startswith(command):
                        reply = channel.play(author, action_items)

                    elif re.compile("\\?\\d+").match(command):
                        reply = channel.select_quiz(author, action_items, command)

                    else:
                        reply = "You can't use that command here :disappointed_relieved:\nSee `?help`."

            if reply is None:
                reply = "That command is invalid :disappointed_relieved:\nSee `?help`."

            # Adds formatting to message where '{0.author.[...]}' is used.
            reply = reply.format(msg)

            # Checks for image link to embed image.
            if reply.startswith("http"):
                embed = discord.Embed()
                embed.set_image(url=reply)
                await msg.channel.send(embed=embed)
            else:
                await msg.channel.send(reply)
            # Command message deleted such that quiz questions are not interrupted by bot commands.
            await msg.delete()

            print("Replied to " + msg.author.name)

            if message is not None:
                await send_dm(author, message)


@client.event
async def on_ready():
    """
    Checks bot loads into servers successfully.
    """
    for guild in client.guilds:
        print("Loaded into server \"" + guild.name + "\" successfully")


@client.event
async def send_dm(member, content):
    """
    Sends a direct message to a user.

    :param member: user to which message should be sent.
    :param content: the content of the message.
    """
    dm_channel = await member.create_dm()
    await dm_channel.send(content)

    print("Direct messaged " + member.name)


client.run(TOKEN)
