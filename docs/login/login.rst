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
