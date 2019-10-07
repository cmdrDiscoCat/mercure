from main import _

# EDSM Constants and parameters for the body search used in the farm command
# https://www.edsm.net/en/search/bodies/index/cmdrPosition/Pytheas/

# Group values for that search
EDSM_STARS = 1
EDSM_BODIES = 2

# Material values for that search
minerals = {
    _("antimony"):1,
    _("arsenic"):2,
    _("cadmium"):3,
    _("carbon"):4,
    _("chromium"):5,
    _("germanium"):6,
    _("iron"):7,
    _("manganese"):8,
    _("mercury"):9,
    _("molybdenum"):10,
    _("nickel"):11,
    _("niobium"):12,
    _("phosphorus"):13,
    _("polonium"):14,
    _("ruthenium"):15,
    _("selenium"):16,
    _("sulphur"):17,
    _("technetium"):18,
    _("tellurium"):19,
    _("tin"):20,
    _("tungsten"):21,
    _("vanadium"):22,
    _("yttrium"):23,
    _("zinc"):24,
    _("zirconium"):25,
}

# Material values for that search
stars_types = {
    1: _("O (Blue-White) Star"),
    2: _("B (Blue-White) Star"),
    201: _("B (Blue-White super giant) Star"),
    3: _("A (Blue-White) Star"),
    301: _("A (Blue-White) Star"),
    4: _("F (White) Star"),
    401: _("F (White super giant) Star"),
    5: _("G (White-Yellow) Star"),
    5001: _("G (White-Yellow super giant) Star"),
    6: _("K (Yellow-Orange) Star"),
    601: _("K (Yellow-Orange super giant) Star"),
    7: _("M (Red dwarf) Star"),
    701: _("M (Red giant) Star"),
    702: _("M (Red super giant) Star"),
    8: _("L (Brown dwarf) Star"),
    9: _("T (Brown dwarf) Star"),
    10: _("Y (Brown dwarf) Star"),
    11: _("T Tauri Star"),
    12: _("Herbig Ae/Be Star"),
    21: _("Wolf-Rayet Star"),
    22: _("Wolf-Rayet N Star"),
    23: _("Wolf-Rayet NC Star"),
    24: _("Wolf-Rayet C Star"),
    25: _("Wolf-Rayet O Star"),
    31: _("CS Star"),
    32: _("C Star"),
    33: _("CN Star"),
    34: _("CJ Star"),
    35: _("CH Star"),
    36: _("CHd Star"),
    41: _("MS-type Star"),
    42: _("S-type Star"),
    51: _("White Dwarf (D) Star"),
    501: _("White Dwarf (DA) Star"),
    502: _("White Dwarf (DAB) Star"),
    503: _("White Dwarf (DAO) Star"),
    504: _("White Dwarf (DAZ) Star"),
    505: _("White Dwarf (DAV) Star"),
    506: _("White Dwarf (DB) Star"),
    507: _("White Dwarf (DBZ) Star"),
    508: _("White Dwarf (DBV) Star"),
    509: _("White Dwarf (DO) Star"),
    510: _("White Dwarf (DOV) Star"),
    511: _("White Dwarf (DQ) Star"),
    512: _("White Dwarf (DC) Star"),
    513: _("White Dwarf (DCV) Star"),
    514: _("White Dwarf (DX) Star"),
    91: _("Neutron Star"),
    92: _("Black Hole"),
    93: _("Supermassive Black Hole"),
    94: _("X"),
    111: _("Rogue Planet"),
    112: _("Nebula"),
    113: _("Stellar Remnant Nebula"),
}

# We define all the volcanism types we need
volcanism_types = {
    0: _("No volcanism"),
    1: _("Water Magma"),
    11: _("Sulphur Dioxide Magma"),
    21: _("Ammonia Magma"),
    31: _("Methane Magma"),
    41: _("Nitrogen Magma"),
    51: _("Rocky Magma"),
    61: _("Metallic Magma"),
    71: _("Water Geysers"),
    81: _("Carbon Dioxide Geysers"),
    91: _("Ammonia Geysers"),
    101: _("Methane Geysers"),
    111: _("Nitrogen Geysers"),
    121: _("Helium Geysers"),
    131: _("Silicate Vapour Geysers")
}


def module():
    pass