# snap-pac

![GitHub release](https://img.shields.io/github/release/wesbarnett/snap-pac.svg)
![License](https://img.shields.io/github/license/wesbarnett/snap-pac.svg)
![Issues](https://img.shields.io/github/issues/wesbarnett/snap-pac.svg)

This makes Arch Linux's pacman use
[snapper](https://wiki.archlinux.org/index.php/Snapper) to automatically take a
pre and post snapshot before and after pacman transactions using pacman's hooks
feature, similar to how YaST does with OpenSuse. This provides a simple way to
undo changes to a system after a pacman transaction.

## Installation

Install [the package from the
AUR](https://aur.archlinux.org/packages/snap-pac/).

After installation, the hooks are located at `/usr/share/libalpm/hooks`, and the
scripts are located at `/usr/share/libalpm/hooks.bin/snap-pac`.

## Configuration

The configuration file is located at `/etc/snap-pac.conf`. There you can choose
which snapper configurations, descriptions, and cleanup algorithm to use.
Changing the file should be self-explanatory.  The defaults should be sufficient
for most users.

By default, the snapshots are set up to use snapper's `number` algorithm.
Additionally, by default, snapshots are only taken of the subvolume
corresponding with the `root` snapper configuration. Descriptions are of the
pacman command that initiated the snapshots.

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
environment to do any of these things. The exact procedure depends on your
specific setup. Be careful.

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
