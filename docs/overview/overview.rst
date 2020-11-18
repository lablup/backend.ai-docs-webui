========
Overview
========

Backend.AI Enterprise R2 is a platform that makes it easy to utilize virtualized
compute resource clusters in a cloud or on-premises environment. Provides a
convenient web-based GUI interface to access the Backend.AI server to utilize
compute resources and manage user's own compute environment, and provides
pre-made images which enables immediate creation of compute sessions without the
need by users to install separate programs. In addition, the container-based GPU
virtualization technology of Backend.AI supports the efficient use of GPUs by
flexibly dividing one physical GPU, so that multiple users can use it at the
same time. Most of this works can be done with some mouse clicks and short
typings, making it more intuitive to use.

Key Concepts
------------

.. image:: key_concepts.png
   :alt: Diagram explaining key concepts

- User: The user is the person who connects to Backend.AI and performs work.
  Users are divided into normal users and superadmins according to their
  privileges. While ordinary users can only perform tasks related to their
  computing sessions, superadmins perform almost all tasks throughout the
  system. A user belongs to one domain and can belong to multiple groups within
  a domain.
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
  user applications (eg Jupyter Notebook, shell terminal, TensorBoard,
  etc.) running within the compute session. You do not need to know the
  container's address and port number directly, but you can use the provided CLI
  client or GUI console to directly access the desired daemon of the session.
- (GUI) Console: A GUI client that is served by web. You can use the service
  after logging in by specifying the address of the Backend.AI server and
  entering the user account information.
- WSProxy: Proxy server which serves interactive apps, such as Jupyter Notebook
  and Terminal, that can be used in the GUI Console to communicate with the
  Backend.AI server through websocket, which converts general HTTP requests to
  and from the Console into websocket to deliver messages.

  - If the GUI Gonsole loses its connection to wsproxy or the wsproxy server is
    dead, it will not be possible to access services such as Jupyter Notebook
    and Terminal.
