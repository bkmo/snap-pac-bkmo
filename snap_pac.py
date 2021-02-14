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
"""
Script for taking pre/post snapshots; run from pacman hooks.
"""

from argparse import ArgumentParser
from configparser import ConfigParser
import logging
import os
import sys

logging.basicConfig(format="%(message)s", level=logging.INFO)


def create_snapper_cmd(preorpost, config, section, prefile):
    """Populate the snapper command."""
    try:
        chroot = os.stat("/") != os.stat("/proc/1/root/.")
    except PermissionError:
        logging.warning("Unable to detect if in chroot. Run script as root.")
        chroot = False
    snapper_cmd = ["snapper"]
    if chroot:
        snapper_cmd.append("--no-dbus")
    snapper_cmd.append(f"--config {section} create")
    snapper_cmd.append(f"--type {preorpost}")
    snapper_cmd.append(f"--cleanup-algorithm {config.get(section, 'cleanup_algorithm')}")
    snapper_cmd.append("--print-number")
    desc_limit = config.getint(section, "desc_limit")
    if preorpost == "pre":
        snapper_cmd.append(f"--description {config.get(section, 'pre_description')[:desc_limit]}")
    else:
        snapper_cmd.append(f"--description {config.get(section, 'post_description')[:desc_limit]}")
        with open(prefile, "r") as f:
            pre_number = f.read().rstrip("\n")
            snapper_cmd.append(f"--pre-number {pre_number}")
        os.remove(prefile)
    return snapper_cmd


def do_snapshot(preorpost, cmd, prefile):
    """Run the actual snapper command and save snapshot number if pre snapshot."""
    num = os.popen(" ".join(cmd)).read().rstrip("\n")
    if preorpost == "pre":
        with open(prefile, "w") as f:
            f.write(num)
    return num


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
        "pre_description": "".join(["\"", parent_cmd, "\""]),
        "post_description":  "".join(["\"", packages, "\""]),
        "desc_limit": 72
    }
    config["root"] = {
        "snapshot": True
    }
    config.read(ini_file)
    return config


def main(snap_pac_ini, snapper_conf_file, args):

    if os.getenv("SNAP_PAC_SKIP", "n") in ["y", "Y", "yes", "Yes", "YES"]:
        return False

    parent_cmd = os.popen(f"ps -p {os.getppid()} -o args=").read().strip()
    packages = " ".join([line.rstrip("\n") for line in sys.stdin])
    config = setup_config_parser(snap_pac_ini, parent_cmd, packages)
    snapper_configs = get_snapper_configs(snapper_conf_file)

    for c in snapper_configs:

        if c not in config:
            config.add_section(c)

        logging.debug(f"{c = }")
        if config.getboolean(c, "snapshot"):
            prefile = f"/tmp/snap-pac-pre_{c}"
            logging.debug(f"{prefile = }")
            snapper_cmd = create_snapper_cmd(args.preorpost, config, c, prefile)
            logging.debug(f"{snapper_cmd = }")
            num = do_snapshot(args.preorpost, snapper_cmd, prefile)
            logging.info(f"==> {c}: {num}")

    return True


if __name__ == "__main__":

    snap_pac_ini = "/etc/snap-pac.ini"
    logging.debug(f"{snap_pac_ini = }")
    snapper_conf_file = "/etc/conf.d/snapper"
    logging.debug(f"{snapper_conf_file = }")

    parser = ArgumentParser()
    parser.add_argument(dest="preorpost")
    args = parser.parse_args()

    if args.preorpost not in ["pre", "post"]:
        raise ValueError("preorpost must be 'pre' or 'post'")

    main(snap_pac_ini, snapper_conf_file, args)
