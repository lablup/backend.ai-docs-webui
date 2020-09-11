================================================
CPU/Memory Allocation and Using Compute Sessions
================================================

.. note:: Objectives

   * From the GUI environment, users can create a compute session by specifying
     the amount of CPU and memory resources dynamically
   * From the GUI, check the amount of CPU and memory resources of the session
   * Using Jupyter Notebook and Terminal apps in container environment
   * Check the allocated CPU and memory resources from inside the container by
     referencing cgroup

The most visited pages in the Backend.AI GUI Console would be the Sessions and
Storage pages. On the Sessions page, you can view, create, and use
container-based compute sessions, and on the Storage page, you can create a
storage folder to keep important data. Here, you will learn how to create
container-based compute sessions and utilize various web applications on
the Sessions page.


Start a new session
-------------------

After logging in with a user account, click Sessions on the left menu to visit
the Sessions page.

.. image:: sessions_page.png

Click the START button to start a new compute session. The following setup
dialog will appear. You can specify the language environment (Environments,
Version) and resources you want to allocate. Set the CPU and memory as shown in
the following figure and click the LAUNCH button. The environment was chosen as
TensorFlow 2.2.

.. image:: session_launch_dialog.png
   :width: 350
   :align: center

If no mount folder is specified in the Folder to mount input box, a warning
dialog may appear indicating that the storage folder is not mounted. For now,
ignore the warning and click the LAUNCH WITHOUT STORAGE FOLDER button to create
a compute session. Let's see that a new compute session is created in the
Running tab.

.. image:: session_created.png

You can check information such as ID, start date, usage time, resource setting,
and resource usage for each session. In particular, check the allocated
resources in the Configuration column. Note that the amounts of resources you
specified in creating the compute session are displayed.

.. note::
   Superadmins can view all compute session information currently running (or
   terminated) in the cluster, and users can view only the sessions they have
   created.


Utilize Jupyter Notebook and check the resource quota from inside the container
-------------------------------------------------------------------------------

Let's look at how to use and manage compute sessions that are already running.
If you look at the Control column of the session list, there are several icons.
When you click the first icon, the app launcher appears as shown in the figure
below, and several app services supported by the session appear.

.. image:: app_launch_dialog.png
   :width: 400
   :align: center

Let's click on Jupyter Notebook.

.. image:: jupyter_app.png

A new window pops up and you can see that Jupyter Notebook is running. This
notebook was created inside a running compute session and can be used easily
with the click of a button without any other settings. Also, there is no need
for a separate package installation process because the language environment and
library provided by the computation session can be used as it is. For detailed
instructions on how to use Jupyter Notebook, please refer to the official
documentation.

Click the NEW button on the top right and select the Notebook for Backend.AI,
then the ipynb window appears where you can enter your own code.

.. image:: backendai_notebook_menu.png
   :width: 400
   :align: center

In this window, you can enter and execute any code you want by using the
environment that session provides. The code execution happens on one of the
Backend.AI nodes where the compute session is actually created, and there is no
need to configure a separate environment on the local machine. Enter the
following code and click the Run button or type ``Ctrl-Enter`` to run the code.
It is a Python code that reads and prints the resource quota under
``/sys/fs/cgroup/``.

.. image:: notebook_code_execution.png

Since Python is already installed in the TensorFlow 2.2 environment, the code
will run without any configuration. Make sure that the amount of core and memory
you specified when you first created the compute session is displayed.

.. note::
   The amount of memory may vary slightly depending on the calculation method.

Like this, after creating a compute session, you can use web apps such as
Jupyter Notebook, and in Jupyter Notebook, you can run Python code that checks
resource constraints right away without installing a separate packages.


Web terminal
------------

If you close the Jupyter Notebook app and open the app launcher screen of the
math session again, you will see the Console app present. Let's click.

.. image:: session_terminal.png
   :width: 500
   :align: center

A terminal will also appear in a new window, and you can issue shell commands by
accessing inside the computational session as shown in the following figure. If
you are familiar with using commands, you can easily issue various Linux
commands. You can see that the Untitled.ipynb file automatically generated in
Jupyter Notebook is viewed through the ``ls`` command. This is proof that both
apps are running in the same container environment.

In addition to this, you can use web-based services such as TensorBoard, Jupyter
Lab, etc., depending on the type of service provided by the compute session.

To delete a specific session, simply click on the red power icon.

.. image:: session_destroy_dialog.png
   :width: 400
   :align: center
