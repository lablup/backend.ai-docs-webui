=============
Model Serving
=============

Model Service
-------------

Backend.AI not only facilitates the construction of development environments 
and resource management during the model training phase, but also supports 
the model service feature from version 23.09 onwards. This feature allows 
end-users (such as AI-based mobile apps and web service backends) to make 
inference API calls when they want to deploy the completed model as an 
inference service.

The Model Service extends the functionality of the existing training
compute sessions, enabling automated maintenance, scaling, and permanent
port and endpoint address mapping for production services. Developers or
administrators only need to specify the scaling parameters required for
the Model Service, without the need to manually create or delete compute
sessions.

Configuring and limitations of model service in version 23.03 and earlier
-------------------------------------------------------------------------

Although the model serving-specific feature is officially supported from 
version 23.09, you can still use model service in earlier versions.

For example, in version 23.03, you can configure a model service by
modifying the compute session for training in the following way:

1. Add pre-opened ports during session creation to map the running
   server port inside the session for model serving. (For instructions
   on how to use preopen ports, refer to
   this :ref:`Set Preopen Ports <set-preopen-ports>`.)
2. Check “Open app to public” to allow the service mapped to the
   pre-opened port to be publicly accessible. (For detailed information
   about “Open app to public,” refer to
   this :ref:`Open app to public <open-app-to-public>`.)

However, there are certain limitations in version 23.03:

-  Sessions do not automatically recover if they are terminated due to
   external factors such as idle timeout or system errors.
-  The app port changes every time a session is restarted.
-  If sessions are repeatedly restarted, the idle ports may be
   exhausted.

The official Model Service feature in version 23.09 resolves these
limitations. Therefore, starting from version 23.09, it is recommended
to create/manage Model Services through the model serving menu whenever
possible. The use of pre-opened ports is recommended only for
development and testing purposes.

Guide to Steps for Using Model Service
--------------------------------------

To use the Model Service, you need to follow the steps below:

1. Create a model definition file.
2. Upload the model definition file to the model type folder.
3. Create/modify the Model Service.
4. (If the Model Service is not public) Obtain a token.
5. (For end users) Access the endpoint corresponding to the Model
   Service to verify the service.

Creating a Model Definition File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   Note: The model definition file must be named model-definition.yml or
   model-definition.yaml to align with the current version.

The model definition file contains the configuration information
required by the `Backend.AI <http://backend.ai/>`__ system to
automatically start, initialize, and scale the inference session. It is
stored in the model type folder independently from the container image
that contains the inference service engine. This allows the engine to
serve different models based on specific requirements and eliminates the
need to build and deploy a new container image every time the model
changes. By loading the model definition and model data from the network
storage, the deployment process can be simplified and optimized during
automatic scaling.

The model definition file follows the following format:

.. code:: yaml

   models:
     - name: "simple-http-server"
       model_path: "/models"
       service:
         pre_start_actions:
         start_command: ["python3", "-m", "http.server", "8080"]
         port: 8080
         health_check:
           path: /
           max_retries: 10

Key-Value Descriptions for Model Definition File

   Note: Values marked as required in the notes must be included in the
   model definition file. Other items are optional and can be
   omitted.Items with a / slash indicate descriptions for subkeys under
   the key preceding the slash.

+--------------------------------------+-----------------------+-------------------+
| **Key**                              | **Description**       | **Note**          |
+======================================+=======================+===================+
| ``name``                             | | Defines the name    | Required          |
|                                      | | of the model.       |                   |
+--------------------------------------+-----------------------+-------------------+
| ``model_path``                       | | Addresses the path  | - Required        |
|                                      | | of where model is   | - Starts from     |
|                                      | | defined.            |   ``/models``     |
+--------------------------------------+-----------------------+-------------------+
| ``service``                          | | Item for organizing | ``-``             |
|                                      | | information about   |                   |
|                                      | | the files to be     |                   |
|                                      | | served (includes    |                   |
|                                      | | command scripts and |                   |
|                                      | | code)               |                   |
+--------------------------------------+-----------------------+-------------------+
| ``service/pre_start_actions``        | | Item for organizing | ``-``             |
|                                      | | preceding commands  |                   |
|                                      | | or actions to be    |                   |
|                                      | | executed before the |                   |
|                                      | | ``start_command``   |                   |
+--------------------------------------+-----------------------+-------------------+
| ``service/pre_start_actions/action`` | | Please refer to the | | Useful actions  |
|                                      | | description for     | | may be added in |
|                                      | | service action      | | the future      | 
+--------------------------------------+-----------------------+-------------------+
| ``service/pre_start_actions/args/*`` | | Please refer to     | ``-``             |
|                                      | | description for     |                   |
|                                      | | service action      |                   |
+--------------------------------------+-----------------------+-------------------+
| ``service/start_command``            | | Specify the command | Required          |
|                                      | | to be executed as   |                   | 
|                                      | | an array of strings |                   |
|                                      | | in model serving.   |                   |
+--------------------------------------+-----------------------+-------------------+
| ``service/port``                     | | Specify the ports to| Required          |
|                                      | | be opened in        |                   |
|                                      | | accordance with the |                   |
|                                      | | commands executed   |                   |
|                                      | | during model serving|                   |
|                                      | | at the container.   |                   |
+--------------------------------------+-----------------------+-------------------+
| ``health_check/path``                | | Specify the path for| | This is the path|
|                                      | | verifying that      | | that follows the|
|                                      | | the service is      | | endpoint        |
|                                      | | running properly    |                   |
|                                      | | in model serving.   |                   |
+--------------------------------------+-----------------------+-------------------+
| ``health_check/max_retries``         | | Specify the number  | ``-``             |
|                                      | | of retries to be    |                   |
|                                      | | made if there is no |                   |
|                                      | | response after a    |                   |
|                                      | | request is sent to  |                   |
|                                      | | the service during  |                   |
|                                      | | model serving.      |                   |
+--------------------------------------+-----------------------+-------------------+


Description for service action supported in Backend.AI Model serving
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------+---------------------------------------------+-----------------------+
| **Action name**    | **Supported key name / description**        | **Notes**             |
+====================+=============================================+=======================+
| ``write_file``     | | - arg/filename: Specify the file name     | | This is an action   |
|                    | | - body: Specify the content to be         | | to create a file    |
|                    | |         added to the file.                | | with the given      |
|                    | | - mode: Specify the file's access         | | file name and       |
|                    | |         permissions.                      | | append control to it|
|                    | | - append: Set whether to overwrite or     | | the default access  |
|                    | |           append content to the file      | | permission is       |
|                    | |           as ``True`` or ``False``.       | | ``644``.            |
+--------------------+---------------------------------------------+-----------------------+
| ``write_tempfile`` | | - body: Specify the content to be         | | This is an action to|
|                    | |         added to the file.                | | create a file with  |
|                    | | - mode: Specify the file's access         | | a temporary file    |
|                    | |         permissions.                      | | name (``.py``) and  |
|                    | |                                           | | append content to   |
|                    | |                                           | | it. If no value is  |
|                    | |                                           | | specified for the   |
|                    | |                                           | | mode, the default   |
|                    | |                                           | | access permission is|
|                    | |                                           | | ``644``.            |
+--------------------+---------------------------------------------+-----------------------+
| ``run_command``    | | args/command: Specify the command to      | | The result of       |
|                    | | executed as an array.                     | | executing a command,|
|                    | | e.g. python3 -m http.server, 8080 ->      | | including any errors|
|                    | | [["python3", "-m", "http.server", "8080"]]| | , will be returned  |
|                    | |                                           | | in following format:|
|                    | |                                           | | - out: Output of the|
|                    | |                                           | | command execution   |
|                    | |                                           | | - err: Error msg if |
|                    | |                                           | | an error occurs     |
|                    | |                                           | | during command      |
|                    | |                                           | | execution           |
+--------------------+---------------------------------------------+-----------------------+
| ``mkdir``          | | args/path: Specify the path to create a   | ``-``                 |
|                    | | directory                                 |                       |
+--------------------+---------------------------------------------+-----------------------+
| ``log``            | | - args/message: Specify the message to be | ``-``                 |
|                    | |                 displayed in the logs.    |                       |
|                    | | - debug: Set to ``True`` if it is in      |                       |
|                    | |          debug mode, otherwise, set to    |                       |
|                    | |          ``False``.                       |                       |
+--------------------+---------------------------------------------+-----------------------+



Uploading Model Definition File to Model Type Folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To upload the model definition file (``model-definition.yml``) to the
model type folder, you need to create a virtual folder. When creating
the virtual folder, select the ``model`` type instead of the default
``regular`` type. Refer to the section on creating a storage folder in
the Data & Folders page for instructions on how to create a folder.
After creating the folder, select the “Model” tab in the Data & Folders
page, click on the recently created model type folder icon to open the
folder explorer, and upload the model definition file.

Creating/Modifying Model Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the model definition file is uploaded to the virtual folder of the
model type, you are ready to create the model service.

Click the “Start Service” button on the Model Serving page. This will
bring up a modal where you can enter the required settings for creating
the service.

First, provide a service name and select a resource group. Then, select
the virtual folder of the model type to be used for the model service.

For detailed explanations of each item, please refer to the following:

-  Open To Public: This option allows access to the model service
   without any separate token on the server where the service is to be
   hosted. By default, it is disabled.
-  Desired Routing Count: The model service can be serviced by multiple
   servers. This setting determines how many routing sessions to create
   for the current service. The value specified here will be used as the
   basis for creating the sessions.
-  Environment / Version: You can configure the execution environment
   for the dedicated server of the model service. Currently, even if the
   service has multiple routings, it will be executed in a single
   environment only. (Support for multiple execution environments will
   be added in a future update)
-  CPU: The number of CPU cores allocated to the routing for running the
   model service.
-  RAM: The amount of memory allocated to the routing for running the
   model service (in GiB).
-  GPU: The GPU allocation for the routing for running the model
   service.
-  Shared Memory: The amount of shared memory allocated to the routing
   for running the model service (in GiB). It should be smaller than the
   allocated memory.

Modifying Model Service
~~~~~~~~~~~~~~~~~~~~~~~

In the current version, only changing the desired session count of the
model service is supported, rather than modifying all the configuration
values of the service. Click on the wrench icon in the Control tab to
open a modal where you can change the desired session count. After
modifying the value, click the confirm button. The routing count will be
adjusted accordingly.

Terminating Model Service
~~~~~~~~~~~~~~~~~~~~~~~~~

The model service periodically runs a scheduler to adjust the routing
count to match the desired session count. However, this puts a burden on
the Backend.AI scheduler. Therefore, it is recommended to terminate the 
model service if it is no longer needed. To terminate the model service, 
click on the trash icon in the Control tab. A modal will appear asking 
for confirmation to terminate the model service. Clicking “confirm” 
will terminate the model service. The terminated model service will be 
removed from the list of model services.

Handling Failed Model Service Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the status of the model service remains ``UNHEALTHY``, it indicates
that the model service cannot be executed properly.

The common reasons for creation failure and their solutions are as
follows:

-  Insufficient allocated resources for the routing when creating the
   model service

   -  Solution: Terminate the problematic service and recreate it with
      an allocation of more sufficient resources than the previous
      settings.

-  Incorrect format of the model definition file (``model-definition.yml``)

   -  Solution: Verify the format of the model definition file (link)
      and if any key-value pairs are incorrect, modify them and
      overwrite the file in the saved location. Then, click the refresh
      button to ensure that the routing of the model service is set
      correctly.

Generating Tokens
~~~~~~~~~~~~~~~~~

Once the model service is successfully executed, the status will be set
to HEALTHY. In this case, you can click on the corresponding endpoint
name in the Model Service tab to view detailed information about the
model service. From there, you can check the service endpoint in the
routing information of the model service. If the “Open to Public” option
is enabled when the service is created, the endpoint will be publicly
accessible without any separate token, and end users can access it.
However, if it is disabled, you can issue a token as described below to
verify that the service is running properly.

Click the token creation button located to the right of the generated
token list in the routing information. In the modal that appears for
token creation, enter the expiration date. The issued token will be
added to the list of generated tokens. Click the copy icon in the token
item to copy the token, and add it as the value of the following key.

============= ================
Key           Value
============= ================
Content-Type  application/json
Authorization BackendAI
============= ================

Accessing the Model Service Endpoint for End Users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To complete the model serving, you need to share information with the
actual end users so that they can access the server where the model
service is running. If the Open to Public option is enabled when the
service is created, you can share the service endpoint value from the
routing information page. If the service was created with the option
disabled, you can share the service endpoint value along with the token
previously generated.

.. warning:: 
   By default, end users must be on a network that can access the
   endpoint. If the service was created in a closed network, only end
   users who have access within that closed network can access the
   service.
