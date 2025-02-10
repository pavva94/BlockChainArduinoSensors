import time
from web3 import Web3

print("Waiting to connect..")
# Wait for X seconds before trying to connect
X = 25  # Change this value to the number of seconds you want to wait
time.sleep(X)

ganache_url = "http://ganache:8545"
w3 = Web3(Web3.HTTPProvider(ganache_url))



if w3.is_connected():
    print("Connected to Ganache!")
    print("Accounts:", w3.eth.accounts)
else:
    print("Failed to connect to Ganache.")
