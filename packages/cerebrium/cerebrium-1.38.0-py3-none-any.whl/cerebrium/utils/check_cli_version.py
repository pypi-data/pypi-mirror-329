import json
import urllib.request

import packaging.version
from rich import print

from cerebrium import __version__ as cerebrium_version


def print_update_cli_message():
    """
    Compare the current version of the CLI with the latest version available on PyPI
    """
    latest_version = find_latest_pip_version()

    if packaging.version.parse(cerebrium_version) < packaging.version.parse(latest_version):
        print(f"A new release of Cerebrium is available.")
        print(
            f"Please upgrade to version {latest_version} by running `pip install cerebrium --upgrade`"
        )


def find_latest_pip_version():
    """
    Find the latest version of the cerebrium package.
    """
    url = "https://pypi.python.org/pypi/cerebrium/json"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))

    releases = data["releases"].keys()
    latest_version = max(
        packaging.version.parse(release)
        for release in releases
        if not packaging.version.parse(release).is_prerelease
    )

    return str(latest_version)
