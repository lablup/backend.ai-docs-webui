=========================
Querying Compute Sessions
=========================

To see the list of compute sessions, click Sessions in the left sidebar. In
the Running tab on the right, you can check the information on the currently
running sessions. Click the Finished tab to see the list of terminated
sessions. For each session, you can check information such as ID, created date,
used time, allocated resources, resource usage, and etc.

.. image:: session_list.png
   :align: center
   :alt: Session list

As a superadmin, you can see the information of all sessions currently running
(or ended) in the cluster. On the other hand, users can see their sessions only.

The resource indicator is displayed at the top of the screen. You can check the
amount of resources currently used by the user and the total amount of resources
that can be allocated. The display bar is divided into two parts: the upper and
the lower. The upper part shows the resource allocation status in the current
scaling group, and the lower part shows the allocation status of total
accessible resources.

* Upper: Allocated and available resources within the current scaling group

   - (Resources allocated by the user in the current scaling group) /
     (Total resources allocatable by the user in the current scaling group)

* Lower: Total allocated and available resources

   - (Resources allocated by the user) / (Resources allocated by the user +
     Total resources allocatable by the user in the current scaling group)

.. note::
   If the GPU resource is marked as FGPU, this means that the server is serving
   the GPU resources in a virtualized form. Backend.AI supports GPU
   virtualization technology that a single physical GPU can be divided and
   shared by multiple users for better utilization. Therefore, if you want to
   execute a task that does not require a large amount of GPU computation, you
   can create a compute session by allocating only a portion of a GPU. The
   amount of GPU resources that 1 FGPU actually allocates may vary from system
   to system depending on the administrator's setting. For example, if
   administrator has set to split one physical GPU into five pieces, 5 FGPU
   means 1 physical GPU, or 1 FGPU means 0.2 physical GPU. At this
   configuration, if you create a compute session by allocating 1 FGPU, you can
   utilize SM (streaming multiprocessor) and GPU memory corresponding to 0.2
   physical GPU for the session.
