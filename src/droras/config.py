import os

# directory structure
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_DIR = os.path.join(BASE_DIR, "static")
LOG_DIR = os.path.join(BASE_DIR, "log")
SOUND_DIR = os.path.join(BASE_DIR, "sound")
HEAT_LIST_CSV = os.path.join(LOG_DIR, "heat_list.csv")
