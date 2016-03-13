# snap-pac

This makes Arch Linux's pacman use
[snapper](https://wiki.archlinux.org/index.php/Snapper) to automatically take a
pre and post snapshot before and after pacman transactions, similar to how YaST
does with OpenSuse.

*Note:* The scripts only take snapshots of the subvolume mounted at `/`; other
subvolumes are not included. You must modify the scripts to include other
subvolumes.

The scripts are set up to use the `number` algorithm. That is, snapper will
periodically clean up snapshots tagged with `number` after reaching a set
threshold in the snapper configuration file.

## Installation

Install [the package from the AUR](https://aur.archlinux.org/packages/snap-pac/).

## Usage

**Use pacman (and AUR helpers) as normal and watch snapper do its thing.** No
bash scripts for you to call. No bash aliases to setup.

Because these are pacman hooks, it doesn't matter how you call pacman (whether
directly, through an AUR helper, or an alias) -- snapper will create the
snapshots whenever pacman is asked to install, upgrade, or remove a package.

### Example

Installing the `nano` package as normal:

	$ sudo pacman -S nano
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

    $ sudo snapper -c root list | tail -n 2 
	pre    | 112 |       | Fri 11 Mar 2016 01:59:04 PM CST | root | number   | pacman pretransaction     |         
	post   | 113 | 112   | Fri 11 Mar 2016 01:59:04 PM CST | root | number   | pacman posttransaction    |         

What changed (see the man page for what each symbol means)?

	$ sudo snapper -c root status 112..113
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
diff` in the same way - I'll spare you that one.

To undo the upgrade:

	$ sudo snapper -c root undochange 112..113
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
