# snap-pac

![Tests](https://github.com/wesbarnett/snap-pac/workflows/Tests/badge.svg)
![Docs](https://github.com/wesbarnett/snap-pac/workflows/Docs/badge.svg)

## Synopsis

This is a set of pacman hooks and script that automatically causes snapper to
perform a pre and post snapshot before and after pacman transactions, similar to
how YaST does with OpenSuse. This provides a simple way to undo changes to a
system after a pacman transaction.

## Installation

Install the `snap-pac` package using pacman.

Alternatively [download the latest release] and signature , verify the download, and
then run `make install`.

I have signed the release tarball and commits with my PGP key.  Starting with release
2.2, the tarballs are signed with my key with fingerprint
`F7B28C61944FE30DABEEB0B01070BCC98C18BD66`.

For previous releases, the key's fingerprint was
`8535CEF3F3C38EE69555BF67E4B5E45AA3B8C5C3`.

## Configuration

Most likely, configuration is not needed. By default, the snapper configuration named
`root` will have pre/post snapshots taken for every pacman transaction.

To configure, copy the example configuration file:

```bash
cp /etc/snap-pac.ini{.example,}
```

Then edit with your favorite editor. The file is commented and should be
self-explanatory.

## Documentation

See the [documentation here](https://wesbarnett.github.io/snap-pac/).

## Troubleshooting

After reviewing the documentation, [check the issues page] and file a new issue if your
problem is not covered.

[download the latest release]: https://github.com/wesbarnett/snap-pac/releases
[check the issues page]: https://github.com/wesbarnett/snap-pac/issues
