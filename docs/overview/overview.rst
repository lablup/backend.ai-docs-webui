========
Overview
========

Backend.AI is an open source cloud resource management platform. Backend.AI
efficiently manages compute resources in a cloud or on-premises cluster,
providing a virtualized compute environment to provide on-demand computation,
anytime, anywhere. With GPU virtualization technique, Backend.AI helps
scientists, DevOps, enterprise, and AI enthusiasts to scale up efficiently.

Backend.AI offers a variety of performance-driven optimizations for machine
learning and high-performance computing clusters, along with management and
research features to support a diverse users, including researchers,
administrators, and DevOps. The Enterprise Edition adds support for multi-domain
management, a dedicated Hub app for superadmins, and the GPU virtualization
plug-in.

A GUI client package is also provided to easily take advantage of the features
supported by the Backend.AI server. Backend.AI Console is a GUI client in the
form of a web service or standlone app. It provides a convenient graphical
interface for accessing the Backend.AI server to utilize computing resources and
manage its environment. Most tasks can be done with mouse clicks and brief
typing, which achieves more intuitive use.


Key Concepts
------------

.. image:: key_concepts.png
   :alt: Diagram explaining key concepts

- User: The user is the person who connects to Backend.AI and performs work.
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
  policies. A user should belong to only one domain, and can create sessions or
  do some other jobs only in their own domain. A domain can have one or
  more domain admins, who can set policies within the domain or manage
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
  cluster admin, create your own image with the software you want to
  use, and ask the admin to register it.
- Virtual Folder (vfolder): A "cloud" folder that is always accessible and
  mountable in a container on a per-user basis, regardless of which node the
  container runs on. After creating your own virtual folder, you can upload your
  own program code, data, etc. in advance, and mount it when you run the
  compute session to read from and write to it as if it is on your local disk.
- Application service, service port: A feature that allows you to access various
  user applications (eg DIGITS, Jupyter Notebook, shell terminal, TensorBoard,
  etc.) running within the compute session. You do not need to know the
  container's address and port number directly, but you can use the provided CLI
  client or GUI console to directly access the desired daemon of the session.
- Console App: A GUI client that is served as a web or standalond app.
  You can use the service after logging in by specifying the address of the
  Backend.AI server and entering the user account information.
- Local wsproxy: Proxy server built into the console app. Services such as
  Jupyter Notebook and Terminal that can be used in the console app communicate
  with the server through websocket, which converts general HTTP requests to and
  from the console app into websocket to deliver messages.

  - If the console app loses its connection to wsproxy or the wsproxy server is
    dead, it will not be possible to access services such as Jupyter Notebook
    and Terminal.

- Web wsproxy: In the case of the console app provided as a web, the built-in
  server cannot be operated due to the nature of the browser. In this case, you
  can use services such as Jupyter Notebook, Terminal, etc. in the web
  environment by making the wsproxy server as a separate web server
  so that the console app can see the web wsproxy.
