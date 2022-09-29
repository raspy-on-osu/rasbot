# This is a built-in function.
# Please do not modify this unless you really know what you're doing.

from commands import BaseModule


class Module(BaseModule):
    helpmsg = "Returns a mentioned user. If no user is mentioned, returns the last messages' author."

    def main(self, bot):
        if not bot.cmdargs:
            return bot.author_name

        user = bot.cmdargs[0]
        if user[0] == "@":
            user = user[1:]

        return user