===============
Handing Folders
===============

Backend.AI supports dedicated storage to preserve user's files. Since the files
and directories of a compute session are deleted upon session termination, it is
recommended to save them in a storage folder. List of storage folders can be
found by selecting the Storage on the left sidebar.

.. image:: vfolder_list.png
   :alt: Folder list in Storage page

There are two types of storage folders. User type folders can be created by
normal users, and you can check that ther is one user icon in the Type column.
On the other hand, Group folders can be recognized by an icon with multiple
users in the column. Group folders are created by domain admins, and normal
users can only see group folders which are created in a group where user
belongs.


Create storage folder
---------------------

You can create a storage folder with the desired name by clicking the NEW FOLDER
button. Enter the name of the folder to be created in Folder name, and select
one of User / Group for Type. (Depending on the server settings, only one of
User or Group may be selectable.) When creating a group folder, the Group field
must be set. The group folder will be bind to the group specified in the Group
field, and only users belonging to the group can mount and use the group folder.
After setting the values as desired, you can create a folder by clicking the
CREATE button.

.. image:: vfolder_create_dialog.png
   :width: 400
   :align: center
   :alt: Folder creation dialog


Explore folder
--------------

You can click the folder icon in the Control column to bring up a file explorer
where you can view the contents of that folder.

.. image:: vfolder_item_with_controls.png
   :alt: Controls in folder item

You can see that directories and files inside the folder will be listed, if
exists. Click a directory name in the Name column to move to the directory.  You
can click the download button or delete button in the Actions column to download
it or delete it entirely from the directory. You can rename a file/directory as
well. For more detailed file operations, you can mount this folder when creating
a compute session, and then use a service like Terminal or Jupyter Notebook to
do it.

.. image:: vfolder_explorer.png
   :alt: File explorer of a storage folder

You can create a new directory on the current path with the NEW FOLDER button
(in the file explorer), or upload a local file with the UPLOAD FILES button. All
of these file operations can also be performed using the above-described method
of mounting folders into a compute session.

To close file explorer, click the X button in the upper right.


Rename folder
-------------

If you have permission to rename the storage folder, you can rename it by
clicking the edit icon in the Control column. When you click the icon button, a
rename dialog will appears. Write new folder name and then click RENAME button.


Delete folder
-------------

If you have permission to delete the storage folder, you can delete it by
clicking the trash can icon in the Control column. When you click the Delete
button, a confirm dialog appears. To prevent accidental deletion, you have to
enter the name of the folder to be deleted, explicitly.

.. image:: vfolder_delete_dialog.png
   :width: 400
   :align: center
   :alt: Folder deletion dialog

The folders created here can be mounted when creating a compute session. Folders
are mounted under the user's default working directory, ``/home/work/``, and the
files stored in this directory will not be deleted when the compute session
is terminated. (However, if you delete the folder itself, it will be gone).


Automount folder
----------------

Storage & Folders page has an Automount Folders tab. Click this tab to see a
list of folders whose names prefixed with a dot (.). When you create a folder,
if you specify a name that starts with a dot (.), it is added to the Automount
Folders tab, not the Folders tab. Automount Folders are special folders that are
automatically mounted in your home directory even if you do not mount them
manually when creating a compute session. By using this feature, creating and
using Storage folders such as ``.local``, ``.linuxbrew``, ``.pyenv``, and etc.,
you can configure a certain user packages or environments that do not change
with different kinds of compute session.

For more detailed information on the usage of Automount folders, refer to
:ref:`Create a Compute Session with Mounted Folders<session-with-mounts>`
section.

.. image:: vfolder_automount_folders.png
   :alt: Automount folders
