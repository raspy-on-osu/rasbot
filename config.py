import json

DEFAULT_CHANNEL = {
    "meta": {
        "prefix": "r!"
    },
    "commands": {
        "help": {
            "cooldown": 10,
            "requires_mod": False,
            "hidden": False,
            "response": "@&caller& > &help&"
        },
        "uptime": {
            "cooldown": 10,
            "requires_mod": False,
            "hidden": False,
            "response": "@&caller& > &uptime&"
        },
        "cmdadd": {
            "cooldown": 0,
            "requires_mod": True,
            "hidden": False,
            "response": "@&caller& > &cmdadd&"
        },
        "cmddel": {
            "cooldown": 0,
            "requires_mod": True,
            "hidden": False,
            "response": "@&caller& > &cmddel&"
        },
        "prefix": {
            "cooldown": 0,
            "requires_mod": True,
            "hidden": False,
            "response": "@&caller& > &prefix&"
        },
    },
    "modules": []
}
"""Default channel config."""

DEFAULT_GLOBAL = {
    "always_debug": False,
    "default_authfile": "config/auth",
    "release_branch": "main",
    "channels": [],
}


def read_global() -> dict:
    """Reads the global config file.
    """
    return read("config/rasbot", DEFAULT_GLOBAL)


def read_channel(cfg: str) -> dict:
    """Reads the config file for a given channel ID.

    :param cfgid: The path to the channels' config.
    """
    path = f"config/{cfg}"
    return read(path, DEFAULT_CHANNEL)


def read(cfg: str, default: dict) -> dict:
    """Read a file and return the contained json.

    :param cfg: The path to the file.

    :param default: Default to write to file if the path does not exist.
    """
    # Attempt to read config
    try:
        with open(cfg, 'r') as cfgfile:
            config = json.loads(cfgfile.read())
            return config

    # If no config file is found, write the default,
    # and return a basic config dict.
    except FileNotFoundError:
        with open(cfg, 'w') as cfgfile:
            cfgfile.write(json.dumps(default, indent=4))
            return default


def write_channel(bot):
    """Generates then writes the config file for the given TwitchBot.

    :param bot: The TwitchBot to write the config for.
    """
    bot.log_debug("config", f"writing for {bot.channel_id}")

    path = f"config/{bot.cfgpath}"

    # Append prefix to lines
    data = {
        'meta': {
            'prefix': bot.prefix
        },
        'commands': {},
        'modules': [],
    }

    # Adding commands
    for name, command in bot.commands.commands.items():
        data['commands'][name] = {
            'cooldown': command.cooldown,
            'requires_mod': command.requires_mod,
            'hidden': command.hidden,
            'response': command.response,
        }

    # Writing config
    write(path, data)


def write(path: str, cfg: dict):
    """Write `cfg` to `path`.
    """
    with open(path, 'w') as file:
        file.write(json.dumps(cfg, indent=4))
