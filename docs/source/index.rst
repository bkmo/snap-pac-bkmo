.. snap-pac documentation master file, created by
   sphinx-quickstart on Thu Mar 11 19:49:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

snap-pac
========

.. toctree::
   :maxdepth: 2

   installation
   configuration
   examples
   troubleshooting
   faq

This is a set of `pacman <https://archlinux.org/pacman/>`_ hooks and script that causes
`snapper <http://snapper.io/>`_ to automatically take a pre and post snapshot before and
after pacman transactions, similar to how `YaST <https://yast.opensuse.org/>`_ does with
OpenSuse. This provides a simple way to undo changes to a system after a pacman
transaction.

Because these are pacman hooks, it doesn't matter how you call pacman—whether
directly, through an AUR helper, or using an alias—snapper will create the snapshots
when pacman installs, upgrades, or removes a package. The pacman command used is
logged in the snapper description for the snapshots. Additionally the snapshot numbers
are output to the screen and to the pacman log for each snapper configuration during the
pacman transaction, so that the user can easily find which changes he or she may want to
revert.

To undo changes from a pacman transaction, use ``snapper undochange``. See the `snapper
documentation <http://snapper.io/documentation.html>`_ for more details as well as
examples.

If you have severe breakage—like snapper is gone for some reason and you can't get it
back—you'll have to resort to more extreme methods, such as taking a snapshot of the pre
snapshot and making it the default subvolume or mounting it as /. Most likely you'll
need to use a live USB to get into a chroot environment to do any of these things.
Snapper has a ``snapper rollback`` feature, but your setup has to be properly configured to
use it. The exact procedure depends on your specific setup. Be careful.
