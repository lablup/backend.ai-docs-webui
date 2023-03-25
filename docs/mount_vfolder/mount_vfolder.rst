.. _session-mounts:

=============================================
Mounting Folders to a Compute Session
=============================================

When you start a compute session, the user has access to the ``/home/work/``
directory, and the normal directories and files created under ``/home/work/``
will disappear when the compute session is terminated. This is because compute
sessions are dynamically created and deleted based on the container. To preserve
the data inside the container independent of the life cycle of the container, a
separate host folder must be mounted into the container, and then files must be
created within the mounted folder. Backend.AI provides a function to mount
storage folders when creating a compute session.

Let's go to the Sessions page and click the START button to create a new compute
session. In the Folders to mount panel in the session creation dialog, you can
see a list of storage folders that can be mount. By clicking the folder you
want to mount, you can mount it. You can also mount multiple folders
simultaneously by clicking multiple items. In this example, we will mount two
folders, ``user1-ml-test`` and ``user2-vfolder``, and then create a compute
session.

.. image:: create_session_with_folders.png
   :width: 350
   :align: center
   :alt: Launch a compute session with storage folders

.. note::
   Folders to mount only lists the data folders that the user can currently
   mount. For example, project folders used by other projects are not exposed in
   Folders to mount. The storage host for each folder is also displayed under
   the folder's name.

Now, open the terminal by clicking the terminal icon in the created session. If
you run ``ls`` command in the terminal, you can see that the ``user1-ml-test``
and ``user2-vfolder`` folders are mounted under the home directory.

.. note::
   The selected folder, by default, will be mounted with its name under
   ``/home/work/`` inside the compute session. For example, if a folder's name
   is ``test``, it is mounted on ``/home/work/test``. In case you want to
   customize the mount path, write the absolute path in the Path & Alias input
   field. If you write ``/workspace`` in the input field for the ``test`` folder,
   it will be mounted on ``/workspace`` inside the session. Writing a relative
   path will mount the folder under ``/home/work/`` with the path.

Let's create a ``test_file`` under ``user2-vfolder`` to see if the file can be
preserved after the compute session is terminated. The contents of this file
will be "file inside user2-vfolder".

.. image:: mounted_folders_in_terminal.png
   :alt: Mounted folders in terminal

If you run ``ls`` command against ``user2-vfolder``, you can see that the file
was created successfully. Also note the contents of the file with the ``cat``
command.

Now delete the compute session and go to the Storage page. Locate the
``user2-vfolder folder``, open a file explorer and check that the file
``test_file`` exists. Click the file download button in Actions to download the
file to the local machine and open it to confirm that the contents
of the file are "file inside user2-vfolder".

.. image:: download_file_from_folder.png
   :alt: Download icon in the folder explorer

Like this, when creating a compute session, you can mount storage folders and
perform any file operations on those mounted folders to save data even after the
compute session termination.


.. _using-automount-folder:

Configure a compute session environment using an automount folder
-------------------------------------------------------------------

Sometimes you need a new program or library that is not pre-installed in a
compute session. In that case, you can install packages and configure a certain
environment regardless of the type of compute session by using the Storage
folder, which persists independent of session lifecycle, and the :ref:`automount
folder<automount-folder>`.

.. _using-pip-with-automountfolder:

Install Python packages via pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creating a folder named ``.local`` allows a user to install Python user packages
in that folder. This is because ``pip`` by default installs the packages in the
``.local`` folder under the user's home folder (note that automount folder is
mounted under user's home folder). So, if you want to install and keep the
Python package ``tqdm`` regardless of the type of computing environment, you can
issue the following command in your terminal:

.. code-block:: shell

   pip install tqdm

After that, when a new compute session is created, the ``.local`` folder where
the ``tqdm`` package is installed is automatically mounted, so you can use the
``tqdm`` package without reinstalling.

.. warning::

   If you spawn multiple sessions that use different Python versions, there may
   be compatibility issues with the packages. This can be circumvented by
   branching ``PYTHONPATH`` environment variable via the ``.bashrc``. This is
   because the user's ``pip`` package is installed in the path specified in the
   ``PYTHONPATH``.

.. _using-linuxbrew-with-automountfolder:

Install packages via Homebrew
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Package managers like Ubuntu ``apt`` or CentOS ``yum`` usually require the
``root`` permission. For security reasons, ``sudo`` and ``root`` accesses are
blocked by default in Backend.AI's compute session (it may be allowed depending
on the configuration), so we recommend to use `Homebrew on Linux
<https://docs.brew.sh/Homebrew-on-Linux>`_ which does not require ``sudo``.

Homebrew can be configured as follows:

- Create ``.linuxbrew`` folder in Data & Storage page.
- Create a compute session (``.linuxbrew`` folder is automatically mounted).
- Install Homebrew in the compute session.

   .. code-block:: shell

      $ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      $ export PATH=/home/linuxbrew/.linuxbrew/bin:$PATH

- Homebrew packages can be installed like:

   .. code-block:: shell

      $ brew install hello
      $ hello

``brew`` installs packages under ``/home/linuxbrew/.linuxbrew`` which is
automatically symlinked to ``/home/work/.linuxbrew``. So, if you create a data
folder named ``.linuxbrew``, which will be automatically mounted when creating a
compute session, those installed packages can be kept after the compute session
is destroyed and then reused for the next compute session.
