from main import _

inara_ranks = {}

inara_ranks['combat'] = {
0: "Inoffensif",
1: "Bleu",
2: "Novice",
3: "Compétent",
4: "Expert",
5: "Maître",
6: "Vétéran",
7: "Létal",
8: "Elite"
}

inara_ranks['trade'] = {
0: "Sans le sou",
1: "Mendiant",
2: "Boutiquier",
3: "Revendeur",
4: "Marchand",
5: "Courtier",
6: "Entrepreneur",
7: "Magnat",
8: "Elite"
}

inara_ranks['exploration'] = {
0: "Vagabond",
1: "Touriste",
2: "Voyageur",
3: "Éclaireur",
4: "Prospecteur",
5: "Découvreur",
6: "Navigateur",
7: "Pionnier",
8: "Elite"
}

inara_ranks['cqc'] = {
0: "Irrécupérable",
1: "Quasi irrécupérable",
2: "Amateur(ice)",
3: "Semi-professionnel(le)",
4: "Professionnel(le)",
5: "Champion",
6: "Héros/Héroïne",
7: "Légende",
8: "Elite"
}

inara_ranks['federation'] = {
0: "Recrue",
1: "Cadet",
2: "Matelot",
3: "Second maître",
4: "Premier maître",
5: "Major",
6: "Enseigne",
7: "Lieutenant",
8: "Capitaine de corvette",
9: "Capitaine de frégate",
10: "Capitaine de vaisseau",
11: "Contre-Amiral",
12: "Vice-Amiral",
13: "Amiral"
}

inara_ranks['empire'] = {
0: "Étranger",
1: "Serf",
2: "Vilain",
3: "Écuyer",
4: "Chevalier",
5: "Banneret",
6: "Baron",
7: "Vicomte",
8: "Comte",
9: "Marquis",
10: "Duc",
11: "Archiduc",
12: "Prince",
13: "Roi"
}

materials = {}

materials['fer'] = {
    'column': 'J',
    'number': 9,
    'location': _('Matériaux très communs (Geysers: "Amas Asphaltéeen" / Spacetree: "Excroissance de Cordyceps")')
}

materials['nickel'] = {
    'column': 'K',
    'number': 10,
    'location': _('Matériaux très communs (Geysers: "Amas Asphaltéeen" / Spacetree: "Excroissance de Cordyceps")')
}

materials['carbone'] = {
    'column': 'L',
    'number': 11,
    'location': _('Matériaux très communs (Geysers: "Amas Asphaltéeen" / Spacetree: "Excroissance de Cordyceps")')
}

materials['soufre'] = {
    'column': 'M',
    'number': 12,
    'location': _('Matériaux très communs (Geysers: "Amas Asphaltéeen" / Spacetree: "Excroissance de Cordyceps")')
}

materials['phosphore'] = {
    'column': 'N',
    'number': 13,
    'location': _('Matériaux très communs (Geysers: "Amas Asphaltéeen" / Spacetree: "Excroissance de Cordyceps")')
}

materials['chrome'] = {
    'column': 'O',
    'number': 14,
    'location': _('Matériaux communs (Geysers: "Fragments Cristallins" / Spacetree: "Excroissance de Polypore")')
}

materials['manganese'] = {
    'column': 'P',
    'number': 15,
    'location': _('Matériaux communs (Geysers: "Fragments Cristallins" / Spacetree: "Excroissance de Polypore")')
}

materials['zinc'] = {
    'column': 'Q',
    'number': 16,
    'location': _('Matériaux communs (Geysers: "Fragments Cristallins" / Spacetree: "Excroissance de Polypore")')
}

materials['vanadium'] = {
    'column': 'R',
    'number': 17,
    'location': _('Matériaux communs (Geysers: "Fragments Cristallins" / Spacetree: "Excroissance de Polypore")')
}

materials['germanium'] = {
    'column': 'S',
    'number': 18,
    'location': _('Matériaux communs (Geysers: "Fragments Cristallins" / Spacetree: "Excroissance de Polypore")')
}

materials['arsenic'] = {
    'column': 'T',
    'number': 19,
    'location': _('Matériaux (Geyser: "Amas Cristallin" / Spacetree: "Excroissance de Polypore")')
}

materials['tungstene'] = {
    'column': 'U',
    'number': 20,
    'location': _('Matériaux (Geyser: "Amas Cristallin" / Spacetree: "Excroissance de Polypore")')
}

materials['niobium'] = {
    'column': 'V',
    'number': 21,
    'location': _('Matériaux (Geyser: "Amas Cristallin" / Spacetree: "Excroissance de Polypore")')
}

materials['selenium'] = {
    'column': 'W',
    'number': 22,
    'location': _('Matériaux (Geyser: "Amas Cristallin" / Spacetree: "Excroissance de Polypore")')
}

materials['zirconium'] = {
    'column': 'X',
    'number': 23,
    'location': _('Matériaux (Geyser: "Amas Cristallin" / Spacetree: "Excroissance de Polypore")')
}

materials['yttrium'] = {
    'column': 'Y',
    'number': 24,
    'location': _('Matériaux rares (Geysers: "Amas Cristallin" / Spacetree: "Cosse mussidienne")')
}

materials['molybdene'] = {
    'column': 'Z',
    'number': 25,
    'location': _('Matériaux rares (Geysers: "Amas Cristallin" / Spacetree: "Cosse mussidienne")')
}

materials['etain'] = {
    'column': 'AA',
    'number': 26,
    'location': _('Matériaux rares (Geysers: "Amas Cristallin" / Spacetree: "Cosse mussidienne")')
}

materials['mercure'] = {
    'column': 'AB',
    'number': 27,
    'location': _('Matériaux rares (Geysers: "Amas Cristallin" / Spacetree: "Cosse mussidienne")')
}

materials['cadmium'] = {
    'column': 'AC',
    'number': 28,
    'location': _('Matériaux rares (Geysers: "Amas Cristallin" / Spacetree: "Cosse mussidienne")')
}

materials['technetium'] = {
    'column': 'AD',
    'number': 29,
    'location': _('Matériaux très rares (Geysers: "Cristaux Epineux"/ Spacetree: "Excression de Phloème")')
}

materials['tellure'] = {
    'column': 'AE',
    'number': 30,
    'location': _('Matériaux très rares (Geysers: "Cristaux Epineux"/ Spacetree: "Excression de Phloème")')
}

materials['polonium'] = {
    'column': 'AF',
    'number': 31,
    'location': _('Matériaux très rares (Geysers: "Cristaux Epineux"/ Spacetree: "Excression de Phloème")')
}

materials['antimoine'] = {
    'column': 'AG',
    'number': 32,
    'location': _('Matériaux très rares (Geysers: "Cristaux Epineux"/ Spacetree: "Excression de Phloème")')
}

materials['ruthenium'] = {
    'column': 'AH',
    'number': 33,
    'location': _('Matériaux très rares (Geysers: "Cristaux Epineux"/ Spacetree: "Excression de Phloème")')
}

translations = {
    "Federation": _("Federation"),
    "Empire": _("Empire"),
    "Alliance": _("Alliance"),
    "Pilots Federation": _("Pilots Federation"),
    "Independent": _("Independant"),
    "Anarchy": _("Anarchie"),
    "Colony": _("Colony"),
    "Communism": _("Communism"),
    "Confederacy": _("Confederacy"),
    "Cooperative": _("Cooperative"),
    "Corporate": _("Corporate"),
    "Democracy": _("Democracy"),
    "Dictatorship": _("Dictatorship"),
    "Feudal": _("Feudal"),
    "Imperial": _("Imperial"),
    "None": _("None"),
    "Patronage": _("Patronage"),
    "Prison Colony": _("Prison Colony"),
    "Theocracy" : _("Theocracy"),
    "Boom": _("Boom"),
    "Bust": _("Bust"),
    "Civil unrest": _("Civil unrest"),
    "Civil war": _("Civil war"),
    "Civil liberty": _("Civil liberty"),
    "Election": _("Election"),
    "Expansion": _("Expansion"),
    "Famine": _("Famine"),
    "Investment": _("Investment"),
    "Lockdown": _("Lockdown"),
    "Outbreak": _("Outbreak"),
    "Retreat": _("Retreat"),
    "War": _("War"),
    "Workshop (Engineer)": _("Workshop (Engineer)"),
    "Extraction": _("Extraction"),
    "Refinery": _("Refinery"),
    "Industrial": _("Industrial"),
    "High Tech": _("High Tech"),
    "Agriculture": _("Agriculture"),
    "Terraforming": _("Terraforming"),
    "Tourism": _("Tourism"),
    "Service": _("Service"),
    "Military": _("Military"),
    "Rescue": _("Rescue"),
    "Damaged": _("Damaged"),
    "Station Repair": _("Station Repair"),
    "Low": _("Low"),
    "Medium": _("Medium"),
    "High": _("High"),
    "Lawless": _("Lawless"),
    "Black Market": _("Black Market"),
    "Restock": _("Restock"),
    "Refuel": _("Refuel"),
    "Repair": _("Repair"),
    "Universal Cartographics": _("Universal Cartographics"),
    "Search and Rescue": _("Search and Rescue"),
    "Interstellar Factors Contact": _("Interstellar Factors Contact")
}