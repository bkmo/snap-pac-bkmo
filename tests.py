from configparser import ConfigParser
import tempfile
import os

import pytest

from scripts.snap_pac import SnapperCmd, get_snapper_configs, main, setup_config_parser


@pytest.fixture
def config():
    config = ConfigParser()
    config["DEFAULT"] = {
        "snapshot": False,
        "cleanup_algorithm": "number",
        "pre_description": "\"foo\"",
        "post_description":  "\"bar\"",
        "desc_limit": 72
    }
    config["root"] = {
        "snapshot": True
    }
    config["home"] = {
        "snapshot": True
    }
    return config


def test_snapper_cmd_pre():
    snapper_cmd = SnapperCmd("root", "pre", "number", "foo")
    cmd = "snapper --config root create --type pre --cleanup-algorithm number --print-number --description \"foo\""
    assert str(snapper_cmd) == cmd


def test_snapper_cmd_post():
    snapper_cmd = SnapperCmd("root", "post", "number", "bar", False, 1234)
    cmd = "snapper --config root create --type post --cleanup-algorithm number --print-number"
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
        f.write("snapshot = True")
        name = f.name
    config2 = setup_config_parser(name, "foo", "bar")
    assert config == config2
