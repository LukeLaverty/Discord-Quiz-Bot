# Discord-Quiz-Bot
A Discord bot to facilitate a pub quiz through a Discord server.

### Usage
When added to a server, this bot may only accept commands from and post to a channel named "pub-quiz".  
This specified channel name can be changed from within 'bot.py'.

The discord API token must also be entered in 'bot.py'.

A minimum of 2 players is required to start a quiz.

### Commands
**From anywhere:**  
&nbsp;`?help` will show you this screen, duh.  
&nbsp;`?drop` will cancel any ongoing actions - including your quiz.  
**From a channel:**  
&nbsp;`?create` will prompt you in your DMs to create a new quiz.  
&nbsp;`?edit` will prompt you in your DMs to edit a quiz.  
&nbsp;`?play` will allow you to play your quiz.  
**During a quiz:**  
&nbsp;`?join` will add you to the quiz.  
&nbsp;`?next` will display the next question, answers if at the end of the round, and next round.  
&nbsp;`?points` allows each user to input their score for each round.  
&nbsp;`?leaderboard` will display the current leaderboard.  
&nbsp;`?quit` allows you to leave a quiz midway.  
**From your direct messages:**  
&nbsp;`?create` will prompt you to create a new quiz.  
&nbsp;`?edit` will allow you to edit a pre-existing quiz.  

### Features to Implement
* Editing functionality during and after creation of quizzes;
* Allowing music round (through possible use of Spotify API);
* Allowing the quiz to progress through reactions rather than commands.

### Known Limitations
* Music rounds are unable to be automated due to music bots not accepting commands from other bots.