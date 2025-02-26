from antelop.connection import import_schemas, connect
from antelop.utils.os_utils import get_config
import getpass

config = get_config()
if config is None:
    print("Config file not found.")
    print("Please run `antelop-config` to generate a configuration file.")
    exit()

username = input("Please enter your username: ")
password = getpass.getpass("Please enter your password: ")

conn = connect.dbconnect(username, password)
tables = import_schemas.schema(conn)

# predefine experimenters
experimenters = [
    ["rbedford", "Rory Bedford", "Tripodi Lab", "MRC LMB", "True"],
    ["mtripodi", "Marcoo Tripodi", "Tripodi Lab", "MRC LMB", "True"],
    ["ewilliams", "Elena Williams", "Tripodi Lab", "MRC LMB", "False"],
    ["dwelch", "Daniel Welch", "Tripodi Lab", "MRC LMB", "False"],
    ["dmalmazet", "Daniel de Malmazet", "Tripodi Lab", "MRC LMB", "False"],
    ["lgeyer", "Lynn Geyer", "Tripodi Lab", "MRC LMB", "False"],
    ["yuanxinz", "Yuanxin Zhang", "Tripodi Lab", "MRC LMB", "False"],
    ["srogers", "Stefan Rogers-Coltman", "Tripodi Lab", "MRC LMB", "False"],
    ["arueda", "Ana Gonzalez-Rueda", "Tripodi Lab", "MRC LMB", "False"],
    ["yyu", "Yujiao Yu", "Tripodi Lab", "MRC LMB", "False"],
    ["fmorgese", "Fabio Morgese", "Tripodi Lab", "MRC LMB", "False"],
]

# insert into the experimenter table
tables["Experimenter"].insert(experimenters, skip_duplicates=True)
