import datajoint as dj
from antelop.utils.os_utils import get_config


def dbconnect(username, password):
    """
    Function loads configuration from home and
    returns a connection to the database.
    """

    # load config file
    config = get_config()

    dj.config["database.host"] = config["mysql"]["host"]
    dj.config["database.user"] = username
    dj.config["database.password"] = password
    dj.config["stores"] = {
        "raw_ephys": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelop-external-data",
            "location": "/raw_ephys",
            "access_key": username,
            "secret_key": password,
        },
        "feature_behaviour": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelop-external-data",
            "location": "/features_behaviour",
            "access_key": username,
            "secret_key": password,
        },
        "dlcmodel": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelop-external-data",
            "location": "/dlcmodel",
            "access_key": username,
            "secret_key": password,
        },
        "behaviour_video": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelop-external-data",
            "location": "/behaviour_video",
            "access_key": username,
            "secret_key": password,
        },
        "labelled_frames": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelop-external-data",
            "location": "/labelled_frames",
            "access_key": username,
            "secret_key": password,
        },
        "evaluated_frames": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelop-external-data",
            "location": "/evaluated_frames",
            "access_key": username,
            "secret_key": password,
        },
    }

    conn = dj.conn(reset=True)

    return conn
