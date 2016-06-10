# snap-pac

[![AUR Version](https://img.shields.io/aur/version/snap-pac.svg)](https://aur.archlinux.org/packages/snap-pac/)
[![License](https://img.shields.io/aur/license/snap-pac.svg)](https://github.com/wesbarnett/snap-pac/blob/master/LICENSE)
[![AUR Votes](https://img.shields.io/aur/votes/snap-pac.svg)](https://aur.archlinux.org/packages/snap-pac/)

This makes Arch Linux's pacman use
[snapper](https://wiki.archlinux.org/index.php/Snapper) to automatically take a
pre and post snapshot before and after pacman transactions using pacman's hooks
feature, similar to how YaST does with OpenSuse. This provides a simple way to
undo changes to a system after a pacman transaction.

* [Installation](#installation)
* [Configuration](#configuration)
* [Usage](#usage)
* [Example](#example)
* [Troubleshooting](#troubleshooting)
* [License](#license)
* [See also](#see-also)

## Installation

Install [the package from the
AUR](https://aur.archlinux.org/packages/snap-pac/).

After installation, the hooks will be located in `/usr/share/libalpm/hooks`, and
the script will be located in `/usr/share/libalpm/hooks.bin`.

In an effort to bring about a higher standard in distributing packages in the
AUR, starting with release 0.6, I have signed the release with my PGP key. You
must import my public key to verify the signature if you are using the PKGBUILD
in the AUR. This can be done via:

    $ gpg --recv-keys A3B8C5C3

The key's fingerprint is:

    8535CEF3F3C38EE69555BF67E4B5E45AA3B8C5C3

You can manually verify the signature of the tarball with:

    $ gpg --verify version.tar.gz.sig

where "version" is the version of the release you are checking.

## Configuration

Configuration is done via the snapper configuration files, with extra variables
specific to these pacman hooks. The defaults should be suitable for most users.
The following are possible settings you can place in each snapper configuration
file:

* `PACMAN_PRE_POST` - perform pacman pre/post snapshots for this configuration.
  Default is `"no"` for all configurations, except for the `root` configuration
which is `"yes"`.
* `PACMAN_CLEANUP_ALGORITHM` - snapper algorithm used in cleaning up the pacman pre/post
  snapshots. Default is `"number"`.
* `PACMAN_PRE_DESCRIPTION` - snapper description used for the pacman pre snapshot.
  Default is the pacman command that called the snapshot.
* `PACMAN_POST_DESCRIPTION` - snapper description used for the pacman post snapshot.
  Default is the pacman command that called the snapshot.

These settings only need to be added to the snapper configuration files if you
want to change the default.

## Usage

### Taking snapshots

**Use pacman—and AUR helpers—as normal and watch snapper do its thing.** No
bash scripts for you to call. No bash aliases to setup.

Because these are pacman hooks, it doesn't matter how you call pacman—whether
directly, through an AUR helper, or using an alias—snapper will create the
snapshots when pacman installs, upgrades, or removes a package. The
pacman command used is logged in the snapper description for the
snapshots.

### Undoing a transaction

To undo changes from a pacman transaction, use `snapper undochange`. See the
snapper manpage and the following example.

If you have severe breakage—like snapper is gone for some reason and you can't
get it back—you'll have to resort to more extreme methods, such as taking a
snapshot of the pre snapshot and making it the default subvolume or mounting it
as `/`. Most likely you'll need to use a live USB to get into a chroot
environment to do any of these things. Snapper has a `snapper rollback` feature,
but your setup has to be properly configured to use it. The exact procedure
depends on your specific setup. Be careful.

## Example

Installing the `nano` package as normal:

	# pacman -S nano
	resolving dependencies...
	looking for conflicting packages...

	Packages (1) nano-2.5.3-1

	Total Installed Size:  2.14 MiB

	:: Proceed with installation? [Y/n] Y
	(1/1) checking keys in keyring                               [######################################] 100%
	(1/1) checking package integrity                             [######################################] 100%
	(1/1) loading package files                                  [######################################] 100%
	(1/1) checking for file conflicts                            [######################################] 100%
	(1/1) checking available disk space                          [######################################] 100%
	:: Running pre-transaction hooks...
	(1/1) snapper pre snapshot
	:: Processing package changes...
	(1/1) installing nano                                        [######################################] 100%
    :: Running post-transaction hooks...
    (1/2) snapper post snapshot
    (2/2) generate GRUB configuration file

And here are the snapshots:

    # snapper -c root list -t pre-post | tail -n 1
    1033  | 1034   | Fri 22 Apr 2016 01:54:13 PM CDT | Fri 22 Apr 2016 01:54:14 PM CDT | pacman -S nano      | 

What changed?

	# snapper -c root status 1033..1034
    +..... /etc/nanorc
    c..... /etc/snapper/.snap-pac-pre
    +..... /usr/bin/nano
    +..... /usr/bin/rnano
    +..... /usr/share/doc/nano
    +..... /usr/share/doc/nano/faq.html
    +..... /usr/share/doc/nano/fr
    +..... /usr/share/doc/nano/fr/nano.1.html
    +..... /usr/share/doc/nano/fr/nanorc.5.html
    +..... /usr/share/doc/nano/fr/rnano.1.html


I truncated the above output, but it continues. See the manpage for snapper to
see what each symbol means. You can also do `snapper diff` in the same
way—I'll spare you that one.

To undo the upgrade:

	# snapper -c root undochange 1033..1034
	create:0 modify:3 delete:100

And `nano` is now gone, along with all the files it changed:

	$ pacman -Qi nano
	error: package 'nano' was not found

## Troubleshooting

**ERROR: /etc/conf.d/snapper does not exist!**

*snap-pac* reads in the snapper configurations from `/etc/conf.d/snapper`. It
can't do that if the file doesn't exist. I'm not sure what you've done to not
have it exist in the default location.

**WARNING: No snapper configurations found, so not taking any snapshots!**

No snapper configurations were found in `/etc/conf.d/snapper`. This means you
haven't created any configurations yet using `snapper create-config`. See the
snapper manpage on how to do this.

**WARNING: No snapper configurations are set up for snapshots to be taken!**

Although you seem to have created at least one configuration, none of them are
set up for *snap-pac*'s pacman hooks. By default *snap-pac* will take snapshots
for the `root` configuration and any other configuration which has
`PACMAN_PRE_POST` set to `yes` in its configuration file. This message means you
don't have a snapper configuration named `root` (or `PACMAN_PRE_POST` is set to
`no` for it) and no other configuration is set up for snapshots. See the
configuration section above.

**WARNING: *prefile* does not exist, so no post snapshot will be taken. If you are initially installing snap-pac, this is normal.**

*snap-pac* saves the pre snapshot's number in a temporary file. Somehow it go
removed before the post snapshot could be taken. When you initially install
*snap-pac* the post hook is run, but the pre hook never was, so this message
will show up then as well.

## License

snap-pac

Copyright (C) 2016 James W. Barnett

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

## See also

* [ArchWiki Btrfs article](https://wiki.archlinux.org/index.php/Btrfs)
* [ArchWiki Snapper article](https://wiki.archlinux.org/index.php/Snapper)
* [Btrfs homepage](https://wiki.archlinux.org/index.php/Btrfs)
* [snapper homepage](http://snapper.io/)
* `man alpm-hooks`
* `man btrfs`
* `man snapper`
