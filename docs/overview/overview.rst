========
Overview
========

Backend.AI is an open source cloud resource management platform, which makes it
easy to utilize virtualized compute resource clusters in a cloud or on-premises
environment. The container-based GPU virtualization technology of Backend.AI
supports the efficient use of GPUs by flexibly dividing one physical GPU, so
that multiple users can use it at the same time.

Backend.AI offers a variety of performance-driven optimizations for machine
learning and high-performance computing clusters, along with management and
research features to support a diverse users, including researchers,
administrators, and DevOps. The Enterprise Edition adds support for multi-domain
management, a dedicated Control-Panel for superadmins, and the GPU
virtualization plug-in.

A GUI client package is provided to easily take advantage of the features
supported by the Backend.AI server. Backend.AI Web-UI is a GUI client in the form
of a web service or stand-alone app. It provides a convenient graphical
interface for accessing the Backend.AI server to utilize computing resources and
manage its environment. Backend.AI provides pre-made images which enable
immediate creation of compute sessions without any need of installing separate
programs.  Most tasks can be done with mouse clicks and brief typing, which
achieves more intuitive use.


Key Concepts
------------

.. image:: key_concepts.png
   :alt: Diagram explaining key concepts

- User: The user is a person who connects to Backend.AI and performs work.
  Users are divided into normal users, domain admins, and superadmins according
  to their privileges. While ordinary users can only perform tasks related to
  their computing sessions, domain admins have the authority to perform
  tasks within a domain, and superadmins perform almost all tasks throughout the
  system. A user belongs to one domain and can belong to
  multiple groups within a domain.
- Compute session, container: An isolated virtual environment in which your
  code runs. It looks like a real Linux server with full user rights,
  and you can't see other user's session even if it's running on the same
  server as your session. Backend.AI implements this virtual environment through
  a technology called containers. You can only create compute sessions within
  the domain and groups to which you belong.
- Domain: This is the top layer for authority and resource control supported by
  Backend.AI. For companies or organizations, you can view domains as an
  affiliate and set up per-domain (or per-affiliate) permissions and resource
  policies. Users should belong to only one domain, and can create sessions or
  do some other jobs only in their own domain. A domain can have one domain admin or
  more, who can set policies within the domain or manage
  sessions. For example, if you set the total amount of resources available in a
  domain, the resources of all containers created by users in the domain cannot
  be greater than the amount set.
- Groups: A hierarchy belonging to a domain. Multiple groups can exist in one
  domain. You can think of a group as a project unit. A user can belong to
  multiple groups (or projects) at the same time within a domain. Compute
  sessions must belong to one group, and users can only create sessions within
  their own groups. Domain admins can set policies or manage sessions for
  groups within the domain. For example, if you set the total amount of
  resources available within a group, the resources in all containers created by
  users in the group cannot be greater than the amount set.
- Image: Each container has a pre-installed language-specific runtime and
  various computational frameworks. The state of such snapshots before they are
  executed is called an image. You can choose to run an image provided by the
  cluster admin or create your own image with the software you want to
  use and ask the admin to register it.
- Virtual Folder (vfolder): A "cloud" folder that is always accessible and
  mountable in a container on a per-user basis, regardless of which node the
  container runs on. After creating your own virtual folder, you can upload your
  own program code, data, etc. in advance and mount the folder when you run the
  compute session to read from and write to it as if it is on your local disk.
- Application service, service port: A feature that allows you to access various
  user applications (eg DIGITS, Jupyter Notebook, shell terminal, TensorBoard,
  etc.) running within the compute session. You do not need to know the
  container's address and port number directly, but you can use the provided CLI
  client or GUI Web-UI to directly access the desired daemon of the session.
- Web-UI: A GUI client that is served as a web or stand-alone app.
  You can use the service after logging in by specifying the address of the
  Backend.AI server and entering the user account information.
- Local wsproxy: Proxy server built into the Web-UI app. Local wsproxy converts
  general HTTP requests between the server and Web-UI app to websocket and
  delivers the messages. If the Web-UI app loses its connection to wsproxy or
  the wsproxy server is dead, it will not be possible to access services such as
  Jupyter Notebook and Terminal.
- Web wsproxy: In the case of the Web-UI provided in a web, the built-in
  server cannot be used due to the nature of the browser. In this case, you
  can use services such as Jupyter Notebook, Terminal, etc. in the web
  environment by making the wsproxy server as a separate web server
  so that the Web-UI app can see the web wsproxy.


Backend.AI feature details
--------------------------

+----------------------+-------------------------------------------------------+
| Category             | Feature                                               |
+======================+=======================================================+
| GPU support          | Container-level multi GPU                             |
+                      +-------------------------------------------------------+
|                      | (Enterprise) Fractional GPU sharing & scaling         |
+                      +-------------------------------------------------------+
|                      | Multiple CUDA library version support (8.0 to 11.1)   |
+----------------------+-------------------------------------------------------+
| Scaling              | On-premise installation on both bare-metal / VM       |
+                      +-------------------------------------------------------+
|                      | Hybrid cloud (on-premise + cloud)                     |
+                      +-------------------------------------------------------+
|                      | Polycloud (multi-cloud federation)                    |
+----------------------+-------------------------------------------------------+
| Scheduling           | Unified scheduling & monitoring with GUI admin        |
+                      +-------------------------------------------------------+
|                      | Per-user (keypair) resource policy                    |
+                      +-------------------------------------------------------+
|                      | (Enterprise) Per-group resource policy                |
+                      +-------------------------------------------------------+
|                      | Availability-slot based scheduling                    |
+----------------------+-------------------------------------------------------+
| Cluster partitioning | Resource groups by H/W spec and usage                 |
+                      +-------------------------------------------------------+
|                      | (Enterprise) Access control of users to               |
|                      | resource group                                        |
+                      +-------------------------------------------------------+
|                      | (Enterprise) Access control of group to               |
|                      | resource group                                        |
+----------------------+-------------------------------------------------------+
| Security             | Sandboxing via hypervisor/container                   |
+                      +-------------------------------------------------------+
|                      | Access logs for each user                             |
+                      +-------------------------------------------------------+
|                      | Per session (container) logs                          |
+----------------------+-------------------------------------------------------+
| UI / UX              | GUI web interface                                     |
+                      +-------------------------------------------------------+
|                      | (Enterprise) Admin GUI web interface                  |
+----------------------+-------------------------------------------------------+
| Data management      | EFS, NFS, SMB and distributed file system             |
|                      | (CephFS, GlusterFS, HDFS, etc)                        |
+                      +-------------------------------------------------------+
|                      | (Enterprise) Dedicated flash-storage integration:     |
|                      | PureStorage FlashBlade                                |
+                      +-------------------------------------------------------+
|                      | Access control to data by user/group                  |
+----------------------+-------------------------------------------------------+
| Developer support    | Universal programming languages (Python, C/C++, etc)  |
+                      +-------------------------------------------------------+
|                      | Interactive web apps (Terminal, Jupyter, VSCode, etc) |
+----------------------+-------------------------------------------------------+
| For data scientists  | NGC (NVIDIA GPU CLoud) image integration              |
+                      +-------------------------------------------------------+
|                      | Popular ML libraries: TensorFlow, PyTorch, etc        |
+                      +-------------------------------------------------------+
|                      | Concurrent user of multiple versions of libraries     |
+                      +-------------------------------------------------------+
|                      | Periodic update of ML libraries                       |
+----------------------+-------------------------------------------------------+
| Customer support     | On-site installation (bare-metal / VM)                |
+                      +-------------------------------------------------------+
|                      | Configuration support (on-premise + cloud)            |
+                      +-------------------------------------------------------+
|                      | Admin/user training                                   |
+                      +-------------------------------------------------------+
|                      | Support for updating to latest version                |
+                      +-------------------------------------------------------+
|                      | Priority development and escalation                   |
+                      +-------------------------------------------------------+
|                      | Custmoized container image / kernel or kernel         |
|                      | repository                                            |
+----------------------+-------------------------------------------------------+


Accessible menu by user role
--------------------------------------

.. note::

   * Pages with ``*`` mark are in Administration menu.
   * Features only for admin are listed in :ref:`admin menu <admin-menu>`.

+----------------+------+-------+
| page \\ role   | user | admin |
+================+======+=======+
| Summary        |   O  |   O   |
+----------------+------+-------+
| Sessions       |   O  |   O   |
+----------------+------+-------+
| Data & Storage |   O  |   O   |
+----------------+------+-------+
| Statistics     |   O  |   O   |
+----------------+------+-------+
| Users*         |   X  |   O   |
+----------------+------+-------+
| Maintenance*   |   X  |   O   |
+----------------+------+-------+
| Information*   |   X  |   O   |
+----------------+------+-------+
| UserSettings   |   O  |   O   |
+----------------+------+-------+

