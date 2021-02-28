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
import logging
import os
import sys


logging.basicConfig(format="%(message)s", level=logging.INFO)


class SnapperCmd:

    def __init__(self, config, snapshot_type, cleanup_algorithm, description="", nodbus=False, pre_number=None):
        self.cmd = ["snapper"]
        if nodbus:
            self.cmd.append("--no-dbus")
        self.cmd.append(f"--config {config} create")
        self.cmd.append(f"--type {snapshot_type}")
        self.cmd.append(f"--cleanup-algorithm {cleanup_algorithm}")
        self.cmd.append("--print-number")
        if description:
            self.cmd.append(f"--description \"{description}\"")
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
    with open(conf_file, "r") as f:
        for line in f:
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
        "post_description": packages,
        "desc_limit": 72
    }
    config["root"] = {
        "snapshot": True
    }
    config.read(ini_file)
    return config


def get_description(snapshot_type, config, section):
    desc_limit = config.getint(section, "desc_limit")
    if snapshot_type == "pre":
        return config.get(section, "pre_description")[:desc_limit]
    else:
        return config.get(section, "post_description")[:desc_limit]


def get_pre_number(snapshot_type, prefile):
    if snapshot_type == "pre":
        pre_number = None
    else:
        try:
            with open(prefile, "r") as f:
                pre_number = f.read().rstrip("\n")
                os.remove(prefile)
        except FileNotFoundError:
            raise FileNotFoundError(f"prefile {prefile} not found. Ensure you have run the pre snapshot first.")
    return pre_number


def write_pre_number(num, prefile):
    with open(prefile, "w") as f:
        f.write(num)


def main(snap_pac_ini, snapper_conf_file, args):

    if os.getenv("SNAP_PAC_SKIP", "n").lower() in ["y", "yes", "true", "1"]:
        return False

    parent_cmd = os.popen(f"ps -p {os.getppid()} -o args=").read().strip()
    logging.debug("Getting list of packages from standard input...")
    packages = " ".join([line.rstrip("\n") for line in sys.stdin])
    config = setup_config_parser(snap_pac_ini, parent_cmd, packages)
    snapper_configs = get_snapper_configs(snapper_conf_file)
    chroot = os.stat("/") != os.stat("/proc/1/root/.")

    for snapper_config in snapper_configs:

        if snapper_config not in config:
            config.add_section(snapper_config)

        logging.debug(f"{snapper_config = }")

        if config.getboolean(snapper_config, "snapshot"):
            prefile = f"/tmp/snap-pac-pre_{snapper_config}"
            logging.debug(f"{prefile = }")

            cleanup_algorithm = config.get(snapper_config, "cleanup_algorithm")
            description = get_description(args.type, config, snapper_config)
            pre_number = get_pre_number(args.type, prefile)

            snapper_cmd = SnapperCmd(snapper_config, args.type, cleanup_algorithm, description, chroot, pre_number)
            logging.debug(f"{str(snapper_cmd) = }")
            num = snapper_cmd()
            logging.info(f"==> {snapper_config}: {num}")

            if args.type == "pre":
                write_pre_number(num, prefile)

    return True


if __name__ == "__main__":

    snap_pac_ini = "/etc/snap-pac.ini"
    logging.debug(f"{snap_pac_ini = }")
    snapper_conf_file = "/etc/conf.d/snapper"
    logging.debug(f"{snapper_conf_file = }")

    parser = ArgumentParser(description="Script for taking pre/post snapper snapshots. Used with pacman hooks.")
    parser.add_argument(dest="type", choices=["pre", "post"])
    args = parser.parse_args()

    main(snap_pac_ini, snapper_conf_file, args)
