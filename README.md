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

For instructions on how to install without pacman, [see the
documentation](https://wesbarnett.github.io/snap-pac/installation.html).

## Configuration

Most likely, configuration is not needed. By default, the snapper configuration named
`root` will have pre/post snapshots taken for every pacman transaction.

For more information on configuring snap-pac, see [the
documentation](https://wesbarnett.github.io/snap-pac/configuration.html).

## Documentation

See the [documentation here](https://wesbarnett.github.io/snap-pac/) or `man 8 snap-pac`
after installation.

## Troubleshooting

After reviewing the documentation, [check the issues page] and file a new issue if your
problem is not covered.

[check the issues page]: https://github.com/wesbarnett/snap-pac/issues
