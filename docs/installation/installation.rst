============
Installation
============

The GUI Console is served as a web client by connecting to a separate web
address prepared by the admins. So, users do not need to install a
platform-dependent desktop applications, and just need the latest modern
browsers such as Chrome.

Recommended browser: latest Chrome (at least version 80)

After initial installation, we will provide following materials/services:

* User GUI Guide manual
* Admin GUI Guide manual (for Enterprise version)
* Installation report
* First-time user/admin on-site tutorial (3-5 hours)


==========================================
Backend.AI Server Installation Information
==========================================

Backend.AI server daemons are installed by Lablup support team. If there are
problems on the daemons or services, please contact with contact@lalbup.com.

Daemon information
------------------

Backend.AI is composed of many modules and daemons. Here, we briefly describe
each services and provide basic maintenance guide in case of specific service
failure. Note that the maintenance operations provided here are just generally
applicable, but may differ depending on the host-specific installation details.

Manager
^^^^^^^

Gateway server that accepts and handles every user requests. If the request is
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

Worker node. Manage the lifecycle of compute sessions (containers).

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

Serves user web GUI Console and provides authentication by email and password.

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
   dockner-compose -f docker-compose.wsproxy-simple.yaml -p <project> ps
   # start service
   dockner-compose -f docker-compose.wsproxy-simple.yaml -p <project> start
   # stop service
   dockner-compose -f docker-compose.wsproxy-simple.yaml -p <project> stop
   # restart service
   dockner-compose -f docker-compose.wsproxy-simple.yaml -p <project> restart
   # see logs
   dockner-compose -f docker-compose.wsproxy-simple.yaml -p <project> logs

PostgreSQL DB
^^^^^^^^^^^^^

Database for Manager.

.. code-block:: shell

   cd /home/lablup/halfstack
   # check status
   dockner-compose -f docker-compose.hs.postgres.yaml -p <project> ps
   # start service
   dockner-compose -f docker-compose.hs.postgres.yaml -p <project> start
   # stop service
   dockner-compose -f docker-compose.hs.postgres.yaml -p <project> stop
   # restart service
   dockner-compose -f docker-compose.hs.postgres.yaml -p <project> restart
   # see logs
   dockner-compose -f docker-compose.hs.postgres.yaml -p <project> logs

Redis
^^^^^

Cache server which is used to collect per-session and per-agent usage
statistics and relays heartbeat signal from Agent to Manager. It also keeps
user's authentication information.

.. code-block:: shell

   cd /home/lablup/halfstack
   # check status
   dockner-compose -f docker-compose.hs.redis.yaml -p <project> ps
   # start service
   dockner-compose -f docker-compose.hs.redis.yaml -p <project> start
   # stop service
   dockner-compose -f docker-compose.hs.redis.yaml -p <project> stop
   # restart service
   dockner-compose -f docker-compose.hs.redis.yaml -p <project> restart
   # see logs
   dockner-compose -f docker-compose.hs.redis.yaml -p <project> logs

Etcd
^^^^^

Config server, which contains Backend.AI system-wide configuration.

.. code-block:: shell

   cd /home/lablup/halfstack
   # check status
   dockner-compose -f docker-compose.hs.etcd.yaml -p <project> ps
   # start service
   dockner-compose -f docker-compose.hs.etcd.yaml -p <project> start
   # stop service
   dockner-compose -f docker-compose.hs.etcd.yaml -p <project> stop
   # restart service
   dockner-compose -f docker-compose.hs.etcd.yaml -p <project> restart
   # see logs
   dockner-compose -f docker-compose.hs.etcd.yaml -p <project> logs
