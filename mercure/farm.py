from main import _

# We define all the POI types we need
poi_types = {
    0: _("Other"),
    1: _("Water Magma"),
    2: _("Sulphur Dioxide Magma"),
    3: _("Ammonia Magma"),
    4: _("Methane Magma"),
    5: _("Nitrogen Magma"),
    6: _("Rocky Magma"),
    7: _("Metallic Magma"),
    8: _("Water Geysers"),
    9: _("Carbon Dioxide Geysers"),
    10: _("Ammonia Geysers"),
    11: _("Methane Geysers"),
    12: _("Nitrogen Geysers"),
    13: _("Helium Geysers"),
    14: _("Silicate Vapour Geysers"),
    15: _("Abandoned Settlement"),
    16: _("Crashed ship"),
    17: _("Crashed xeno ship"),
}

# We initialize the farm list of dicts
farm = []

# Then we add entries to it. Just copy this whole block to add entries to the list.
# Reorder the blocks to change the displayed order when the farm command is called
farm.append(
    {
         'discoveredby': "", 'closeToBubble': True,
         'systemname': "Maia", 'body': "B 1 A A", "type": poi_types[14],
         'distanceFromBubble': 545, 'distanceFromColonia': 0, 'distanceFromArrival': 0,
         'minerals':
            {
                _("iron"): 18.5, _("nickel"): 14, _("carbon"): 17.4, _("sulfur"): 20.7, _("phosphorus"): 11.1,
                _("chromium"): 8.3, _("manganese"): 0, _("zinc"): 0, _("vanadium"): 4.5, _("germanium"): 0,
                _("arsenic"): 0, _("tungsten"): 1, _("niobium"): 0, _("selenium"): 0, _("zirconium"): 2.1,
                _("yttrium"): 1.1, _("molydbenum"): 1.2, _("tin"): 0, _("mercury"): 0, _("cadmium"): 0,
                _("technetium"): 0, _("tellurium"): 0, _("polonium"): 0, _("antimony"): 0, _("ruthenium"): 4.1,
            }
    }
)
farm.append(
    {
         'discoveredby': "", 'closeToBubble': False,
         'systemname': "", 'body': "",
         'distanceFromBubble': 0, 'distanceFromColonia': 0, 'distanceFromArrival': 0,
         'minerals':
            {
                _("iron"): 0, _("nickel"): 15.3, _("carbon"): 0, _("sulfur"):0, _("phosphorus"): 0,
                _("chromium"): 0, _("manganese"): 0, _("zinc"): 0, _("vanadium"): 0, _("germanium"): 0,
                _("arsenic"): 0, _("tungsten"): 0, _("niobium"): 0, _("selenium"): 0, _("zirconium"): 0,
                _("yttrium"): 0, _("molydbenum"): 0, _("tin"): 0, _("mercury"): 0, _("cadmium"): 0,
                _("technetium"): 0, _("tellurium"): 0, _("polonium"): 0, _("antimony"): 0, _("ruthenium"): 4.1,
            }
    }
)

def module():
    pass