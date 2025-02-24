"""List of static, unchanging consts.

    REQ_URL: hexal.de request URL
    ENG_LIST: the english translation of the array of allergens from the site.
    SHORT_OPT: command line options called with a single dash.
    LONG_OPT: command line options called with a double dash.
"""

REQ_URL = "https://allergie.hexal.de/pollenflug/vorhersage/load_pollendaten.php"
ENG_LIST = [
    "Ambrosia",
    "Dock",
    "Artemisia",
    "Birch",
    "Beech",
    "Oak",
    "Alder",
    "Ash",
    "Grass",
    "Hazel",
    "Popplar",
    "Rye",
    "Elm",
    "Plantain",
    "Willow",
]

# Define input options
SHORT_OPT = "d:p:hve"
LONG_OPT = ["date=", "plz=", "help", "verbose", "english"]
