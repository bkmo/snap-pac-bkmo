Troubleshooting
===============

.. toctree::
   :maxdepth: 2

**snap-pac is only taking snapshots of the root configuration.**

That's the default behavior. See :doc:`configuration`.

**No snapshots are being taken when I run pacman.**

No snapper configurations are set up for snap-pac's pacman hooks. By default snap-pac
will take snapshots for the root configuration and any other configuration which has
SNAPSHOT set to yes in its configuration file. See :doc:`configuration`.

**After restoring snapshot from snap-pac, the pacman database is locked.**

The pre/post snaphots are taken while pacman is running, so this is expected.  Follow
the instructions pacman gives you (*e.g.*, removing the lock file). You can add the
database lock file to a snapper filter so that snapper  won't consider it when
performing snapper diff, snapper status, snapper undochange, etc. See the Filters
section in :manpage:`snapper(8)` for more information.
