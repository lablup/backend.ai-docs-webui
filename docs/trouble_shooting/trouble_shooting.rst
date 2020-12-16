================
Trouble Shooting
================

If you use the GUI Console for a long time, you may experience connection
problems to Jupyter and/or terminal service, or compute session list not
updating. Those problems often disappear when you refresh the Console page. You
may refresh the Console by following methods.

- Web-based Console: Refresh the browser page (use the shortcut provided by
  browsers such as Ctrl-R). Since the browser's cache may cause troubles
  sometimes, it is recommended to refresh the page bypassing the cache
  (such as Shift-Ctrl-R, but the keys may differ in each browser).
- Console App: Press Ctrl-R shortcut to refresh the app.


SFTP disconnection
------------------

When Console App launches SFTP connection, it uses a local proxy server which is
embeded in the App. If you exit the Console App during the file transfer with
SFTP protocol, the transfer will immediately fail because the connection
established through the local proxy server is disconnected.  Therefore, even if
you are not using a compute session, you should not quit the Console App while
using SFTP. If you need to refresh the page, we recommend using the Ctrl-R
shortcut.

If the Console App is closed and restarted, the SFTP service is not
automatically initiated for the existing compute session. You must explicitly
start the SSH/SFTP service in the desired container to establish the SFTP
connection.



Inconsistency between the resources allocated to the session and the resources used by the session
------------------------------------------------------------

.. note::
   This feature is only available for superadmins.

Occasionally, unstable network connection or container management issues by the
docker daemon may cause mismatch between the resources allocated to the session and dispaly of the resources used by the session. If this
problem occurs, you can go to the Maintenance page and click the RECALCULATE
USAGE button to manually correct it.



Image is not displayed after it is pushed to a docker registry
--------------------------------------------------------------

.. note::
   This feature is only available for superadmins.

If a new image is pushed to one of the Backend.AI docker registries, the image
metadata must be updated in Backend.AI to be used in creating a compute session.
Metadata update can be performed by clicking the RESCAN IMAGES button on the
Maintenance page. This will update metadata for every docker registry, if
there are multiple registries.

If you want to update the metadata for a specific docker registry, you can go to
the Registries tab in Environments page.  Just click the refresh button in the
Controls column of the desired registry. Be careful not to delete the registry
by clicking the trash icon.
