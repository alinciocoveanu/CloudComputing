from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.common.credentials import ServicePrincipalCredentials

# OS ENVIRONMENT VARS
import os
#


credentials = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://petify-vault.vault.azure.net/", credential=credentials)


# Storage key
def get_storage_secret():
    return secret_client.get_secret('storage-secret').value


# DB key
def get_db_secret():
    masterKey = secret_client.get_secret('db-mk-secret').value
    resourceTokens = secret_client.get_secret('db-rt-secret').value
    return {"masterKey": masterKey, "resourceTokens": resourceTokens}


if __name__ == '__main__':
    print(get_storage_secret())
    print(get_db_secret())
