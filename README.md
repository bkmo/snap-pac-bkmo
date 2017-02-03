# snap-pac

[![Arch Version](https://img.shields.io/badge/Arch-0.8.2-brightgreen.svg)](https://git.archlinux.org/svntogit/community.git/tree/trunk/PKGBUILD?h=packages/snap-pac)
[![License](https://img.shields.io/github/license/wesbarnett/snap-pac.svg)](https://github.com/wesbarnett/snap-pac/blob/master/LICENSE)

This is a set of pacman hooks and script that causes
[snapper](https://wiki.archlinux.org/index.php/Snapper) to automatically take a
pre and post snapshot before and after pacman transactions, similar to how YaST
does with OpenSuse. This provides a simple way to undo changes to a system after
a pacman transaction.

## PGP Key

I have signed the release tarball with my PGP key. You may need to import my
public key before installation:

    $ gpg --keyserver hkp://pgp.mit.edu --recv-keys 0xE4B5E45AA3B8C5C3

The key's fingerprint is `8535CEF3F3C38EE69555BF67E4B5E45AA3B8C5C3`.

## Documentation

See `man 7 snap-pac` after installation.
