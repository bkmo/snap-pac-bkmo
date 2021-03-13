Installation
============

Install the ``snap-pac`` package using pacman:

.. code-block:: bash

   pacman -S snap-pac

Alternatively download the `latest release and signature
<https://github.com/wesbarnett/snap-pac/releases>`_. Then, verify the download:

.. code-block:: bash

   gpg --verify snap-pac-<version>.tar.gz.sig

where ``<version>`` is the version number you downloaded.

Finally, run:

.. code-block:: bash

    make install

I have signed the release tarball and commits with my PGP key. Starting with release
2.2, the tarballs are signed with my key with fingerprint
``F7B28C61944FE30DABEEB0B01070BCC98C18BD66``.

For previous releases, the key's fingerprint was
``8535CEF3F3C38EE69555BF67E4B5E45AA3B8C5C3``.
