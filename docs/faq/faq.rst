==================
FAQ & Troubleshoot
==================

Session list is not display correctly
-------------------------------------

Due to intermittent network problems and/or other various reasons, session list
may not displayed correctly. Most of the time, this problem will be gone just by
refreshing the browser.

Suddenly, I cannot login with my account
----------------------------------------

Sometimes, there are problems in the recognition of authentication cookies.  Try
to login with private browser window. If it succeeds, please clear your
browser's cache and/or application data.

How to install apt packages?
----------------------------

Inside a compute session, user cannot access root account and perform operations
that require sudo privilge for security reasons. So, it is generally not
possible to install packages from apt or yum since they requires sudo.
Alternatively, user may install packages by
`brew <https://docs.brew.sh/Homebrew-on-Linux>`.

To install and use ``brew`` from the compute session, follow commands below:

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

How to install pip packages?
----------------------------

Like ``brew``, it is possible to install ``pip`` packages under ``~/.local`` by
providing ``--user`` option.

.. code-block:: shell

   $ pip install --user aiohttp

I can create a compute session, but cannot launch Jupyter Notebook
------------------------------------------------------------------

There may be a problem on connecting WSProxy service. Try to stop and restart
the service by referencing the guide on start/stop/restart WSProxy service.

Indicated resources are not match with actual allocation
--------------------------------------------------------

Occasionally, due to unstable network connections or container management
problem of Docker daemon, there may be a case where the resource occupied by
Backend.AI does not match the resource actually used by the container. In this
case, try to follow the steps below.

* Login as admin account.
* Visit Maintenance page.
* Click the RECALCULATE USAGE button to manually correct the resource occupancy.

Page layout is weird
--------------------

Backend.AI Console utilizes most modern JavaScript and/or browser features.
Please use the LATEST versions of moder browsers (such as Chrome).

Service unreachable
-------------------

Some backend services may have been down. Try to stop and restart services by
following guide on start/stop/restart <service-name> service.


Start/stop/restart Manager service
----------------------------------

SSH into Manager node, and run either of following command.

.. code-block:: shell

   systemctl start backendai-manager
   systemctl stop backendai-manager
   systemctl restart backendai-manager

Start/stop/restart Agent service
--------------------------------

SSH into Agent node, and run either of following command.

.. code-block:: shell

   systemctl start backendai-agent
   systemctl stop backendai-agent
   systemctl restart backendai-agent

Start/stop/restart Console-Server service
-----------------------------------------

SSH into Console-Server node, and run either of following command.

.. code-block:: shell

   systemctl start backendai-console-server
   systemctl stop backendai-console-server
   systemctl restart backendai-console-server

Start/stop/restart database
---------------------------

SSH into DB node, and run either of following command. Note that <project>
should be manually written if it was provided when launching the service. It can
be checked by running ``docker ps | grep postgres`` and see the name prefix for
the corresponding container or something like that.

.. code-block:: shell

   docker-compose -f docker-compose.hs.postgres.yaml -p <project> up -d
   docker-compose -f docker-compose.hs.postgres.yaml -p <project> down
   docker-compose -f docker-compose.hs.postgres.yaml -p <project> restart

Start/stop/restart Redis
------------------------

SSH into Redis node, and run either of following command. Note that <project>
should be manually written if it was provided when launching the service. It can
be checked by running ``docker ps | grep redis`` and see the name prefix for
the corresponding container or something like that.

.. code-block:: shell

   docker-compose -f docker-compose.hs.redis.yaml -p <project> up -d
   docker-compose -f docker-compose.hs.redis.yaml -p <project> down
   docker-compose -f docker-compose.hs.redis.yaml -p <project> restart

Start/stop/restart Etcd
-----------------------

SSH into Etcd node, and run either of following command. Note that <project>
should be manually written if it was provided when launching the service. It can
be checked by running ``docker ps | grep etcd`` and see the name prefix for
the corresponding container or something like that.

.. code-block:: shell

   docker-compose -f docker-compose.hs.etcd.yaml -p <project> up -d
   docker-compose -f docker-compose.hs.etcd.yaml -p <project> down
   docker-compose -f docker-compose.hs.etcd.yaml -p <project> restart

Start/stop/restart WSProxy
---------------------------

SSH into WSProxy node, and run either of following command. Note that <project>
should be manually written if it was provided when launching the service. It can
be checked by running ``docker ps | grep proxy`` and see the name prefix for
the corresponding container or something like that.

.. code-block:: shell

   docker-compose -f docker-compose.hs.wsproxy.simple.yaml -p <project> up -d
   docker-compose -f docker-compose.hs.wsproxy.simple.yaml -p <project> down
   docker-compose -f docker-compose.hs.wsproxy.simple.yaml -p <project> restart


