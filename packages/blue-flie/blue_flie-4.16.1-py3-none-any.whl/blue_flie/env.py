from blue_options.env import load_config, load_env, get_env

load_env(__name__)
load_config(__name__)

BLUE_FLIE_CONFIG = get_env("BLUE_FLIE_CONFIG")
