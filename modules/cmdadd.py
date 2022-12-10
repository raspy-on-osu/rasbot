# This is a built-in function.
# Please do not modify this unless you really know what you're doing.

from commands import BaseModule
from definitions import VALID_COMMAND_REGEX,\
    CommandGivenInvalidNameError,\
    CommandMustHavePositiveCooldownError

DEFAULT_CONFIG = {
    # The parameters to be given, after cooldown, before response
    # to indicate this command should be mod-only or hidden from !help
    "modonly_arg": "-modonly",
    "hidden_arg": "-hidden",
    # The default cooldown to apply to a command if none is specified
    "default_cooldown": 5,
}


class Module(BaseModule):
    helpmsg = 'Adds a new command, or modifies an existing one. Usage: cmdadd <name> <cooldown?> <params?> <response>.'

    def __init__(self, bot, name):
        BaseModule.__init__(self, bot, name, DEFAULT_CONFIG)

        self.MODONLY_ARG = self.cfg_get('modonly_arg')
        self.HIDDEN_ARG = self.cfg_get('hidden_arg')
        self.DEFAULT_COOLDOWN = self.cfg_get('default_cooldown')

    def main(self):
        if not self.bot.cmdargs:
            return "No command information given."

        cmd = self.bot.cmdargs

        # use lower of next item as name
        cmd_name = cmd.pop(0).lower()

        # try to use next item as cooldown in seconds
        # if it can't convert to int, use default
        try:
            cmd_cooldown = int(cmd[0])
            cmd.pop(0)
        except ValueError:
            cmd_cooldown = self.DEFAULT_COOLDOWN

        # check for parameters and consume if found
        params = {
            'modonly': False,
            'hidden': False
        }
        for _ in params:
            for param in params:
                if (cmd[0].lower() == param):
                    params[param] = True
                    cmd.pop(0)

        try:
            # add command and write config
            self.bot.commands.command_modify(cmd_name,
                                             cmd_cooldown,
                                             " ".join(cmd),
                                             params['modonly'],
                                             params['hidden'])
            self.bot.write_config()

            return f'Command {cmd_name} added successfully.'

        except CommandMustHavePositiveCooldownError:
            return 'Command must have a positive cooldown.'

        except CommandGivenInvalidNameError:
            return f'Command name must fit the regular expression {VALID_COMMAND_REGEX}.'

        except ModuleNotFoundError as mod:
            return f'Module {mod} does not exist.'

        except IndexError:
            return 'Command is missing required information.'
