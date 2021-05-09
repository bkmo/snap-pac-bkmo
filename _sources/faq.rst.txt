FAQ
===

.. toctree::
   :maxdepth: 2

**Does snap-pac backup non-btrfs /boot partitions?**

No, but you can add a hook that does it for you. It would be something like the following:

.. code-block:: none

	[Trigger]
	Operation = Upgrade
	Operation = Install
	Operation = Remove
	Type = Package
	Target = linux

	[Action]
	Description = Backing up /boot...
	When = PreTransaction
	Exec = /usr/bin/rsync -avzq --delete /boot /.bootbackup

Note that you will probably want to name the file with a numbered prefix less than
``05`` so that it is run before the snap-pac pre snapshot takes place. That will ensure
that the snapshot taken will have the boot partition back-up corresponding with the
state of the system. For example, you could name it ``04-backupboot.hook``.


**How do I link old kernel modules automatically when the kernel is upgraded?**

This behavior is no longer a part of this package. Use a pacman hook like the following:

.. code-block:: none

	[Trigger]
	Operation = Upgrade
	Operation = Install
	Operation = Remove
	Type = Package
	Target = linux

	[Action]
	Description = Symlinking old kernel modules...
	When = PostTransaction
	Exec = /usr/bin/bash -c "find /usr/lib/modules -xtype l -delete; ln -sv /.snapshots/$(snapper -c root list | awk 'END{print $1}')/snapshot/usr/lib/modules/$(uname -r) /usr/lib/modules/"
