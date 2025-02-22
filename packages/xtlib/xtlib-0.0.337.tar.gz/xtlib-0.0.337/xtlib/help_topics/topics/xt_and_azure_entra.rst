.. _xt_and_azure_entra:

========================================
Using Azure Entra Authentication with XT
========================================

As of build 0.0.329, XT supports running with Azure Entra authentication under Azure Batch.

Support for Singularity in under development.

======================================================
Suggested Steps for Getting Started with Azure Entra
======================================================

1. Create an Entra group for your team (in Azure Portal).  All members of the group should be added using their SC ALT identities.

2. Create a User-Assigned Managed Identity for your team (in Azure Portal).  This identity will be used to authenticate your 
jobs as they run on Azure compute nodes (Azure Batch and Singularity).

3. In Azure Portal, for each of your team's resource groups, assign your team's group and user-assigned managed identity to the
"Contributor" role (under privileged administator roles).  This will give you the necessary permissions to use your Azure resources
with Entra authentication.

4. Remove any existing corporate identities for you and your team from all of your resources, resource groups, and your Azure subscription.

5. Add your team's SC ALT identities to your SQL database (see next section).

========================================================
Adding your team members to your SQL database (required)
========================================================

Adding users to SQL::
The following information has been taken from this original document:  https://eng.ms/docs/products/onecert-certificates-key-vault-and-dsms/key-vault-dsms/certandsecretmngmt/tsg/cfazuresql#create-sql-user-for-managed-identity-or-application

IMPORTANT: The following queries must be in the scope of the XT_DB (not the System Databases).

1. Add your group team as an authorized SQL user:

In Query windows (of Azure portal or SQL Server Management Studio), enter and RUN the following commands, substituting the uppercase names and id's as appropriate:

.. code-block:: sql

    -- Replace the two variables with the MS Entra group display name and object ID
    declare @groupName sysname = 'YOUR_TEAM_NAME'; 
    declare @objectId uniqueidentifier = 'YOUR_TEAM_OBJECT_ID';

    -- convert the guid to the right type and create the SQL user
    declare @castObjectId nvarchar(max) = CONVERT(varchar(max), convert (varbinary(16), @objectId), 1);

    -- Construct command: CREATE USER [@groupName] WITH SID = @castObjectId, TYPE = X;
    declare @cmd nvarchar(max) = N'CREATE USER [' + @groupName + '] WITH SID = ' + @castObjectId + ', TYPE = X;'
    EXEC (@cmd)

2. add managed identity as a user:

In Query windows (of Azure portal or SQL Server Management Studio), enter and RUN the following commands, substituting the uppercase names and id's as appropriate:

.. code-block:: sql

    -- Replace the two variables with the managed identity display name and client ID
    declare @MSIname sysname = 'YOUR_USER_ASSIGNED_MANAGED_IDENTITY_NAME'
    declare @clientId uniqueidentifier = 'YOUR_USER_ASSIGNED_MANAGED_IDENTITY_CLIENT_ID';

    -- convert the guid to the right type and create the SQL user
    declare @castClientId nvarchar(max) = CONVERT(varchar(max), convert (varbinary(16), @clientId), 1);

    -- Construct command: CREATE USER [@MSIname] WITH SID = @castClientId, TYPE = E;
    declare @cmd nvarchar(max) = N'CREATE USER [' + @MSIname + '] WITH SID = ' + @castClientId + ', TYPE = E;'
    EXEC (@cmd)

3. grant permissions:

In Query windows (of Azure portal or SQL Server Management Studio), enter and RUN the following commands, substituting the uppercase names as appropriate:

.. code-block:: sql

    EXEC sp_addrolemember 'db_datareader', 'YOUR_TEAM_NAME';			
    EXEC sp_addrolemember 'db_datawriter', 'YOUR_TEAM_NAME';
    EXEC sp_addrolemember 'db_ddladmin', 'YOUR_TEAM_NAME';

    EXEC sp_addrolemember 'db_datareader', 'YOUR_USER_ASSIGNED_MANAGED_IDENTITY_NAME';			
    EXEC sp_addrolemember 'db_datawriter', 'YOUR_USER_ASSIGNED_MANAGED_IDENTITY_NAME';
    EXEC sp_addrolemember 'db_ddladmin', 'YOUR_USER_ASSIGNED_MANAGED_IDENTITY_NAME';


======================================================
XT config file changes for Azure Entra authentication
======================================================

1. In the external-services section of your XT configuration file, add "azure-login: true" to each of the following service types:

    - batch, singularity, storage, odbc, registry

This attribute tells XT that to access that resource, it needs to authenticate with Azure Entra.

2. In the external-services section of your XT configuration file, remove the "key" name/value pair for each of the following service types:

    - batch, singularity, storage, odbc, registry

Since these are now using Azure Entra authentication, the key is not needed.

3. In the setups section, add the following package to all BATCH setups (in the pip-packages list):
    
        - "pynvml"

4. In the setups section, add the following packages to all SINGULARITY setups (in the pip-packages list):
    
        - "pynvml", "azure-ai-ml"


=====================================================
Batch-specific changes for Entra authentication
=====================================================


1. In external-services section of your XT configuration file, each batch service entry must now contain the following attributes:

    - type, url, azure-login, user-identity-id, subscription-id, resource-group

 Example:
.. code-block:: xml

        xtsandboxbatch: {type: "batch", url: "https://xtsandboxbatch.eastus.batch.azure.com", azure-login: true,
        user-identity-id: "/subscriptions/41c6e824-0f66-4076-81dd-f751c70a140b/resourcegroups/xt-sandbox/providers/Microsoft.ManagedIdentity/userAssignedIdentities/xt_user_identity",
        subscription-id: "41c6e824-0f66-4076-81dd-f751c70a140b", resource-group: "xt-sandbox"}


Notes:
   - type should always be set to "batch".
   - url should be the URL of the Azure Batch account.
   - azure-login should always be set to true.
   - user-identity-id: this Id can be found in the Azure Portal page for the user-assigned managed identity, under Settings | Properties.
   - subscription-id is the id of the subscription containing the batch account.
   - resource-group is the name of the resource group containing the batch account.


