=====================================================
Limiting Maximum Compute Resources per User (Keypair)
=====================================================

.. note:: Objective

   * After logging in to the administrator account, use the function to set the
     allowed resources for each user (keypair)
   * Confirm that only allowed resources can be used at maximum when creating a
     compute session by a user

In Backend.AI, you can set a limit on the total amount of resources available
for each user and group. Resource limits per group can only be set through the
enterprise-dedicated administrator GUI console, but resource limits per user
(precisely user's keypair) can be set in the user GUI console.

Log in to the user GUI Console with an administrator account to check the
resource limit status. If you log in as an administrator, you will see more
administrator-only menus at the bottom of the left menu. Among them, click Users
to go to the user management page and click the Resource Policies tab. You can
check the list of currently registered resource policies. In the figure below,
there are a total of three policies (gardener, STUDENT, default). If you look at
the Resources column of the default policy, you can see that resources such as
Cores, Ram, and fGPU are marked as infinite (∞). The infinity means that no
resource restrictions have been placed at all.

.. image:: resource_policy_page.png

Currently, the user accounts used in this guide are restricted by the default
resource policy. This can be found in the Credentials tab on the left. If you
look at the Resource Policy, you can also see that all resources can be used
indefinitely (to the extent the hardware allows).

.. image:: credentials.png

Log in again with your user account, now. Go to the Sessions page and check the
resource indicator at the top. Check the maximum quota for CPU, RAM and FGPU.
This corresponds to the total amount of resources currently held by the test
node.

.. image:: resource_indicator_no_limit.png
   :align: center

Click START to open the compute session creation dialog and pull the CPU, RAM,
and GPU sliders all the way to the right, and you can see that you cannot
allocate more than the total amount shown in the resource indicator.

.. image:: session_launch_dialog_no_limit.png
   :width: 350
   :align: center

Now log back into the administrator account and go to the Resource Policies tab.
Click the gear button in the Control column of the default policy to enter the
policy editing screen. In Update Resource Policy dialog, every option is
changeable except Policy Name which is the primary key for distinguishing the
resource policy from list. Each numeric value is regarded as maximum value for
creating/destroying a session and also for the number of vfolders. Uncheck the
Unlimited checkbox at the bottom of CPU, RAM, fGPU, and set the resource limits
to the desired values. Set the amount of constrained resource to be smaller than
the total amount of hardware. Here, we set it to 2, 4 and 1 respectively. Click
the UPDATE button to update the resource policy.

.. image:: update_resource_policy.png
   :width: 400
   :align: center

About details in each option in resource policy dialog, see the description below.

* Resource Policy
   * CPU : The fundamental resource for all kind calculation. Mostly useful at handling single and complex calculations sequentially.
   * RAM : It loads codes to execute the calculation for Machine learning. The bigger the size becomes, less overhead occurs.
   * GPU : It does similar job as the CPU does. The difference between CPU and GPU is that GPU is much faster in processing multiple but simpler calculations parallel meanwhile CPU is for more general calculations.
   * fGPU : Fractional GPU (fGPU) is literally split a single GPU to multiple partitions in order to use GPU economically. Notice that the minimum amount of fGPU required is differed by each image.

* Sessions
   * Container Per Session : The independent unit for calculating.
   * Idle timeout (sec.) : Configurable period of time during which the user can be inactive without any impact on their session.
   * Concurrent Jobs : It is about the number of jobs can be done in parallel.

* Folders
   * Allowed hosts : Allowed hosts for accessing vfolders created under this resource policy.
   * Capacity(GB) : the maximum size(GB) for folder that can be afforded.
   * Max. # : the maximum number of vfolders that can be created/invited.

In the resource policy list, check that the Resources value of the default
policy has been updated.

.. image:: update_check.png
   :width: 400
   :align: center

Once again, log in with your user account. Go to the Session page. You can see
that the resource constraint value set earlier is reflected in the resource
indicator at the top.

.. image:: resource_indicator_limit.png
   :align: center

Click START to open the calculation session creation dialog and pull the CPU,
RAM, and GPU sliders all the way to the right, and you can see that it cannot be
moved beyond the value after the resource constraint was placed.

.. image:: session_launch_dialog_limit.png
   :width: 350
   :align: center

In this way, it was confirmed that the development user can control the maximum
amount of resources that can be allocated when creating a compute session
based on the user's key pair.

.. note::
   Occasionally, the amount of resources displayed on the resource indicator may
   be out of sync due to a network connection problem or an error in the docker
   daemon. In this case, after logging in with an administrator account, go to
   the Maintenance page on the left sidebar and click the RECALCULATE USAGE
   button to synchronize the resource status again.
