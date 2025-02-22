import os
import sys
import argparse
import mergedeep

from opencos import util

def find_eda_config_yml_fpath(filename:str, package_search_only=False, package_search_enabled=True) -> str:
    '''Locates the filename (.yml) either from fullpath provided or from the sys.path
    opencos package paths.'''

    # Check fullpath, unless we're only checking the installed pacakge dir.
    if package_search_only:
        pass
    elif os.path.exists(filename):
        return os.path.abspath(filename)

    leaf_filename = os.path.split(filename)[1]

    if leaf_filename != filename:
        # filename had subdirs, and we didn't find it already.
        util.error(f'eda_config: Could not find {filename=}')
        return None

    # Search in . or pacakge installed dir
    thispath = os.path.dirname(__file__) # this is not an executable, should be in packages dir.

    if package_search_only:
        paths = [thispath]
    elif package_search_enabled:
        paths = ['', thispath]
    else:
        paths = ['']


    for dpath in paths:
        fpath = os.path.join(dpath, leaf_filename)
        if os.path.exists(fpath):
            return fpath

    util.error(f'eda_config: Could not find {leaf_filename=} in opencos within {paths=}')
    return None


def get_config(filename) -> dict:
    fpath = find_eda_config_yml_fpath(filename)
    user_config = util.yaml_safe_load(fpath)
    return user_config

def get_config_handle_defaults(filename) -> dict:
    user_config = get_config(filename)
    user_config = get_config_merged_with_defaults(user_config)
    return user_config


def get_config_merged_with_defaults(config:dict) -> dict:
    default_fpath = find_eda_config_yml_fpath('eda_config_defaults.yml', package_search_only=True)
    default_config = util.yaml_safe_load(default_fpath)
    mergedeep.merge(default_config, config, strategy=mergedeep.Strategy.REPLACE)
    # This technically mutated updated into default_config, so return that one:
    return default_config



def get_eda_config(args:list) -> (dict, list):
    '''Returns an config dict and a list of args to be passed downstream
    to eda.main and eda.process_tokens.

    Handles args for:
      --debug, --debug-.*
      --config-reduced
      --config-yml=<YAMLFILE>
    '''

    # Set global --debug early before parsing other args:
    if any([x.startswith('--debug') for x in args]):
        util.debug_level = 1
        util.args['debug'] = True

    if len(args) == 0 or (len(args) == 1 and '--debug' in args):
        interactive = True
    else:
        interactive = False

    util.debug(f"eda_config: file: {os.path.realpath(__file__)}")
    util.debug(f"eda_config: args: {args=}")

    # Do some minimal argparsing here, even though we've already looked at --debug.*:
    parser = argparse.ArgumentParser(prog='eda_config', add_help=False, allow_abbrev=False)
    parser.add_argument('--config-reduced', action='store_true',
                        help='Use the reduced feature configuration, same as --config-yml=eda_config_reduced.yml')
    parser.add_argument('--config-yml', default='eda_config_defaults.yml',
                        help='YAML filename to use for configuration')
    try:
        parsed, unparsed = parser.parse_known_args(args + [''])
        unparsed = list(filter(None, unparsed))
    except argparse.ArgumentError:
        return util.error(f'problem attempting to parse_known_args for {args=}')

    args = unparsed

    if parsed.config_reduced:
        util.info(f'eda_config: --config-reduced observed')
        fullpath = find_eda_config_yml_fpath('eda_config_reduced.yml')
        config = get_config(fullpath)
        util.info(f'eda_config: using config: {fullpath}')
        # re-add this parsed arg back to args, so it's seen by class Command and preserved
        # for CommandMulti re-invoking eda. Put it at the front of the list:
        # (effectively: eda --config-yml=<file> <command> <options/args> <targets>)
        if not interactive:
            args.insert(0, '--config-reduced')
    elif parsed.config_yml:
        util.info(f'eda_config: --config-yml={parsed.config_yml} observed')
        fullpath = find_eda_config_yml_fpath(parsed.config_yml)
        config = get_config(fullpath)
        util.info(f'eda_config: using config: {fullpath}')
        if not interactive:
            args.insert(0, '--config-yml=' + fullpath)
    else:
        config = None


    return config, args
