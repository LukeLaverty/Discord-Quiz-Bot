import discord
import re
from command import general, channel, dm

cmd_pattern = re.compile("\\?.+")

TOKEN = ""
client = discord.Client()


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
    if cmd_pattern.match(command):

        author = msg.author

        # Checks if message is direct message.
        if isinstance(msg.channel, discord.DMChannel):

            if "?help".startswith(command):
                message = general.get_help()

            elif "?drop".startswith(command):
                message = dm.exit_action(author)

            elif "?name".startswith(command):
                message = dm.set_name(author, content)

            elif "?round".startswith(command):
                message = dm.set_round(author, content)

            elif "?music".startswith(command):
                message = dm.set_round_music(author)

            elif "?question".startswith(command):
                message = dm.set_question(author, content)

            elif "?answer".startswith(command):
                message = dm.set_answer(author, content)

            elif "?finish".startswith(command):
                message = dm.finish(author)

            elif "?create".startswith(command):
                message = dm.create(author)

            else:
                message = "You can't use that command here :disappointed_relieved:\nSee `?help`."

            if message is None:
                message = "That command is invalid :disappointed_relieved:\nSee `?help`."

            await send_dm(msg.author, message)

        # Else, ensures will only respond to messages from channel named "pub-quiz".
        elif msg.channel == quiz_channel:

            message = None

            if "?help".startswith(command):
                reply = general.get_help()

            elif "?drop".startswith(command):
                reply = channel.exit_action(author)

            elif "?join".startswith(command):
                reply = channel.join(author)

            elif "?start".startswith(command):
                reply = channel.start(author)

            elif "?next".startswith(command):
                reply = channel.quiz_next(author)

            elif "?points".startswith(command):
                reply = channel.points(author, content)

            elif "?leaderboard".startswith(command):
                reply = channel.leaderboard()

            elif "?create".startswith(command):
                reply = channel.create()
                message = dm.channel_create()

            elif "?edit".startswith(command):
                reply = channel.create()
                message = dm.channel_edit()

            elif "?quiz".startswith(command):
                reply = channel.play(author)

            elif re.compile("\\?\\d+").match(command):
                reply = channel.select_quiz(author, command)

            else:
                reply = "You can't use that command here :disappointed_relieved:\nSee `?help`."

            if reply is None:
                reply = "That command is invalid :disappointed_relieved:\nSee `?help`."

            # Adds formatting to message where '{0.author.[...]}' is used.
            reply = reply.format(msg)


            await msg.channel.send(reply)
            # Command message deleted such that quiz questions are not interrupted by bot commands.
            await msg.delete()

            print("Replied to " + msg.author.name)

            if message is not None:
                await send_dm(author, message)


@client.event
async def on_ready():
    for guild in client.guilds:
        print("Loaded into server \"" + guild.name + "\" successfully")


@client.event
async def send_dm(member, content):
    dm_channel = await member.create_dm()
    await dm_channel.send(content)

    print("Direct messaged " + member.name)


client.run(TOKEN)
