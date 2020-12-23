================
Signup and Login
================

Signup
------

When you launch the GUI console, login dialog appears. If you haven't signed up
yet, press the SIGN UP button.

.. image:: login_dialog.png
   :width: 400
   :align: center
   :alt: Login dialog

Enter the required information, read and agree to the Terms of Service /
Privacy Policy, and click the SIGNUP button. Depending on your system settings,
you may need to enter an invitation token to sign up. A verification email may
be sent to verify that the email is yours. If the verification email is sent, you
will need to read the email and click the link inside to pass verification
before you can log in with your account.

.. image:: signup_dialog.PNG
   :width: 350
   :align: center
   :alt: Signup dialog

.. note::
   Depending on the server configuration and plugin settings, signing up by
   anonymous user may not be allowed. In that case, please contact administrator
   of your system.

.. note::
   To prevent malicious users from guessing user's password, password should be longer
   than 8 characters with at least one alphabet(s), number(s), and special
   character(s).
   
Login
-----

Enter your ID and password and press the LOGIN button. In API ENDPOINT, the URL
of Backend.AI Console Server, which relays the request to the Manager, should be
entered.

.. note::
   Depending on the installation and setup environment of the Console Server,
   the endpoint might be pinned and not configurable.
   
.. note::
   Backend.AI keeps the user's password securely through a one-way hash. BCrypt,
   the default password hash of BSD, is used, so even the server admins cannot
   know the user's password.

After login, you can check the information of the current resource usage in
the Summary tab.

By clicking the icon in the upper-right corner, you will see sub menus. You
can logout by selecting the Log Out menu.

.. image:: signout_button.png
   :width: 600
   :align: center
   :alt: Signout button


When you forgot your password
-----------------------------

If you have forgotten your password, you can click the CHANGE PASSWORD button on
the login panel to email a link to change password. You can change your password
by reading and following the instruction. Depending on the server settings, the
password change feature may be disabled. In this case, contact the
administrator.

.. image:: forgot_password_panel.png
   :width: 350
   :align: center
   :alt: Signout button

.. note::
   This is also a modular feature, so changing password may not be possible in
   some systems.

.. warning::
   If login failure occures more than 10 times consecutively, access
   to the endpoint is temporarily restricted for 20 minutes for security
   reasons. If the access restriction continues on more than 20 minutes, please contact
   your system administrator.
   

Sidebar Menus
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

There is a question mark icon at the lower left corner of the sidebar. Click
this icon to access the web version of this guide document.

.. image:: question_icon.png
   :width: 300
   :align: center
