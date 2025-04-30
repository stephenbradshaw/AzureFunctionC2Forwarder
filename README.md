# AzureFunctionC2Forwarder
Simple POC for an Azure Function C2 Forwarder


# Prerequisites

* Setup the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)
* Configure an Azure function with local private network access for outbound network traffic and a private VPC subnet for virtual network integration
* Setup and Azure VM with a C2 and allow traffic from the subnet of the Azure function to port 80
* Set the `DESTINATION` environment variable in the functions config with the private IP address of the Azure VM



# Deployment


Zip deployment to a configured function with name `<FUNCTION_NAME>` in resource group `<RESOURCE_GROUP>` like so.


```
zip -r /tmp/dep.zip .
az functionapp deployment source config-zip -g <RESOURCE_GROUP> -n <FUNCTION_NAME> --src /tmp/dep.zip
```

The forwarder will be available at the address: `https://<FUNCTION_NAME>.azurewebsites.net/`
