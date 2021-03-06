# Config
config = {}
config["discord_token"] = ""  # TO FILL : you'll have to go to discord's dev portal and create a bot there
config["inara_api_key"] = ""  # you can generate this by contact the inara devs to create an app with an api key
config["inara_appname"] = ""  # put here what you told the inara devs the bot's name would be
config["inara_cmdr_name"] = ""  # the name of your commander (the one of the account tied to the api key above)
config["prefix"] = "!"
config['DEBUG'] = False
config['LANGUAGE'] = "en"

# To get the ids of people and channel, go to discord's display options and activate developer mode
# Then, right click on people and channel will allow you to copy their id

# Admin ids (put the ids directly, not in strings).
admin_ids = []

# Daily BGS update channel id
channel_for_daily_post = ''
# we also want its name
channel_for_daily_post_name = 'oracle'
# then the time when you want it to run
daily_time = "16:00"

# Followed factions, find the ids on inara by searching for your faction
# here : https://inara.cz/galaxy-minorfaction/
# Once you are on the desired faction page, hover over the "edit" link and do a right-click
# example : https://inara.cz/galaxy-minorfaction-edit/12345/
# Finally, note that id at the end (here 12435), and also use the scissors icon to copy the exact name of the faction
# Make sure the ids are the correct ones, and that the paste names are exactly the same shown on EDSM
followed_factions = {12345: "Exact displayed name of Faction 1", 67890: "Exact displayed name of Faction 2"}
