import requests
import time


def test_ipfs_connection():
    try:
        # Connect to the IPFS container via HTTP
        ipfs_url = 'http://ipfs:5001/api/v0/id'  # API endpoint to get node information
        response = requests.post(ipfs_url)

        if response.status_code == 200:
            print("Successfully connected to IPFS!")
            node_id = response.json()  # Parse the response JSON to get the node ID
            print("Node ID:", node_id)
        else:
            print(f"Failed to connect to IPFS. Status Code: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to IPFS: {e}")

if __name__ == "__main__":
    # Waiting the other services to start
    print("Waiting to connect..")
    X = 25
    time.sleep(X)
    test_ipfs_connection()
