import ipfshttpclient
import time

def test_ipfs_connection():
    # Waiting the other services to start
    print("Waiting to connect..")
    X = 25
    time.sleep(X)

    try:
        # Connect to local IPFS node
        ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

        # Fetch and print IPFS node ID
        node_id = ipfs_client.id()
        print("Successfully connected to IPFS!")
        print("Node ID:", node_id)

    except Exception as e:
        print("Failed to connect to IPFS:", e)

if __name__ == "__main__":
    test_ipfs_connection()
