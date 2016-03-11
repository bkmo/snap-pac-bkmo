# snap-pac

This makes Arch Linux's pacman use
[snapper](https://wiki.archlinux.org/index.php/Snapper) to automatically takes a
pre and post snapshot before and after pacman transactions, similar to how YaST
does with OpenSuse.

*Note:* The scripts only take snapshots of the subvolume mounted at `/`; other
subvolumes are not included. You must modify the scripts to include other
subvolumes.

The scripts are set up to use the `number` algorithm. That is, snapper will
periodically clean up snapshots tagged with `number` after reaching a set
threshold in the configuration file.

See `man alpm-hooks` and `man snapper` for more information.

## Installation

Install [the package from the AUR](https://aur.archlinux.org/packages/snap-pac/).

That's it! Continue to use pacman as normal and watch snapper do its thing.
