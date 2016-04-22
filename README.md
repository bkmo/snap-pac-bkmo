# snap-pac

This makes Arch Linux's pacman use
[snapper](https://wiki.archlinux.org/index.php/Snapper) to automatically take a
pre and post snapshot before and after pacman transactions, similar to how YaST
does with OpenSuse.

*Note:* The scripts only take snapshots of the subvolume mounted at `/`; other
subvolumes are not included. You must modify the scripts to include other
subvolumes. It's recommended that you create subvolumes of directories you do
*not* want included (*e.g.* `/var/cache/pacman/pkg`). 

The scripts are set up to use the `number` algorithm. That is, snapper will
periodically clean up snapshots tagged with `number` after reaching a set
threshold in the snapper configuration file.

Additionally the package provides a hook to regenerate your GRUB configuration
file after every pacman transaction. This is useful when using
[grub-btrfs](https://aur.archlinux.org/packages/grub-btrfs-git/).

## Installation

Install [the package from the
AUR](https://aur.archlinux.org/packages/snap-pac/).

Optionally install
[grub-btrfs](https://aur.archlinux.org/packages/grub-btrfs-git/) to populate
your GRUB menu with the ability to boot into snapshots.

## Usage

**Use pacman (and AUR helpers) as normal and watch snapper do its thing.** No
bash scripts for you to call. No bash aliases to setup.

Because these are pacman hooks, it doesn't matter how you call pacman (whether
directly, through an AUR helper, or an alias)---snapper will create the
snapshots whenever pacman is asked to install, upgrade, or remove a package. The
description for the snapshot is the pacman command that called the hook in the
first place.

### Example

Installing the `nano` package as normal:

	# pacman -S nano
	resolving dependencies...
	looking for conflicting packages...

	Packages (1) nano-2.5.3-1

	Total Installed Size:  2.14 MiB

	:: Proceed with installation? [Y/n] Y
	(1/1) checking keys in keyring                                      [######################################] 100%
	(1/1) checking package integrity                                    [######################################] 100%
	(1/1) loading package files                                         [######################################] 100%
	(1/1) checking for file conflicts                                   [######################################] 100%
	(1/1) checking available disk space                                 [######################################] 100%
	:: Running pre-transaction hooks...
	(1/1) snapper pre snapshot
	:: Processing package changes...
	(1/1) installing nano                                               [######################################] 100%
	:: Running post-transaction hooks...
	(1/1) snapper post snapshot

And here are the snapshots:

    # snapper -c root list -t pre-post | tail -n 1
    1033  | 1034   | Fri 22 Apr 2016 01:54:13 PM CDT | Fri 22 Apr 2016 01:54:14 PM CDT | pacman -S nano                                  |         

What changed (see the man page for what each symbol means)?

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
	+..... /usr/share/doc/nano/nano.1.html
	+..... /usr/share/doc/nano/nanorc.5.html
	+..... /usr/share/doc/nano/rnano.1.html
	c..... /usr/share/info/dir
	+..... /usr/share/info/nano.info.gz

(I truncated the above output, but it continues...) You can also do `snapper
diff` in the same way---I'll spare you that one.

To undo the upgrade:

	# snapper -c root undochange 1033..1034
	create:0 modify:3 delete:100

And `nano` is now gone:

	$ pacman -Qi nano
	error: package 'nano' was not found

## References

* [snapper homepage](http://snapper.io/)
* [Btrfs homepage](https://wiki.archlinux.org/index.php/Btrfs)
* [ArchWiki Snapper article](https://wiki.archlinux.org/index.php/Snapper)
* [ArchWiki Btrfs article](https://wiki.archlinux.org/index.php/Btrfs)
* `man alpm-hooks`
* `man snapper`
* `man btrfs`
