from configparser import ConfigParser
import tempfile
import os

import pytest

from scripts.snap_pac import (
   SnapperCmd, get_pre_number, get_snapper_configs, main, setup_config_parser,
   write_pre_number, get_description
)


@pytest.fixture
def config():
    config = ConfigParser()
    config["DEFAULT"] = {
        "snapshot": False,
        "cleanup_algorithm": "number",
        "pre_description": "foo",
        "post_description":  "bar",
        "desc_limit": 72
    }
    config["root"] = {
        "snapshot": True
    }
    config["home"] = {
        "snapshot": True,
        "desc_limit": 3,
        "post_description": "a really long description"
    }
    return config


@pytest.fixture
def prefile():
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("1234")
        name = f.name
    return name


def test_snapper_cmd_pre():
    snapper_cmd = SnapperCmd("root", "pre", "number", "foo")
    cmd = "snapper --config root create --type pre --cleanup-algorithm number --print-number --description \"foo\""
    assert str(snapper_cmd) == cmd


def test_snapper_cmd_post():
    snapper_cmd = SnapperCmd("root", "post", "number", "bar", False, 1234)
    cmd = "snapper --config root create --type post --cleanup-algorithm number --print-number"
    cmd += " --description \"bar\" --pre-number 1234"
    assert str(snapper_cmd) == cmd


def test_snapper_cmd_post_nodbus():
    snapper_cmd = SnapperCmd("root", "post", "number", "bar", True, 1234)
    cmd = "snapper --no-dbus --config root create --type post --cleanup-algorithm number --print-number"
    cmd += " --description \"bar\" --pre-number 1234"
    assert str(snapper_cmd) == cmd


def test_get_snapper_configs():
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("## Path: System/Snapper\n")
        f.write("\n")
        f.write("## Type:        string\n")
        f.write("## Default:     \"\"\n")
        f.write("# List of snapper configurations.\n")
        f.write("SNAPPER_CONFIGS=\"home root foo bar\"\n")
        name = f.name
    assert get_snapper_configs(name) == ["home", "root", "foo", "bar"]


def test_skip_snap_pac():
    os.environ["SNAP_PAC_SKIP"] = "y"
    assert main("foo", "bar", "yep") is False


def test_setup_config_parser(config):
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("[home]\n")
        f.write("snapshot = True\n")
        f.write("desc_limit = 3\n")
        f.write("post_description = a really long description\n")
        name = f.name
    config2 = setup_config_parser(name, "foo", "bar")
    assert config == config2


def test_get_pre_number_pre(prefile):
    assert get_pre_number("pre", prefile) is None


def test_get_pre_number_post(prefile):
    assert get_pre_number("post", prefile) == "1234"


def test_write_pre_number(prefile):
    write_pre_number("5678", prefile)
    assert get_pre_number("post", prefile) == "5678"


def test_get_pre_description(config):
    assert get_description("pre", config, "home") == "foo"


def test_get_post_description(config):
    assert get_description("post", config, "home") == "a r"
