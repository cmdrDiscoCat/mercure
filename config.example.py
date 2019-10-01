# Config
config = {}
config["discord_token"] = "" # TO FILL
config["inara_api_key"] = ""
config["inara_appname"] = ""
config["prefix"] = "!"

# Admin ids
admin_ids = []

# Daily BGS update channel
channel_for_daily_post = ''

# Followed factions, find the ids on inara by searching for your faction
# here : https://inara.cz/galaxy-minorfaction/
# Once you are on the desired faction page, hover over the "edit" link and do a right-click
# example : https://inara.cz/galaxy-minorfaction-edit/12345/
# Finally, note that id at the end (here 12435)
# In the daily "bigbrother" function, the value assigned to each id
followed_factions = {12345: "Displayed name for Faction 1", 67890: "Displayed name for Faction 2"}
