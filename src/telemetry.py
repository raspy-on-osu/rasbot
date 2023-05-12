from discord import SyncWebhook

from src.config import read_global
from update import get_rasbot_current_version

WEBHOOK_URL = "https://discord.com/api/webhooks/1104885792779812906/U0sYFISyGGRU7TcNNqAjpSH300mQBRPLhxUoVCnX7iKKaeUmUVvJbv6tU0l2n7zu5dlA"
# Please don't do anything weird with this! This webhook is for private exception reporting so anyone noted as a developer can take a look.

WEBHOOK = SyncWebhook.from_url(WEBHOOK_URL)

GLOBAL_CONFIG = read_global()


def report_exception(message, username):
    # Turn this off if you don't want it, but it helps me fix issues.
    if GLOBAL_CONFIG["telemetry"] > 0:
        WEBHOOK.send(content=message, username=username)


def notify_instance(username):
    if GLOBAL_CONFIG["telemetry"] > 1:
        message = f"New instance started with version {get_rasbot_current_version()}"
        WEBHOOK.send(content=message, username=username)
