# This is a built-in function.
# Please do not modify this unless you really know what you're doing.

import re

from src.commands import BaseModule
from src.definitions import MODULE_MENTION_REGEX

MODULE_RE = re.compile(MODULE_MENTION_REGEX)


class Module(BaseModule):
    helpmsg = 'Prints all available commands, or, if provided a method, prints the help message for that method. Usage: help <method?>'

    consumes = 1

    def main(self):
        args = self.get_args_lower()

        # If no command is provided, just run the base help message.
        if not args:
            # list of all commands (not hidden, not mod-only)
            user_commands_list = ', '.join(
                [n for n, c in self._bot.commands.commands.items() if not c.hidden and not c.requires_mod])
            # list of all commands (not hidden, mod-only)
            mod_commands_list = ', '.join(
                [n for n, c in self._bot.commands.commands.items() if not c.hidden and c.requires_mod])

            return f"Available commands are: {user_commands_list} (mod-only: {mod_commands_list})"

        # If a command is provided, run the help for it.
        else:
            name = args[0]

            # if the name resolves to a module, give the module's helpmsg
            if name in self._bot.commands.modules:
                return str(self._bot.commands.modules[name].help())

            # if not a module and resolves to a command...
            elif name in self._bot.commands.commands:

                # see if it mentions any modules
                command_modules = self.module_re.findall(
                    self._bot.commands.commands[name].response)

                # if it does, give the modules it mentions
                if command_modules:
                    return str(f"Module '{name}' not found, but the matching command uses module(s): "
                               + f"{', '.join(command_modules)}")

                else:
                    return str(f"Command {name} does not mention any modules.")

            else:
                return "No matching command or module."
