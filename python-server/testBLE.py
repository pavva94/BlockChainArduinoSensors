import asyncio
from bleak import BleakScanner

async def discover_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        # Print the MAC address and name of each discovered device
        print(f"Device: {device.name}, MAC Address: {device.address}")

if __name__ == "__main__":
    asyncio.run(discover_devices())
