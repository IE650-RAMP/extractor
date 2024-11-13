import os
import requests
from requests.auth import HTTPBasicAuth

def delete_blazegraph_namespace(namespace):
    """
    Deletes the specified Blazegraph namespace.

    Parameters:
    namespace (str): The name of the Blazegraph namespace to delete.

    Returns:
    bool: True if the operation was successful, False otherwise.
    """
    graph_endpoint = os.getenv("GRAPH_ENDPOINT")
    username = os.getenv("GRAPH_USERNAME")
    password = os.getenv("GRAPH_PASSWORD")
    
    # Construct the namespace URL
    namespace_url = f"{graph_endpoint}/namespace/{namespace}"
    
    headers = {
        "Accept": "application/json"
    }

    try:
        # Perform the DELETE request with or without authentication based on environment variables
        if username and password:
            response = requests.delete(namespace_url, headers=headers, auth=HTTPBasicAuth(username, password))
        else:
            response = requests.delete(namespace_url, headers=headers)
        
        if response.status_code == 200:
            print(f"Namespace '{namespace}' deleted successfully.")
            return True
        else:
            print(f"Failed to delete namespace. Status code: {response.status_code}, Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Blazegraph: {e}")
        return False
    
def create_blazegraph_namespace(namespace):
    """
    Creates a new Blazegraph namespace with optional configuration settings.

    Parameters:
    namespace (str): The name of the Blazegraph namespace to create.
    config_content (str): The configuration content for the namespace, in the Blazegraph configuration format.
                          If not provided, a default configuration will be used.

    Returns:
    bool: True if the namespace was created successfully, False otherwise.
    """

    graph_endpoint = os.getenv("GRAPH_ENDPOINT")
    username = os.getenv("GRAPH_USERNAME")
    password = os.getenv("GRAPH_PASSWORD")
    
    # Construct the endpoint URL for creating a namespace
    create_url = f"{graph_endpoint}/namespace"
    
    # Default configuration with the provided settings, using the specified namespace
    default_config = f"com.bigdata.rdf.sail.namespace={namespace}"
    
    headers = {
        "Content-Type": "text/plain;charset=iso-8859-1",
        "Accept": "application/json"
    }

    try:
        # Perform the POST request with or without authentication based on environment variables
        if username and password:
            response = requests.post(create_url, headers=headers, data=default_config,
                                     auth=HTTPBasicAuth(username, password))
        else:
            response = requests.post(create_url, headers=headers, data=default_config)
        
        if response.status_code == 201:
            print(f"Namespace '{namespace}' created successfully.")
            return True
        else:
            print(f"Failed to create namespace. Status code: {response.status_code}, Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Blazegraph: {e}")
        return False