# coding: utf-8
import os

import click

from askoclics import AskomicsInstance
from askoclics.cli.cli import pass_context
from askoclics.cli import config
from askoclics.cli.io import warn, info

CONFIG_TEMPLATE = """## Askomics's askoclics: Global Configuration File.
# Each stanza should contain a single askomics server to control.
#
# You can set the key __default to the name of a default instance
__default: local
local:
    url: "%(url)s"
    api_key: "%(api_key)s"
"""

CONFIG_AUTH = """## Askomics's askoclics: Global Configuration File.
# Each stanza should contain a single askomics server to control.
#
# You can set the key __default to the name of a default instance
__default: local
local:
    url: "%(url)s"
    api_key: "%(api_key)s"
    proxy_username: "%(username)s"
    proxy_password: "%(password)s"
"""

SUCCESS_MESSAGE = (
    "Ready to go! Type `askoclics` to get a list of commands you can execute."
)


@click.command("config_init")
@pass_context
def cli(ctx, url=None, admin=False, **kwds):
    """Help initialize global configuration (in home directory)
    """

    click.echo("""Welcome to Askoclics""")
    if os.path.exists(config.global_config_path()):
        info("Your askoclics configuration already exists. Please edit it instead: %s" % config.global_config_path())
        return 0

    while True:
        # Check environment
        url = click.prompt("Askomics server url, including http:// and the port if required")
        url.rstrip().rstrip("/")
        api_key = click.prompt("Askomics user's API key")
        username = ""
        password = ""
        if click.confirm("""Is your Askomics instance running behind an authentication proxy?"""):
            username = click.prompt("Username")
            password = click.prompt("Password", hide_input=True)
        info("Testing connection...")
        try:
            AskomicsInstance(url=url, api_key=api_key, proxy_username=username, proxy_password=password)
            # We do a connection test during startup.
            info("Ok! Everything looks good.")
            break
        except Exception as e:
            warn("Error, we could not access the configuration data for your instance: %s", e)
            should_break = click.prompt("Continue despite inability to contact this instance? [y/n]")
            if should_break in ('Y', 'y'):
                break

    config_path = config.global_config_path()
    if os.path.exists(config_path):
        warn("File %s already exists, refusing to overwrite." % config_path)
        return -1

    with open(config_path, "w") as f:

        if username and password:
            f.write(CONFIG_AUTH % {
                'url': url,
                'api_key': api_key,
                'username': username,
                'password': password
            })
        else:
            f.write(CONFIG_TEMPLATE % {
                'url': url,
                'api_key': api_key
            })
        info(SUCCESS_MESSAGE)

    # We don't want other users to look into this file
    os.chmod(config_path, 0o600)


