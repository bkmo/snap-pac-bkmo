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
threshold in the configuration file.

## Installation

Install [the package from the AUR](https://aur.archlinux.org/packages/snap-pac/).

## Usage

Continue to use pacman as normal and watch snapper do its thing.  Because these
are pacman hooks, it doesn't matter how you call pacman (whether directly,
through an AUR helper, or an alias) -- snapper will create the snapshots whenever
pacman is asked to install, upgrade, or remove a package.

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
	(1/1) snapper pre transaction
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
	+..... /usr/share/locale/bg/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/ca/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/cs/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/da/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/de/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/eo/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/es/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/eu/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/fi/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/fr/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/ga/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/gl/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/hr/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/hu/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/id/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/it/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/ja/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/ms/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/nb/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/nl/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/nn/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/pl/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/pt_BR/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/ro/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/ru/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/sl/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/sr/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/sv/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/tr/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/uk/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/vi/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/zh_CN/LC_MESSAGES/nano.mo
	+..... /usr/share/locale/zh_TW/LC_MESSAGES/nano.mo
	+..... /usr/share/man/fr/man1/nano.1.gz
	+..... /usr/share/man/fr/man1/rnano.1.gz
	+..... /usr/share/man/fr/man5/nanorc.5.gz
	+..... /usr/share/man/man1/nano.1.gz
	+..... /usr/share/man/man1/rnano.1.gz
	+..... /usr/share/man/man5/nanorc.5.gz
	+..... /usr/share/nano
	+..... /usr/share/nano/asm.nanorc
	+..... /usr/share/nano/autoconf.nanorc
	+..... /usr/share/nano/awk.nanorc
	+..... /usr/share/nano/changelog.nanorc
	+..... /usr/share/nano/cmake.nanorc
	+..... /usr/share/nano/c.nanorc
	+..... /usr/share/nano/css.nanorc
	+..... /usr/share/nano/debian.nanorc
	+..... /usr/share/nano/default.nanorc
	+..... /usr/share/nano/elisp.nanorc
	+..... /usr/share/nano/fortran.nanorc
	+..... /usr/share/nano/gentoo.nanorc
	+..... /usr/share/nano/go.nanorc
	+..... /usr/share/nano/groff.nanorc
	+..... /usr/share/nano/guile.nanorc
	+..... /usr/share/nano/html.nanorc
	+..... /usr/share/nano/java.nanorc
	+..... /usr/share/nano/javascript.nanorc
	+..... /usr/share/nano/json.nanorc
	+..... /usr/share/nano/lua.nanorc
	+..... /usr/share/nano/makefile.nanorc
	+..... /usr/share/nano/man.nanorc
	+..... /usr/share/nano/mgp.nanorc
	+..... /usr/share/nano/mutt.nanorc
	+..... /usr/share/nano/nanorc.nanorc
	+..... /usr/share/nano/nftables.nanorc
	+..... /usr/share/nano/objc.nanorc
	+..... /usr/share/nano/ocaml.nanorc
	+..... /usr/share/nano/patch.nanorc
	+..... /usr/share/nano/perl.nanorc
	+..... /usr/share/nano/php.nanorc
	+..... /usr/share/nano/po.nanorc
	+..... /usr/share/nano/postgresql.nanorc
	+..... /usr/share/nano/pov.nanorc
	+..... /usr/share/nano/python.nanorc
	+..... /usr/share/nano/ruby.nanorc
	+..... /usr/share/nano/sh.nanorc
	+..... /usr/share/nano/spec.nanorc
	+..... /usr/share/nano/tcl.nanorc
	+..... /usr/share/nano/texinfo.nanorc
	+..... /usr/share/nano/tex.nanorc
	+..... /usr/share/nano/xml.nanorc
	c..... /var/cache/ldconfig/aux-cache
	+..... /var/lib/pacman/local/nano-2.5.3-1
	+..... /var/lib/pacman/local/nano-2.5.3-1/desc
	+..... /var/lib/pacman/local/nano-2.5.3-1/files
	+..... /var/lib/pacman/local/nano-2.5.3-1/install
	+..... /var/lib/pacman/local/nano-2.5.3-1/mtree

You can also do `snapper diff` in the same way - I'll spare you that one.

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
