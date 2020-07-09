# Discord-Quiz-Bot
A Discord bot to facilitate a pub quiz through a Discord server.

### Requirements
When added to a server, this bot may only accept commands from and post to a channel named "pub-quiz". \
This specified channel name can be changed from within 'bot.py'.

The discord API token must also be entered in 'bot.py'.

### Features to Implement
* Editing functionality during and after creation of quizzes;
* Ensuring file validity, and that only files ending '.quiz' are displayed;
* Allowing music round (through possible use of Spotify API);
* Displaying questions in random order;
* Ensuring a minimum number of players before proceeding;
* Ensuring all players have entered their score each round before proceeding;
* Message formatting improvements.

### Known Issues
* Music rounds are unable to be automated due to music bots not accepting commands from other bots;
* Exception is thrown if file name is invalid - not handled;
* If `?music` is toggled repeatedly the file does not write correctly.