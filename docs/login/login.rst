=====
Login
=====

Enter your ID and password and press the LOGIN button. In API ENDPOINT, the URL
of Backend.AI Console Server, which relays the request to the Manager, should be
entered.

.. image:: login_dialog.png
   :width: 400
   :align: center
   :alt: Login dialog

.. note::
   Depending on the installation and setup environment of the Console Server,
   the endpoint might be pinned and not configurable.

.. note::
   Backend.AI keeps the user's password securely through a one-way hash. BCrypt,
   the default password hash of BSD, is used, so even the server admins cannot
   know the user's password.

.. note::
   To keep malicious user from guessing user's password, password should longer
   than 8 characters with at least one alphabet(s), number(s), and special
   character(s).

After login, you can check the information of the current resource usage in
the Summary tab.

Buy clicking the icon in the upper-right corner, you will see sub menus. You
can logout by selecting the Log Out menu.

.. image:: signout_button.png
   :alt: Signout button

.. note::
   Depending on the server/client setting, user can sign up by themselves
   through email verification, which requires connection to AWS with paid
   account. For most on-premise installation, this feature is disabled by
   default.

.. warning::
   If there are more than 5 times of login failure occured, access to the
   endpoint is temporarily restricted for 3 minutes for security reasons.
   If the access restriction persists, , please contact your system
   administrator.

.. note::
   After initial login, the browser session information will be keep for 30 days
   from the console-server. That means, after 30 days of initial login, the user
   needs to login again since server-side authentication information will be
   expired. It would be controversal when the server expires the session cookie.
   If its too short, customers are not happy, and if its too long, user's
   account will be more vulnerable. Since many web-based applications, such as
   Microsoft Teams, will expire session information after 30 days, we also
   determined the period as 30 days.

   If you want to change this setting, please follow the steps below.

   * SSH connection to the host where Console-Server is installed.
   * Move to the location where Console-Server configuration file exist. Usually
     it is located at ``/home/lablup/.config/backend.ai/console-server.conf``,
     but this may change depending on the system configuration.
   * Open the ``console-server.conf`` file with a text editor and set the value
     of ``max_age`` in the ``[session]`` section to the desired value. For
     example, if you only want to keep the login session for one day, enter
     ``86400`` (unit: seconds).
   * Restart Console-Server: ``sudo systemctl restart backendai-console-server``


Menus in the sidebar
--------------------

There are three buttons at the top of the left sidebar.

The leftmost button changes the size of the sidebar. Click to make the sidebar
narrower. Click again to bring the sidebar back to its original width.

.. image:: ui_menu.png

The middle button is the event notification button. Events that need to be
recorded during Console operation are displayed here.

The rightmost button is the background task button. When background tasks are
running, such as creating a compute session, you can check the jobs here.  When
the background task is finished, it usually disappears as well.

There is a question mark icon in the lower left corner of the sidebar. Click
this icon to access the web version of this guide document.

.. image:: question_icon.png
   :width: 300
   :align: center
