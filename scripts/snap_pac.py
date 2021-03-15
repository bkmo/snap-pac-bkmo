#!/usr/bin/env python
# Copyright (C) 2021 Wes Barnett

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""Script for taking pre/post snapshots; run from pacman hooks."""

from argparse import ArgumentParser
from configparser import ConfigParser
import json
import logging
from pathlib import Path
import os
import sys
import tempfile


logging.basicConfig(format="%(message)s", level=logging.INFO)


class SnapperCmd:

    def __init__(self, config, snapshot_type, cleanup_algorithm, description="",
                 nodbus=False, pre_number=None, userdata=""):
        self.cmd = ["snapper"]
        if nodbus:
            self.cmd.append("--no-dbus")
        self.cmd.extend([
            f"--config {config} create",
            f"--type {snapshot_type}",
            f"--cleanup-algorithm {cleanup_algorithm}",
            "--print-number"
        ])
        if description:
            self.cmd.append(f"--description \"{description}\"")
        if userdata:
            self.cmd.append(f"--userdata \"{userdata}\"")
        if snapshot_type == "post":
            if pre_number is not None:
                self.cmd.append(f"--pre-number {pre_number}")
            else:
                raise ValueError("snapshot type specified as 'post' but no pre snapshot number passed.")

    def __call__(self):
        return os.popen(self.__str__()).read().rstrip("\n")

    def __str__(self):
        return " ".join(self.cmd)


def get_snapper_configs(conf_file):
    """Get the snapper configurations."""
    for line in conf_file.read_text().split("\n"):
        if line.startswith("SNAPPER_CONFIGS"):
            line = line.rstrip("\n").rstrip("\"").split("=")
            return line[1].lstrip("\"").split()


def setup_config_parser(ini_file, parent_cmd, packages):
    """Set up defaults for snap-pac configuration."""

    config = ConfigParser()
    config["DEFAULT"] = {
        "snapshot": False,
        "cleanup_algorithm": "number",
        "pre_description": parent_cmd,
        "post_description": " ".join(packages),
        "desc_limit": 72,
        "important_packages": [],
        "important_commands": [],
        "userdata": []
    }
    config["root"] = {
        "snapshot": True
    }
    config.read(ini_file)
    return config


def get_description(snapshot_type, config, section):
    desc_limit = config.getint(section, "desc_limit")
    return config.get(section, f"{snapshot_type}_description")[:desc_limit]


def get_pre_number(snapshot_type, prefile):
    if snapshot_type == "pre":
        pre_number = None
    else:
        try:
            pre_number = prefile.read_text()
        except FileNotFoundError:
            raise FileNotFoundError(f"prefile {prefile} not found. Ensure you have run the pre snapshot first.")
        else:
            prefile.unlink()
    return pre_number


def check_important_commands(config, snapper_config, parent_cmd):
    important_commands = json.loads(config.get(snapper_config, "important_commands"))
    return parent_cmd in important_commands


def check_important_packages(config, snapper_config, packages):
    important_packages = json.loads(config.get(snapper_config, "important_packages"))
    return any(x in important_packages for x in packages)


def get_userdata(config, snapper_config, important):
    userdata = set(json.loads(config.get(snapper_config, "userdata")))
    if important:
        userdata.add("important=yes")
    return ",".join(sorted(list(userdata)))


def main(snap_pac_ini, snapper_conf_file, snapshot_type):

    if os.getenv("SNAP_PAC_SKIP", "n").lower() in ["y", "yes", "true", "1"]:
        return False

    parent_cmd = os.popen(f"ps -p {os.getppid()} -o args=").read().strip()
    packages = [line.rstrip("\n") for line in sys.stdin]
    config = setup_config_parser(snap_pac_ini, parent_cmd, packages)
    snapper_configs = get_snapper_configs(snapper_conf_file)
    chroot = os.stat("/") != os.stat("/proc/1/root/.")

    for snapper_config in snapper_configs:

        if snapper_config not in config:
            config.add_section(snapper_config)

        if config.getboolean(snapper_config, "snapshot"):
            prefile = tempfile.gettempdir() / Path(f"snap-pac-pre_{snapper_config}")

            cleanup_algorithm = config.get(snapper_config, "cleanup_algorithm")
            description = get_description(snapshot_type, config, snapper_config)
            pre_number = get_pre_number(snapshot_type, prefile)

            important = (check_important_commands(config, snapper_config, parent_cmd) or
                         check_important_packages(config, snapper_config, packages))

            userdata = get_userdata(config, snapper_config, important)

            snapper_cmd = SnapperCmd(snapper_config, snapshot_type, cleanup_algorithm,
                                     description, chroot, pre_number, userdata)
            num = snapper_cmd()
            logging.info(f"==> {snapper_config}: {num}")

            if snapshot_type == "pre":
                prefile.write_text(num)

    return True


if __name__ == "__main__":

    parser = ArgumentParser(description="Script for taking pre/post snapper snapshots. Used with pacman hooks.")
    parser.add_argument(dest="type", choices=["pre", "post"], help="snapper snapshot type")
    parser.add_argument(
        "--ini", dest="snap_pac_ini", type=Path,
        default=Path("/etc/snap-pac.ini"), help="snap-pac ini file path"
    )
    parser.add_argument(
        "--conf", dest="snapper_conf_file", type=Path,
        default=Path("/etc/conf.d/snapper"), help="snapper configuration file path"
    )
    args = parser.parse_args()

    main(args.snap_pac_ini, args.snapper_conf_file, args.type)
