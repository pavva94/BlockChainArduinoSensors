import asyncio
import time
import json
import ipfshttpclient
from web3 import Web3
from bleak import BleakClient


# BLE Characteristics UUIDs (matching Arduino)
TEMPERATURE_UUID = "2A1C"
HUMIDITY_UUID = "2A6F"
PRESSURE_UUID = "2A6D"

# Ganache URL and Contract
ganache_url = "http://ganache:8545"
contract_address = ""

# Replace with the MAC address of your Arduino Nano 33 BLE Sense
mac_address = ""
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


# IPFS Connection
def connect_to_ipfs():
    ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/')
    print("Connected to IPFS.")
    return ipfs_client


# Function to read sensor data
async def read_sensor_data(address, ipfs_client, contract, account):
    async with BleakClient(address) as client:
        print(f"Connected to {address}")

        # Read the sensor characteristics
        temperature = await client.read_gatt_char(TEMPERATURE_UUID)
        humidity = await client.read_gatt_char(HUMIDITY_UUID)
        pressure = await client.read_gatt_char(PRESSURE_UUID)

        temperature = int.from_bytes(temperature, byteorder='little') / 100.0
        humidity = int.from_bytes(humidity, byteorder='little') / 100.0
        pressure = int.from_bytes(pressure, byteorder='little') / 1000.0

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

        with open("sensor_data.json", "w") as f:
            json.dump(payload, f)

        # Upload to IPFS
        res = ipfs_client.add("sensor_data.json")
        ipfs_hash = res["Hash"]
        print(f"Data stored in IPFS: {ipfs_hash}")

        # Store hash in blockchain
        tx_hash = contract.functions.storeData(ipfs_hash, "arduino_sensor").transact({'from': account})
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Stored IPFS hash in blockchain: {ipfs_hash}")


# Main function to tie everything together
def main():
    # Waiting the other services to start
    print("Waiting to connect..")
    X = 25
    time.sleep(X)

    # Connect to Blockchain and IPFS
    web3, contract, account = connect_to_blockchain()
    ipfs_client = connect_to_ipfs()

    asyncio.run(read_sensor_data(mac_address, ipfs_client, contract, account))


if __name__ == "__main__":
    main()
