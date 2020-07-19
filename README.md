# Discord-Quiz-Bot
A Discord bot to facilitate a pub quiz through a Discord server.

### Requirements
When added to a server, this bot may only accept commands from and post to a channel named "pub-quiz". \
This specified channel name can be changed from within 'bot.py'.

The discord API token must also be entered in 'bot.py'.

A minimum of 2 players is required to start a quiz.

### Features to Implement
* Editing functionality during and after creation of quizzes;
* Allowing music round (through possible use of Spotify API);
* Allowing players to leave;
* Allowing the quiz to progress through reactions rather than commands.

### Known Issues
* Music rounds are unable to be automated due to music bots not accepting commands from other bots;
* Players can join and enter scores mid-round;
* Joint places in leaderboard are not handled;
* If `?music` is toggled repeatedly the file does not write correctly.