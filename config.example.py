# Config
config = {}
config["discord_token"] = "" # TO FILL
config["inara_api_key"] = ""
config["inara_appname"] = ""
config["inara_cmdr_name"] = ""
config["prefix"] = "!"
config['DEBUG'] = False
config['LANGUAGE'] = "en"

# Admin ids (put the ids directly, not in strings)
admin_ids = []

# Daily BGS update channel id
channel_for_daily_post = ''
# we also want its name
channel_for_daily_post_name = 'oracle'

# Followed factions, find the ids on inara by searching for your faction
# here : https://inara.cz/galaxy-minorfaction/
# Once you are on the desired faction page, hover over the "edit" link and do a right-click
# example : https://inara.cz/galaxy-minorfaction-edit/12345/
# Finally, note that id at the end (here 12435), and also use the scissors icon to copy the exact name of the faction
# Make sure the ids are the correct ones, and that the paste names are exactly the same shown on EDSM
followed_factions = {12345: "Exact displayed name of Faction 1", 67890: "Exact displayed name of Faction 2"}
