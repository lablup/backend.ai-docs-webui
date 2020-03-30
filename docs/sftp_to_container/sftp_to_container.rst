==========================================
Connect to Container with SFTP (FileZilla)
==========================================

Backend.AI supports SSH/SFTP connection to the created container. In this
section, we will look at how to access container through SFTP with a FileZilla
client.

.. note::
   SSH/SFTP connection is supported only on desktop app, and not yet supported
   on web-based console service.

Backend.AI Console app supports OpenSSH-based public key connection (RSA2048).
To access with a client such as PuTTY on Windows, a private key must be
converted into a ppk file through a program such as PuTTYgen. You can refer to
the following link for the conversion method:
https://wiki.filezilla-project.org/Howto.

If you want to use your own public key, you can create a user-type storage
folder named ``.ssh`` and store the public key in that folder to use that public
key for authentication. In this example, we will use an automatically generated
key.

First, create a compute session, then click the app icon (first button) in
Control, followed by SSH/SFTP icon. Then, a daemon that allows SSH/SFTP access
inside the container will be initiated, and the Console app interacts with the
daemon through a local wsproxy service.

.. warning::
   You cannot establish a SSH/SFTP connection to the container until you click
   this SSH/SFTP icon. When you close the Console app and launch it again, the
   connection between the local proxy and the Console app is initialized, so the
   SSH/SFTP icon must be clicked again.

Next, a dialog containing SSH/SFTP connection information will be pop up.
Remember the address written in the SFTP URL and click the download link to save
the ``id_container`` file on the local machine. This file is an auto-generated
SSH private key. Instead of using a link, you can also download the
auto-generated ``id_container`` file under ``/home/work/`` with your terminal or
Jupyter Notebook. The auto-generated SSH key does not change unless renewed.

.. note::
   The current connection port number is 10000, 10001, 10002, ... in the order
   of clicking the SSH/SFTP icon after starting the Console app. Therefore, the
   session where the first SSH/SFTP app is clicked will occupy port 10000, and
   the session where the second SSH/SFTP app is clicked will take port 10001.
   When the Console app is restarted, the port mapping is initialized, so the
   session where the SSH/SFTP app is clicked for the first time after the
   Console app restart will take over from port 10000 again. In the future, we
   will add the ability for user to specify the port number of SSH/SFTP
   connection.

.. image:: sftp_app.png
   :alt: Starting SSH/SFTP daemon inside a compute session (container)

``id_container`` is an OpenSSH-based key, so if you use a client that supports
only Windows or ppk type keys, you must convert it. Here, we will convert
through the PuTTYgen program installed with PuTTY. After running the PuTTYgen,
click on the import key in the Conversions menu. Select the downloaded
``id_container`` file from the file open dialog. Click the Save private key
button of PuTTYGen and save the file with the name ``id_container.ppk``.

.. image:: puttygen_conversion.png
   :alt: SSH key conversion with PuttyGen

After launching the FileZilla client, go to the Settings-Connection-SFTP
and register the key file ``id_container.ppk`` (``id_container`` for clients
supporting OpenSSH).

.. image:: filezilla_setting.png
   :alt: Filezilla settings to connect to compute session

Open Site Manager, create a new site, and enter the connection information as
follows.

.. image:: filezilla_site_setting.png
   :alt: Filezilla site setting

When connecting to a container for the first time, the following confirmation
popup may appear. Click the OK button to save the host key.

.. image:: unknown_host_key.png
   :width: 500
   :align: center
   :alt: Unknown Host Key dialog

After a while, you can see that the connection is established as follows. You
can now transfer large files to ``/home/work/`` or other mounted storage folder
with this SFTP connection.

.. image:: filezilla_connection_established.png
   :alt: Filezilla connection established
