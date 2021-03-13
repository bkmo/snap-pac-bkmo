Configuration
=============

.. toctree::
   :maxdepth: 2

Configuration  is  done  via  Python  ini  configuration files. The defaults
should be suitable for most users, so you may not need to do any configuration at all.
By default only the ``root`` snapper configuration is snapshotted.

A commented example configuration files is located at ``/etc/snap-pac.ini.example``.

To configure, copy the example configuration file:

.. code-block:: bash

    cp /etc/snap-pac.ini{.example,}

Then edit with your favorite editor. The file is commented and should be
self-explanatory.

Each section corresponds with a snapper configuration. Add additional sections to add
other snapper configurations to be snapshotted. By default, only the root configuration
is snapshotted.

Environment Variables
---------------------

To temporarily prevent snapshots from being performed for a single pacman
command, set the environment variable ``SNAP_PAC_SKIP``. For example:

.. code-block:: bash

    sudo SNAP_PAC_SKIP=y pacman -Syu
