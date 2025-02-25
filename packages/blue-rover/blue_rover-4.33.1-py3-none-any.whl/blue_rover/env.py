import os
from blue_options.env import load_config, load_env, get_env

load_env(__name__)
load_config(__name__)


BLUE_ROVER_MODEL = get_env("BLUE_ROVER_MODEL")
