import argparse
import os
import shutil
import sys
import tomllib
import yaml
import zmq
import platformdirs
from pathlib import Path
from typing import Any, Optional
from .plugin import Plugin


APP_NAME = 'ReOxide'
APP_AUTHOR = 'ReOxide'


def unpack_name(
    plugins: list[Plugin],
    name: str,
    action: bool,
    message: list[bytes]
) -> bool:
    plug_id = None
    name_id = None

    for i, p in enumerate(plugins):
        lookup = p.actions
        if not action:
            lookup = p.rules

        nid = lookup.get(name)
        if nid is not None:
            name_id = nid
            plug_id = i
            message.append(plug_id.to_bytes(2, 'little'))
            message.append(name_id.to_bytes(2, 'little'))
            return True
    return False


def unpack_action_rule(message: list[bytes], action: Any):
    if 'group' not in action:
        message.append(b'')
    else:
        message.append(action['group'].encode())
    if 'extra_args' not in action:
        message.append(b'\x00')
        return

    arg_count = len(action['extra_args'])
    message.append(arg_count.to_bytes())
    for arg in action['extra_args']:
        match arg['type']:
            case "bool":
                message.append(b'b')
                message.append(arg['value'].to_bytes())


def pipeline_to_message(
    message: list[bytes],
    plugins: list[Plugin],
    pipeline: Any
):
    for step in pipeline:
        if 'action' in step:
            tmp_msg = []
            name_found = unpack_name(
                plugins,
                step['action'],
                True,
                tmp_msg
            )
            if not name_found:
                print(f'Could not find action {step["action"]}')

            message.append(b'a')
            message.extend(tmp_msg)
            unpack_action_rule(message, step)
        elif 'action_group' in step:
            message.append(b'g')
            message.append(step['action_group'].encode())
            pipeline_to_message(message, plugins, step['actions'])
            message.append(b'e')
        elif 'pool' in step:
            message.append(b'p')
            message.append(step['pool'].encode())
            for rule in step['rules']:
                tmp_msg = []
                name_found = unpack_name(
                    plugins,
                    rule['rule'],
                    False,
                    tmp_msg
                )
                if not name_found:
                    print(f'Could not find rule {rule["rule"]}')
                    continue
                message.append(b'r')
                message.extend(tmp_msg)
                unpack_action_rule(message, rule)
            message.append(b'e')


def ghidra_decomp_path(ghidra_root: Path) -> Optional[Path]:
    p = ghidra_root / 'Ghidra' / 'Features' / 'Decompiler' / 'os'
    p = p / 'linux_x86_64' / 'decompile'
    return p if p.exists() and p.is_file() else None


def client_cli():
    parser = argparse.ArgumentParser()
    parser.description = 'Client program for the ReOxide daemon.'
    parser.add_argument(
        '--config',
        type=str,
        help='Specify path to config (reoxide.toml) instead of default path'
    )
    cmd_parser = parser.add_subparsers(dest="cmd", required=True)

    link_desc = 'Replace the Ghidra decompile binary with a symlink to ReOxide'
    cmd_parser.add_parser(
        'link-ghidra',
        description=link_desc,
        help=link_desc
    )

    args = parser.parse_args()

    if args.config:
        config_path = Path(args.config)
    else:
        config_dir = platformdirs.user_config_path(APP_NAME, APP_AUTHOR)
        config_path = config_dir / 'reoxide.toml'

    if not config_path.exists() or not config_path.is_file():
        exit(f'Config file does not exist: {config_path}')

    config = dict()
    with config_path.open('rb') as f:
        try:
            config = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            exit(f'Could not parse {config_path}: {e}')

    if 'reoxide' not in config or 'bin-dir' not in config['reoxide']:
        exit('No ReOxide bin-dir specified in reoxide.toml')

    reoxide_bin = Path(config['reoxide']['bin-dir']) / 'decompile'
    if not reoxide_bin.exists():
        exit('No "decompile" binary in specified ReOxide bin-dir')

    try:
        reoxide_bin = reoxide_bin.resolve(strict=True)
    except OSError:
        exit('Could not resolve path to ReOxide binary')

    if 'ghidra-install' not in config:
        msg = 'No Ghidra installation info (ghidra-install) found in '
        msg += f'{config_path}. Need at least one!'
        exit(msg)

    for ghidra_install in config['ghidra-install']:
        ghidra_root = Path(ghidra_install['root-dir'])
        print(f'Trying to link {ghidra_root}')

        ghidra_decomp = ghidra_decomp_path(ghidra_root)
        if not ghidra_decomp:
            print(f'WARNING: No decompiler found for {ghidra_root}, skipping')
            continue

        if ghidra_decomp.is_symlink():
            try:
                decomp_resolved = ghidra_decomp.resolve(strict=True)
            except OSError:
                print(f'Could not resolve symlink for {ghidra_decomp}')
                continue

            if decomp_resolved != reoxide_bin:
                print(f'WARNING: Ghidra directory {ghidra_root}' +\
                    'has a decompile symlink that does point to ReOxide')
                continue

            print(f'Ghidra directory {ghidra_root} already linked')
            continue

        try:
            os.rename(
                ghidra_decomp,
                ghidra_decomp.with_name('decompile.orig')
            )
        except OSError:
            print(
                f'Could not rename {ghidra_decomp}, skipping {ghidra_root}',
                file=sys.stderr
            )
            continue

        try:
            ghidra_decomp.symlink_to(reoxide_bin)
        except OSError:
            print(
                f'Could not create ReOxide symlink, skipping {ghidra_root}',
                file=sys.stderr
            )
            continue

        print(f'Successfully linked {ghidra_root}')


def install_data():
    base = Path(__file__).parent.resolve() / 'data'
    data_dir = platformdirs.user_data_path(APP_NAME, APP_AUTHOR)
    bin_dir = data_dir / 'bin'
    plugin_dir = data_dir / 'plugins'

    bin_dir.mkdir(parents=True, exist_ok=True)
    plugin_dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(base / 'bin', data_dir / 'bin', dirs_exist_ok=True)
    shutil.copytree(base / 'plugins', data_dir / 'plugins', dirs_exist_ok=True)
    shutil.copy(base / 'default.yaml', data_dir)


def main_cli():
    data_dir = platformdirs.user_data_path(APP_NAME, APP_AUTHOR)
    cache_dir = platformdirs.user_cache_path(APP_NAME, APP_AUTHOR)
    config_dir = platformdirs.user_config_path(APP_NAME, APP_AUTHOR)
    plugin_dir = data_dir / 'plugins'
    plugin_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)

    install_data()

    config_path = config_dir / 'reoxide.toml'
    if not config_path.exists():
        print(f'Config file not found at "{config_path}"')
        print('Creating new basic config.')
        ghidra_root = input('Enter a Ghidra root install directory: ')

        ghidra_root = Path(ghidra_root)
        if not ghidra_root.exists():
            exit('Entered Ghidra root directory does not exist.')

        ghidra_decomp = ghidra_decomp_path(ghidra_root)
        if not ghidra_decomp:
            msg = 'Entered Ghidra root does not contain decompiler.'
            msg += f' Tried path: {ghidra_decomp}'
            exit(msg)

        with config_path.open('w', encoding='utf-8') as f:
            print('[reoxide]', file=f)
            print('bin-dir = {data_dir / "bin"}', file=f)
            print('[[ghidra-install]]', file=f)
            print(f'root-dir = "{ghidra_root}"', file=f)

        print(f'Config saved to {config_path}')

    config = dict()
    with config_path.open('rb') as f:
        try:
            config = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            exit(f'Could not parse {config_path}: {e}')

    if 'ghidra-install' not in config:
        msg = 'No Ghidra installation info (ghidra-install) found in '
        msg += f'{config_path}. Need at least one!'
        exit(msg)

    for ghidra_install in config['ghidra-install']:
        ghidra_root = Path(ghidra_install['root-dir'])
        ghidra_decomp = ghidra_decomp_path(ghidra_root)
        if not ghidra_decomp:
            print(f'WARNING: No decompiler found for {ghidra_root}')
            continue

        if not ghidra_decomp.is_symlink():
            print(f'WARNING: decompile file is not a symlink')
            continue

    default_actions_path = data_dir / 'default.yaml'
    default_actions = None
    if default_actions_path.exists() and default_actions_path.is_file():
        with default_actions_path.open() as f:
            try:
                default_actions = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print('Error while loading default rules from yaml:')
                print(exc)

    plugins = []
    for plugin in plugin_dir.glob('*.so'):
        if not plugin.is_file():
            print(f'Skipping {plugin} in plugin directory...')
            continue

        p = Plugin.load_shared_lib(plugin)
        if p is None:
            print(f'Could not load plugin {plugin}')
            continue

        plugins.append(p)

    ctx = zmq.Context()
    router = ctx.socket(zmq.ROUTER)
    router.bind("ipc:///tmp/reoxide.sock")

    poller = zmq.Poller()
    poller.register(router, zmq.POLLIN)

    while True:
        try:
            socks = dict(poller.poll())
        except KeyboardInterrupt:
            break

        if router not in socks:
            continue

        msg_parts = router.recv_multipart()
        client_id = msg_parts[0]
        data = msg_parts[2:]

        match data[0]:
            case b'\x00':
                print('Decompiler registered, loading plugins')
                msg_parts = [client_id, b'']

                # TODO: Do some sanity checking to make sure we are
                # not sending garbage to the decompiler process (or
                # let the decompiler handle it)
                plugin_paths = [
                    str(p.file_path).encode()
                    for p in plugins
                ]

                # Make sure we at least send an empty message if we
                # don't have any plugins to load
                if plugin_paths:
                    msg_parts.extend(plugin_paths)
                else:
                    msg_parts.append(b'')

                router.send_multipart(msg_parts)
            case b'\x01':
                msg_parts = [client_id, b'']
                pipeline_to_message(msg_parts, plugins, default_actions)
                router.send_multipart(msg_parts)
            case _:
                print(data[0].decode())
                router.send_multipart([client_id, b'', b'OK'])
