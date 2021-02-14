# snap-pac

![Tests](https://github.com/wesbarnett/snap-pac/workflows/Run%20Python%20Tests/badge.svg)

## Synopsis

This is a set of pacman hooks and script that automatically causes snapper to
perform a pre and post snapshot before and after pacman transactions, similar to
how YaST does with OpenSuse. This provides a simple way to undo changes to a
system after a pacman transaction.

## Installation

Install the `snap-pac` package using pacman.

Alternatively [download the latest release] and signature , verify the download, and
then run `make install`.

I have signed the release tarball and commits with my PGP key. The key's
fingerprint is `8535CEF3F3C38EE69555BF67E4B5E45AA3B8C5C3`.

Starting with release 2.2, the tarballs are signed with my key with fingerprint `F7B2
8C61 944F E30D ABEE  B0B0 1070 BCC9 8C18 BD66`.

## Configuration

An commented example configuration file is located at `extras/snap-pac.ini` which is
installed to `/etc/snap-pac.ini.example`. By default only the snapper configuration
named `root` has snapshots taken before and after pacman transactions. See the example
configuration file for how to add other snapper configurations.

## Documentation

Run `man 8 snap-pac` after installation.

## Troubleshooting

After reviewing the man page, [check the issues page] and file a new issue if your
problem is not covered.

[download the latest release]: https://github.com/wesbarnett/snap-pac/releases
[check the issues page]: https://github.com/wesbarnett/snap-pac/issues
