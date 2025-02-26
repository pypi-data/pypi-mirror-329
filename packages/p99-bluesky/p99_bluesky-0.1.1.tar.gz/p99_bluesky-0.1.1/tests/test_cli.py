import subprocess
import sys

from p99_bluesky import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "p99_bluesky", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
