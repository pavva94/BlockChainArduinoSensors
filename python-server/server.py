import asyncio
from bleak import BleakClient
import time
import ipfshttpclient
from web3 import Web3
import json

# Blockchain Connection (Ganache)
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

with open("SensorData_abi.json") as f:
    contract_data = json.load(f)
    abi = contract_data['abi']  # Extract ABI

contract_address = "0x2A942bA77d19Caeb827163aB706394c21167f9Eb"  # Replace with your contract address
contract = web3.eth.contract(address=contract_address, abi=abi)
account = web3.eth.accounts[0]  # Replace with the appropriate account

# IPFS Connection
ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

# BLE Characteristics UUIDs (matching Arduino)
TEMPERATURE_UUID = "2A1C"
HUMIDITY_UUID = "2A6F"
PRESSURE_UUID = "2A6D"


async def read_sensor_data(address):
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


def main():
    # Replace with the MAC address of your Arduino Nano 33 BLE Sense
    address = "0ED28FBB-7208-3275-734C-12D7A24115DB"
    asyncio.run(read_sensor_data(address))


if __name__ == "__main__":
    main()
