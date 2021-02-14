#!/usr/bin/env python

"""
Copyright (C) 2021 Wes Barnett

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from argparse import ArgumentParser
from configparser import ConfigParser
import os


def create_snapper_cmd(args, config):
    chroot = os.stat("/") != os.stat("/proc/1/root/.")
    snapper_cmd = ["snapper"]
    if chroot:
        snapper_cmd.append("--no-dbus")
    snapper_cmd.append("--config")
    snapper_cmd.append(c)
    snapper_cmd.append("create")
    snapper_cmd.append("--type")
    snapper_cmd.append(args.preorpost)
    snapper_cmd.append("--cleanup-algorithm")
    snapper_cmd.append(config.get(x, "cleanup_algorithm"))
    snapper_cmd.append("--print-number")
    snapper_cmd.append("--description")
    desc_limit = config.getint(x, "desc_limit")
    if args.preorpost == "pre":
        snapper_cmd.append(config.get(x, "pre_description")[:desc_limit])
    else:
        snapper_cmd.append(config.get(x, "post_description")[:desc_limit])
    return snapper_cmd


def do_snapshot(preorpost, cmd, prefile):
    if preorpost == "pre":
        return do_pre_snapshot(cmd, prefile)
    else:
        return do_post_snapshot(cmd, prefile)


def do_pre_snapshot(cmd, prefile):
    """Run snapper command, write snapshot number to file."""
    num = os.popen(" ".join(cmd)).read().rstrip("\n")
    with open(prefile, "w") as f:
        f.write(num)
    return num


def do_post_snapshot(cmd, prefile):
    """Read pre snapshot number from file, run snapper, delete prefile."""
    cmd.append("--pre-number")
    with open(prefile, "r") as f:
        cmd.append(f.read().rstrip("\n"))
    num = os.popen(" ".join(cmd)).read().rstrip("\n")
    os.remove(prefile)
    return num


def get_snapper_configs(conf_file):
    """Get the snapper configurations."""
    with open(conf_file, "r") as f:
        for line in f:
            if line.startswith("SNAPPER_CONFIGS"):
                line = line.rstrip("\n").rstrip("\"")
                line = line.split("=")
                line = line[1].lstrip("\"")
                return line.split()


def setup_config_parser(ini_file):
    """Set up defaults for snap-pac configuration."""
    parent_cmd = os.popen(f"ps -p {os.getppid()} -o args=").read().strip()

    config = ConfigParser()
    config["DEFAULT"] = {
        "snapshot": False,
        "cleanup_algorithm": "number",
        "pre_description": "".join(["\"", parent_cmd, "\""]),
        "post_description": "TODO",
        "desc_limit": 72
    }
    config["root"] = {
        "snapshot": True
    }
    config.read(ini_file)
    return config


if __name__ == "__main__":

    snap_pac_ini = "/etc/snap-pac.ini"
    snapper_conf_file = "/etc/conf.d/snapper"

    parser = ArgumentParser()
    parser.add_argument(dest="preorpost")
    args = parser.parse_args()

    config = setup_config_parser(snap_pac_ini)
    snapper_configs = get_snapper_configs(snapper_conf_file)

    for c in snapper_configs:

        if c in config:
            x = c
        else:
            x = "DEFAULT"

        if config.getboolean(x, "snapshot"):
            prefile = f"/tmp/snap-pac-pre_{c}"
            snapper_cmd = create_snapper_cmd(args, config)
            num = do_snapshot(args.preorpost, snapper_cmd, prefile)
            print(f"==> {c}: {num}")
