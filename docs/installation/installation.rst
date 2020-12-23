============
Installation
============

The GUI console can be used in two forms. It can be used as a web service by
connecting to a separate web address prepared by the admins, or as an
app provided as a stand-alone executable file that does not require separate
installation. 

.. note::
   In the case of an app, depending on the security setting of the
   desktop OS, it may be recognized as an unsigned executable file
   and a permission check may be required.

With the web-based GUI console, users do not need to install a
platform-dependent desktop applications and just need the latest versions of
browsers such as Chrome. 

* Recommended browser: the latest version of Chrome (at least version > 80)
* Requirement: any machine that runs Web Browser (2 cores, 4 GiB memory)

.. note::
   We do not support MicroSoft Internet Explorer since it
   is deprecated and does not follow web standard and support up-to-date brower
   features.
   
For Backend.AI Server daemons/services, following hardware specification should be met. For
optimal performance, just double the amount of each resources.

* Manager: 2 cores, 4 GiB memory
* Agent: 4 cores, 32 GiB memory, NVIDIA GPU (for GPU workload), > 512 GiB SSD
* Console-Server: 2 cores, 4 GiB memory
* WSProxy: 2 cores, 4 GiB memory
* PostgreSQL DB: 2 cores, 4 GiB memory
* Redis: 1 core, 2 GiB memory
* Etcd: 1 core, 2 GiB memory

The essential host dependent packages that must be pre-installed before installing
each service are:

* GUI console: Operating system that can run the latest browsers (Windows, Mac
  OS, Ubuntu, etc.)
* Manager: Python (≥3.8), pyenv/pyenv-virtualenv (≥1.2)
* Agent: docker (≥19.03), CUDA/CUDA Toolkit (≥8, 11 recommend),
  nvidia-docker v2, Python (≥3.8), pyenv/pyenv-virtualenv (≥1.2)
* Console-Server: Python (≥3.8), pyenv/pyenv-virtualenv (≥1.2)
* WSProxy: docker (≥19.03), docker-compose (≥1.24)
* PostgreSQL DB: docker (≥19.03), docker-compose (≥1.24)
* Redis: docker (≥19.03), docker-compose (≥1.24)
* Etcd: docker (≥19.03), docker-compose (≥1.24)

For Enterprise version, Backend.AI server daemons are installed by Lablup support team and following materials/services are provided after initial installation:

* DVD 1 (includes Backend.AI packages)
* User GUI Guide manual
* Admin GUI Guide manual
* Installation report
* First-time user/admin on-site tutorial (3-5 hours)

Product maintenance and support information: the commercial contract includes a
monthly/annual subscription fee for the Enterprise version by default. Initial
user/administrator training (1-2 times) and wired/wireless customer support
services are provided for about 2 weeks after initial installation, minor
release updater support and customer support services through online channels
are provided for 3-6 months. Maintenance and support services provided
afterwards may have different details depending on the terms of the contract.

Users of the open source version can also purchase an installation and support
plan separately.

Simple Backend.AI Server Management Guide
-----------------------------------------

Backend.AI is composed of many modules and daemons. Here, we briefly describe
each services and provide basic maintenance guide in case of specific service
failure. Note that the maintenance operations provided here are generally
applicable, but may differ depending on the host-specific installation details.

Manager
^^^^^^^

Gateway server that accepts and handles every user request. If the request is
related with the compute session (container), Manager will delegate the request
to Agent and/or containers in each Agent.

.. code-block:: shell

   # check status
   sudo systemctl status backendai-manager
   # start service
   sudo systemctl start backendai-manager
   # stop service
   sudo systemctl stop backendai-manager
   # restart service
   sudo systemctl restart backendai-manager
   # see logs
   sudo journalctl --output cat -u backendai-manager

Agent
^^^^^

Worker node which manages the lifecycle of compute sessions (containers).

.. code-block:: shell

   # check status
   sudo systemctl status backendai-agent
   # start service
   sudo systemctl start backendai-agent
   # stop service
   sudo systemctl stop backendai-agent
   # restart service
   sudo systemctl restart backendai-agent
   # see logs
   sudo journalctl --output cat -u backendai-agent

Console-Server
^^^^^^^^^^^^^^

Serves user GUI Console and provides authentication by email and password.

.. code-block:: shell

   # check status
   sudo systemctl status backendai-console-server
   # start service
   sudo systemctl start backendai-console-server
   # stop service
   sudo systemctl stop backendai-console-server
   # restart service
   sudo systemctl restart backendai-console-server
   # see logs
   sudo journalctl --output cat -u backendai-console-server

WSProxy
^^^^^^^

Proxies the connection between user-created web apps (such as web Terminal and
Jupyter Notebook) and Manager, which is then relayed to a specific compute
session (container).

.. code-block:: shell

   cd /home/lablup/halfstack
   # check status
   docker-compose -f docker-compose.wsproxy-simple.yaml -p <project> ps
   # start service
   docker-compose -f docker-compose.wsproxy-simple.yaml -p <project> up -d
   # stop service
   docker-compose -f docker-compose.wsproxy-simple.yaml -p <project> down
   # restart service
   docker-compose -f docker-compose.wsproxy-simple.yaml -p <project> restart
   # see logs
   docker-compose -f docker-compose.wsproxy-simple.yaml -p <project> logs

PostgreSQL DB
^^^^^^^^^^^^^

Database for Manager.

.. code-block:: shell

   cd /home/lablup/halfstack
   # check status
   docker-compose -f docker-compose.hs.postgres.yaml -p <project> ps
   # start service
   docker-compose -f docker-compose.hs.postgres.yaml -p <project> up -d
   # stop service
   docker-compose -f docker-compose.hs.postgres.yaml -p <project> down
   # restart service
   docker-compose -f docker-compose.hs.postgres.yaml -p <project> restart
   # see logs
   docker-compose -f docker-compose.hs.postgres.yaml -p <project> logs

To back up the DB data, you can use the following commands from the DB host. The
specific commands may vary depending on the configuration.

.. code-block:: shell

   # query postgresql container's ID
   docker ps | grep halfstack-db
   # Connect to the postgresql container via bash
   docker exec -it <postgresql-container-id> bash
   # Backup DB data. PGPASSWORD may vary depending on the system configuration
   PGPASSWORD=develove pg_dumpall -U postgres > /var/lib/postgresql/backup_db_data.sql
   # Exit container
   exit

To restore the DB from the backup data, you can execute the following commands.
Specific options may vary depending on the configuration.

.. code-block:: shell

   # query postgresql container's ID
   docker ps | grep halfstack-db
   # Connect to the postgresql container via bash
   docker exec -it <postgresql-container-id> bash
   # Disconnect all connection, for safety
   psql -U postgres
   postgres=# SELECT pg_terminate_backend(pg_stat_activity.pid)
   postgres-# FROM pg_stat_activity
   postgres-# WHERE pg_stat_activity.datname = 'backend'
   postgres-# AND pid <> pg_backend_pid();
   # Ensure previous data be cleaned (to prevent overwrite)
   postgres=# DROP DATABASE backend;
   postgres=# \q
   # Restore from data
   psql -U postgres < backup_db_data.sql

Redis
^^^^^

Cache server which is used to collect per-session and per-agent usage
statistics and relays heartbeat signal from Agent to Manager. It also keeps
user's authentication information.

.. code-block:: shell

   cd /home/lablup/halfstack
   # check status
   docker-compose -f docker-compose.hs.redis.yaml -p <project> ps
   # start service
   docker-compose -f docker-compose.hs.redis.yaml -p <project> up -d
   # stop service
   docker-compose -f docker-compose.hs.redis.yaml -p <project> down
   # restart service
   docker-compose -f docker-compose.hs.redis.yaml -p <project> restart
   # see logs
   docker-compose -f docker-compose.hs.redis.yaml -p <project> logs

Usually, Redis data do not need backup since it contains temporary cached data
only, such user's login session information, per-container live stat, and etc.

Etcd
^^^^^

Config server, which contains Backend.AI system-wide configuration.

.. code-block:: shell

   cd /home/lablup/halfstack
   # check status
   docker-compose -f docker-compose.hs.etcd.yaml -p <project> ps
   # start service
   docker-compose -f docker-compose.hs.etcd.yaml -p <project> up -d
   # stop service
   docker-compose -f docker-compose.hs.etcd.yaml -p <project> down
   # restart service
   docker-compose -f docker-compose.hs.etcd.yaml -p <project> restart
   # see logs
   docker-compose -f docker-compose.hs.etcd.yaml -p <project> logs

To back up the Etcd config data used by the Manager, go to the folder where the
Manager is installed and use the following command.

.. code-block:: shell

   cd /home/lablup/manager  # paths may vary
   backend.ai mgr etcd get --prefix '' > etcd_backup.json

To restore Etcd settings from the backup data, you can run a command like this.

.. code-block:: shell

   cd /home/lablup/manager  # paths may vary
   backend.ai mgr etcd put-json '' etcd_backup.json
