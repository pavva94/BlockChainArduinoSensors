from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import json
import traceback
import requests
from web3 import Web3


# Ganache URL and Contract
ganache_url = "http://ganache:8545"
contract_address = "0x2A942bA77d19Caeb827163aB706394c21167f9Eb"

# IPFS endpoint for adding files
ipfs_url_add = 'http://ipfs:5001/api/v0/add'


# Blockchain Connection (Ganache)
def connect_to_blockchain():

    web3 = Web3(Web3.HTTPProvider(ganache_url))

    if not web3.is_connected():
        raise Exception("Failed to connect to Ganache.")

    print("Connected to Blockchain.")

    with open("SensorData_abi.json") as f:
        contract_data = json.load(f)
        abi = contract_data['abi']  # Extract ABI


    contract = web3.eth.contract(address=contract_address, abi=abi)

    accounts = web3.eth.accounts  # List of accounts
    if len(accounts) == 0:
        raise Exception("No accounts found. Make sure Ganache is running.")

    account = accounts[0]  # Use the first available account
    print("Using Account:", account)

    return web3, contract, account


def upload_json_to_ipfs(json_data):
    try:
        # Convert the JSON data to bytes
        json_bytes = json.dumps(json_data).encode('utf-8')

        # Send the data to IPFS
        response = requests.post(ipfs_url_add, files={'file': ('sensor_data.json', json_bytes)})

        # Check if the upload was successful
        if response.status_code == 200:
            ipfs_hash = response.json()['Hash']  # Get the IPFS hash from the response
            print(f"Successfully uploaded JSON to IPFS!")
            print(f"IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Failed to upload JSON to IPFS. Status Code: {response.status_code}")
            print(response.text)
            raise Exception("Failed to upload JSON to IPFS. Status text: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error uploading JSON to IPFS: {e}")

# Function to write sensor data
async def store_data_in_blockchain(data, web3, contract, account):

    temperature = data["temperature"]
    humidity = data["humidity"]
    pressure = data["pressure"]

    print(f"Temperature: {temperature} °C")
    print(f"Humidity: {humidity} %")
    print(f"Pressure: {pressure} hPa")

    # Save data to IPFS
    payload = {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "timestamp": int(time.time())
    }

    # Upload to IPFS
    # res = ipfs_client.add("sensor_data.json")
    ipfs_hash = upload_json_to_ipfs(payload)
    # ipfs_hash = res["Hash"]
    print(f"Data stored in IPFS: {ipfs_hash}")

    # Store hash in blockchain
    tx_hash = contract.functions.storeData(ipfs_hash).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Stored IPFS hash in blockchain: {ipfs_hash}")

    return ipfs_hash


# Define the Pydantic model for sensor data
class SensorData(BaseModel):
    temperature: float
    humidity: float
    pressure: float
    # timestamp: int

# FastAPI instance
app = FastAPI()

@app.post("/store_sensor_data/")
async def store_sensor_data(sensor_data: SensorData):
    """
    Endpoint to receive sensor data and store it asynchronously in the blockchain.
    """
    try:
        # Convert the received data to a dictionary for the blockchain function
        data_dict = sensor_data.dict()
        print(f"Data received: {data_dict}")

        # Connect to Blockchain and IPFS
        web3, contract, account = connect_to_blockchain()
        print("Blockchain Connected..")

        # Call the async function to store data in the blockchain and get the hash
        ipfs_hash = await store_data_in_blockchain(data_dict, web3, contract, account)
        print(f"IPFS hash: {ipfs_hash}")

        # Return the IPFS hash (or other relevant data)
        return {"status": "success", "ipfs_hash": ipfs_hash}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("http_server:app", host="0.0.0.0", port=8000, reload=True)
