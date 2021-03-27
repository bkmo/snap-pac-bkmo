import tempfile
from pathlib import Path
import os

import pytest

from scripts.snap_pac import (
    SnapperCmd, ConfigProcessor, check_skip, get_pre_number, get_snapper_configs,
    ProcessedConfig
)


@pytest.fixture
def prefile():
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("1234")
        name = f.name
    return Path(name)


@pytest.mark.parametrize("snapper_cmd, actual_cmd", [
    (
        SnapperCmd("root", "pre", "number", "foo"),
        "snapper --config root create --type pre --cleanup-algorithm number --print-number --description \"foo\""
    ),
    (
        SnapperCmd("root", "post", "number", "bar", False, 1234),
        "snapper --config root create --type post --cleanup-algorithm number --print-number"
        " --description \"bar\" --pre-number 1234"
    ),
    (
        SnapperCmd("root", "post", "number", "bar", True, 1234),
        "snapper --no-dbus --config root create --type post --cleanup-algorithm number --print-number"
        " --description \"bar\" --pre-number 1234"
    ),
    (
        SnapperCmd("root", "post", "number", "bar", False, 1234, "important=yes"),
        "snapper --config root create --type post --cleanup-algorithm number --print-number"
        " --description \"bar\" --userdata \"important=yes\" --pre-number 1234"
    ),
    (
        SnapperCmd("root", "post", "number", "bar", False, 1234, "foo=bar,important=yes"),
        "snapper --config root create --type post --cleanup-algorithm number --print-number"
        " --description \"bar\" --userdata \"foo=bar,important=yes\" --pre-number 1234"
    )
])
def test_snapper_cmd(snapper_cmd, actual_cmd):
    assert str(snapper_cmd) == actual_cmd


def test_get_snapper_configs():
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("## Path: System/Snapper\n")
        f.write("\n")
        f.write("## Type:        string\n")
        f.write("## Default:     \"\"\n")
        f.write("# List of snapper configurations.\n")
        f.write("SNAPPER_CONFIGS=\"home root foo bar\"\n")
        name = f.name
    assert get_snapper_configs(Path(name)) == ["home", "root", "foo", "bar"]


def test_skip_snap_pac():
    os.environ["SNAP_PAC_SKIP"] = "y"
    assert check_skip() is True


@pytest.mark.parametrize("section, command, packages, snapshot_type, result", [
    (
        "root", "foo", ["bar"], "pre",
        ProcessedConfig("foo", "number", "", True)
    ),
    (
        "root", "pacman -Syu", [], "pre",
        ProcessedConfig("pacman -Syu", "number", "important=yes", True)
    ),
    (
        "mail", "pacman -Syu", [], "pre",
        ProcessedConfig("pacman -Syu", "number", "", False)
    ),
    (
        "home", "pacman -Syu", [], "pre",
        ProcessedConfig("pac", "number", "foo=bar,requestid=42", True)
    ),
    (
        "home", "pacman -Syu", [], "post",
        ProcessedConfig("a r", "number", "foo=bar,requestid=42", True)
    ),
    (
        "myconfig", "pacman -S linux", ["linux"], "post",
        ProcessedConfig("linux", "timeline", "foo=bar,important=yes,requestid=42", True)
    ),
])
def test_config_processor(section, command, packages, snapshot_type, result):
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("[root]\n")
        f.write("important_commands = [\"pacman -Syu\"]\n\n")
        f.write("[home]\n")
        f.write("snapshot = True\n")
        f.write("desc_limit = 3\n")
        f.write("post_description = a really long description\n")
        f.write("userdata = [\"foo=bar\", \"requestid=42\"]\n\n")
        f.write("[myconfig]\n")
        f.write("snapshot = True\n")
        f.write("cleanup_algorithm = timeline\n")
        f.write("important_packages = [\"linux\", \"linux-lts\"]\n")
        f.write("userdata = [\"foo=bar\", \"requestid=42\"]\n")
        name = f.name
    config_processor = ConfigProcessor(name, snapshot_type, command, packages)
    assert config_processor(section) == result


def test_get_pre_number_pre(prefile):
    assert get_pre_number("pre", prefile) is None


def test_get_pre_number_post(prefile):
    assert get_pre_number("post", prefile) == "1234"


def test_no_prefile():
    with pytest.raises(FileNotFoundError):
        get_pre_number("post", Path("/tmp/foo-pre-file-not-found"))
