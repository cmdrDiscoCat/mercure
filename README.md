# Mercure

New BGS bot for Elite Dangerous factions to use on their discord servers

This is basically the new version of discobot, a BGS bot for Elite Dangerous I initially made for my faction.
 
 This new version comes with:
 * translation support (to use the bot in a different language)
 * No need to manually name all the systems for each faction you want to follow, you just have to fill the dict in the config.py file with the inara id and the exact name for each, and the bot will get the systems 
 * a loop for the bigbrother command : that way it can be launched manually or at a set time with the HH:MM format (see the config.py file) 
 * a more generic name
 * use of the cogs from discord.py to allow reloading parts of it in case of updates with a command to reload the cogs (simple named reload)
 * and more... soon...
 
## Installation
 
Simply clone this repository on a windows, linux or mac machine with python 3.6 installed (Python 2 or Python 3.7+ **won't** work).
 
Then in a terminal : `./init.sh` or `init.bat`
 
Fill the config.py newly created with all the info needed (I won't cover getting a discord bot or edsm/inara token here).
 
Finally : `./run.sh` or `run.bat`

That's it !

_Note_ : You may note that I configured 2 virtualenv : venv for windows, and env for unix-like systems. It's totally normal, and allows you, on windows, to test at the same time on a windows shell AND on a linux distro installed in WSL (Windows Subsystem for Linux or whatever it's called). Can be useful.
 
 
## Translation

You can change the `config['LANGUAGE']` value to match your need and set a language for the bot.
 
Translations are included already but there's a few useful things if Mercure isn't available in your language or if the translations are incomplete. If you want to fix that, there's a few steps to take.

First of all, for all the commands below to work, you must enter the app's virtualenv. Open a terminal and go to the root folder of the project - where this file is located - and then : 
- For windows type `venv\Scripts\activate.bat`.
- For Mac OS and Linux type `source env/bin/activate`

Then, go to the mercure directory : `cd mercure`

You're now ready for the commands below. 

### Initializing a language
 
The command to initialize a language is `python i18n_init.py <language>` where language is a 2 letters code for the country (and the one you'll set in `config['LANGUAGE]`) like `fr` or `es``

This will create the directories and the messages.po file for the language. You can edit translations there (look on the web how .po files work)

### Updating a translate file when new translatable strings are added in the app

The command is `python i18n_update.py`. It will update all the messages.po files it can find.


### Compiling a translate file to see the translations you added

The command is `python i18n_compile.py`. It will compile all the messages.po files it can find.

### Once you're done

On windows type `venv\Scripts\deactivate.bat`. On unix-like systems simply enter `deactivate`.