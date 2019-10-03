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
 
 ##Installation
 
 Simply clone this repository on a linux or mac machine with python 3.6 installed (Python 2 or Python 3.7+ **won't** work).
 
 Then in a terminal : `./init.sh`
 
 Fill the config.py newly created with all the info needed (I won't cover getting a discord bot or edsm/inara token here).
 
 Finally : `./run.sh`
 
 That's it !
 
 ##Translation
 
 I'm currently trying to add translation to the whole bot be it the command names or the displayed text.
 
 When that will be done, I'll probably add scripts to init/update/compile your translations files (.po) to manage your language.
 
 Note : don't forget to change the `config['LANGUAGE']` value to match your need.