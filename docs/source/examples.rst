Example
=======

.. toctree::
   :maxdepth: 2

Here is an example of how the snapshots are created and how to rollback and pacman
transaction. Here the nano package is installed:

.. code-block:: bash

	pacman -S nano

.. code-block:: none

	resolving dependencies...
	looking for conflicting packages...

	Packages (1) nano-2.5.3-1

	Total Installed Size:  2.14 MiB

	:: Proceed with installation? [Y/n] Y
	(1/1) checking keys in keyring                               [######################################] 100%
	(1/1) checking package integrity                             [######################################] 100%
	(1/1) loading package files                                  [######################################] 100%
	(1/1) checking for file conflicts                            [######################################] 100%
	(1/1) checking available disk space                          [######################################] 100%
	:: Running pre-transaction hooks...
	(1/1) Performing snapper pre snapshots for the following configurations...
	=> root: 1033
	:: Processing package changes...
	(1/1) installing nano                                        [######################################] 100%
	:: Running post-transaction hooks...
	(1/1) Performing snapper post snapshots for the following configurations...
	=> root: 1034

The snapper snapshot number is given for each snapper configuration that is used. This
is also logged in pacman's log.

Here are the snapshots created before and after the pacman transaction:

.. code-block:: bash

	snapper -c root list -t pre-post | tail -n 1

.. code-block:: none

	1033  | 1034   | Fri 22 Apr 2016 01:54:13 PM CDT | Fri 22 Apr 2016 01:54:14 PM CDT | pacman -S nano      |

Here is what changed during the transaction:

.. code-block:: bash

	snapper -c root status 1033..1034

.. code-block:: none

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

The above output is truncated, but it continues. See the `snapper(8)
<http://snapper.io/manpages/snapper.html>`_ to for what each symbol means. You can also
do ``snapper diff`` in the same way.

Then, to undo the pacman transaction:

.. code-block:: bash

	snapper -c root undochange 1033..1034

.. code-block:: none

	create:0 modify:3 delete:100

Now nano is no longer installed, along with all the files it changed:

.. code-block:: bash

	pacman -Qi nano

.. code-block:: none

	error: package 'nano' was not found
