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
is snapshotted. Additionally you can add a section named ``DEFAULT`` with options that
apply to all snapper configurations unless overridden in a later section.

Each section can have the following entries:

**desc_limit** - integer; maximum length of description string before being truncated.
Default: 72

**important_packages** - list of strings; names of packages that if involved in a pacman
transaction will add ``important=yes`` to the snapper userdata for the pair of
snapshots. Default: []

**important_commands** - list of strings; parent commands that will add
``important=yes`` to the snapper userdata for the pair of snapshots. Default: []

**pre_description** - string; description for the pre snapshot. Default: the parent
command that called the pacman hook.

**post_description** - string; description for the post snapshot. Default: space
separated list of packages that were installed, upgraded, or removed.

**snapshot** - boolean; whether or not to snapshot the configuration. Default: True for
``root`` configuration; False otherwise.

**userdata** - list of strings; key-value pairs that will be added to the userdata for
the pair of snapshots. Default: []


Environment Variables
---------------------

To temporarily prevent snapshots from being performed for a single pacman
command, set the environment variable ``SNAP_PAC_SKIP``. For example:

.. code-block:: bash

    sudo SNAP_PAC_SKIP=y pacman -Syu
