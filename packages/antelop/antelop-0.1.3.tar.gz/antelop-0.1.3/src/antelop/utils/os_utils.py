from pathlib import Path, PurePosixPath
import platform
import toml
import shutil
import os
import textwrap
import re
import requests


def get_config_path():
    if os.environ.get("ANTELOP_CONFIG_PATH") is None:
        if platform.system() in ["Linux", "Darwin", "Windows"]:
            tmp_config_path = Path.home() / ".config" / "antelope" / "config.toml"
            config_path = Path.home() / ".config" / "antelop" / "config.toml"
            if (
                tmp_config_path.exists()
            ):  # can delete once everyone's moved to new package
                # copy to new path and delete
                config_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(tmp_config_path, config_path)
                tmp_config_path.unlink()

            return config_path

    else:
        config_path = Path(os.environ.get("ANTELOP_CONFIG_PATH"))
        return config_path


def get_config():
    config_path = get_config_path()
    if not config_path.exists():
        return None
    else:
        with open(config_path, "r") as f:
            config = toml.load(f)
        ### The following can be deleted after the workshop
        if 'github' not in config:
            config['github'] = {'trilab-scripts': 'https://github.com/marcotripodi/Trilab-Tools'}
            # rewrite the config file
            with open(config_path, "w") as f:
                toml.dump(config, f)
        ###
        return config


def validate_config_file(config):
    keys = {
        "deployment",
        "mysql",
        "s3",
        "multithreading",
        "computation",
        "folders",
    }
    valid = keys.issubset(config.keys())
    return valid


def cp_st_config():
    if platform.system() in ["Linux", "Darwin", "Windows"]:
        # copy  streamlit config to home if it doesn's exist
        stconfig = Path.home() / ".streamlit" / "config.toml"
        stcredentials = Path.home() / ".streamlit" / "credentials.toml"
        if not stconfig.exists():
            stconfig.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                Path(os.path.abspath(__file__)).parent.parent
                / "configs"
                / ".streamlit"
                / "config.toml",
                stconfig,
            )
        if not stcredentials.exists():
            stcredentials.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                Path(os.path.abspath(__file__)).parent.parent
                / "configs"
                / ".streamlit"
                / "credentials.toml",
                stcredentials,
            )


def github_repo_exists(url):
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)(?:/.*)?", url)
    if not match:
        return False  # invalid url

    owner, repo = match.groups()

    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(api_url)

    return response.status_code == 200  # repo existence


def validate_config(config):
    if config is None:
        print("Config file not found.")
    for name, path in config["folders"].items():
        if not Path(path).exists():
            print(f"Folder {name} not found at {path}")
            return False
    if "analysis" in config:
        for folder in config["analysis"]["folders"]:
            if not Path(folder).exists():
                print(f"Analysis folder not found at {folder}")
                return False
    cluster_install = PurePosixPath(config["computation"]["basedir"])
    if not cluster_install.is_absolute():
        print("Cluster install path must be an absolute path")
        return False
    cluster_data = Path(config["computation"]["antelop_data"])
    if not cluster_data.exists():
        print(
            textwrap.dedent(f"""
            Antelop data folder not found at {cluster_data}.
            This is ok if its your first time running Antelop.
            Do check after running a cluster job if this folder is created
            otherwise you might have gotten the path wrong and won't be able to
            see your cluster results.
        """)
        )
    if "github" in config:
        for key, repo in config["github"].items():
            if not key.isidentifier():
                print(f"Invalid key for GitHub repo: {key}")
                return False
    return True
