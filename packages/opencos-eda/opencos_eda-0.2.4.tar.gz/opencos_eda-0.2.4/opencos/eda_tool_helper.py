
import os
import sys

from opencos import eda, eda_config

# Used by pytest, so we can skip tests if tools aren't present.

def get_config_and_tools_loaded():
    # We have to figure out what tools are avaiable w/out calling eda.main,
    # so we can get some of these using eda_config.get_eda_config()
    config, _ = eda_config.get_eda_config(args=[])
    config = eda.init_config(config=config)
    tools_loaded = config.get('tools_loaded', set()).copy()
    return config, tools_loaded
