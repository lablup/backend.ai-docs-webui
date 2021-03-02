=======================
FAQs & Trouble Shooting
=======================

If you use the Web-UI for a long time, you may experience connection
problems to Jupyter and/or terminal service, or compute session list not
updating. Those problems often disappear when you refresh the Web-UI page. You
may refresh the Web-UI by following methods.

- Web-based Web-UI: Refresh the browser page (use the shortcut provided by
  browsers such as Ctrl-R). Since the browser's cache may cause troubles
  sometimes, it is recommended to refresh the page bypassing the cache
  (such as Shift-Ctrl-R, but the keys may differ in each browser).
- Web-UI App: Press Ctrl-R shortcut to refresh the app.


Session list is not displayed correctly
---------------------------------------

Due to intermittent network problems and/or other various reasons, session list
may not be displayed correctly. Most of the time, this problem will disappear just by
refreshing the browser.

Suddenly, I cannot login with my account
----------------------------------------

If there are problems in recognizing authentication cookies, users may not be able to login temporarily. Try
to login with private browser window. If it succeeds, please clear your
browser's cache and/or application data.

How to install apt packages?
----------------------------

Inside a compute session, users cannot access root account and perform operations
that require sudo privilege for security reasons. Therefore, it is not allowed to install packages with apt or yum since they require sudo.
Alternatively, users may install packages by
`brew <https://docs.brew.sh/Homebrew-on-Linux>`_.

To install and use ``brew`` from the compute session, follow the commands below:

.. code-block:: shell

   $ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   $ test -d ~/.linuxbrew && eval $(~/.linuxbrew/bin/brew shellenv)
   $ test -d /home/linuxbrew/.linuxbrew && eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)
   $ test -r ~/.bash_profile && echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.bash_profile
   $ echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile

Now, you can install packages by ``brew``:

.. code-block:: shell

   $ brew install hello

``brew`` installs packages under ``~/.local``. So, if you create a storage
folder named ``.local``, which will be automatically mounted when creating a
compute session, those installed packages can be kept after compute session is
destroyed and then reused for the next compute session.

How to install packages with pip?
---------------------------------

Like ``brew``, it is possible to install the packages under ``~/.local`` by
providing ``--user`` option when using ``pip``.

.. code-block:: shell

   $ pip install --user aiohttp

I have created a compute session, but cannot launch Jupyter Notebook
--------------------------------------------------------------------

There may be a problem on connecting WSProxy service. Try to stop and restart
the service by referencing the guide on start/stop/restart WSProxy service.

Indicated resources do not match with actual allocation
--------------------------------------------------------

Occasionally, due to unstable network connections or container management
problem of Docker daemon, there may be a case where the resource occupied by
Backend.AI does not match with the resource actually used by the container. In this
case, follow the steps below.

* Login as admin account.
* Visit Maintenance page.
* Click the RECALCULATE USAGE button to manually correct the resource occupancy.

Image is not displayed after it is pushed to a docker registry
--------------------------------------------------------------

.. note::
   This feature is only available for superadmins.

If a new image is pushed to one of the Backend.AI docker registries, the image
metadata must be updated in Backend.AI to be used in creating a compute session.
Metadata update can be performed by clicking the RESCAN IMAGES button on the
Maintenance page. This will update metadata for every docker registry, if
there are multiple registries.

If you want to update the metadata for a specific docker registry, you can go to
the Registries tab in Environments page.  Just click the refresh button in the
Controls panel of the desired registry. Be careful not to delete the registry
by clicking the trash icon.

Page layout is broken
---------------------

Backend.AI Web-UI utilizes the latest modern JavaScript and/or browser features.
Please use the LATEST versions of moder browsers (such as Chrome).

SFTP disconnection
------------------

When Web-UI App launches SFTP connection, it uses a local proxy server which is
embeded in the App. If you exit the Web-UI App during the file transfer with
SFTP protocol, the transfer will immediately fail because the connection
established through the local proxy server is disconnected.  Therefore, even if
you are not using a compute session, you should not quit the Web-UI App while
using SFTP. If you need to refresh the page, we recommend using the Ctrl-R
shortcut.

If the Web-UI App is closed and restarted, the SFTP service is not
automatically initiated for the existing compute session. You must explicitly
start the SSH/SFTP service in the desired container to establish the SFTP
connection.

