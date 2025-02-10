# Home Monitoring System with Blockchain and IPFS

## 📌 Project Overview
This project is a **home monitoring system** that collects environmental sensor data (temperature, humidity, and pressure) using an **Arduino Nano 33 BLE Sense** and sends the data via **Bluetooth** to a **Python server**. The data is then stored on **IPFS** (InterPlanetary File System), and only the hash of the data is recorded on a **local blockchain** (Ganache) using a **smart contract** written in Solidity.

---

**🎯 This system ensures secure, immutable storage of home sensor data using blockchain and IPFS, making it a reliable and decentralized monitoring solution.** 🚀

## 🛠️ Technology Choices & Justification

| Technology | Purpose |
|------------|---------|
| **Arduino Nano 33 BLE Sense** | Collects sensor data (temperature, humidity, pressure) and sends it via Bluetooth |
| **Bluetooth (BLE)** | Enables wireless data transmission from Arduino to Python server |
| **Python** | Manages data reception, blockchain interactions, and IPFS storage |
| **Web3.py** | Connects the Python server to the Ethereum-compatible Ganache blockchain |
| **Ganache (Docker)** | Local blockchain to store hashes of sensor data |
| **Solidity** | Smart contract language to manage data on the blockchain |
| **IPFS (Docker)** | Decentralized file storage to store sensor data securely |
| **Hardhat** | Ethereum development environment to compile and deploy smart contracts |
| **Docker & Docker Compose** | Containerized deployment for IPFS, Ganache, and the Python server |

## 📥 Installation Guide

### 🖥️ Prerequisites
Make sure you have the following installed on your system:
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Node.js (v18 or higher)](https://nodejs.org/)
- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [Arduino IDE](https://www.arduino.cc/en/software/)

### 📂 Folder Structure
```plaintext
/home-monitoring-system
├── blockchain/             # Hardhat smart contract setup
│   ├── contracts/          # Solidity contracts
│   ├── scripts/            # Deployment scripts
│   ├── artifacts/          # ABI & compiled contracts
├── ipfs/                   # IPFS setup
├── python-server/          # Python backend
│   ├── server.py           # Main server handling Bluetooth, IPFS, and blockchain
│   ├── web3_client.py      # Blockchain interaction
│   ├── requirements.txt    # Python dependencies
├── arduino/                # Arduino firmware
│   ├── home_monitor.ino    # Arduino BLE sensor script
├── docker-compose.yml      # Docker container setup
├── README.md               # Documentation
```

### 🚀 Setup & Run the Project

### Without Docker

#### **Step 1: Clone the Repository**
```sh
git clone https://github.com/your-repo/home-monitoring-system.git
cd home-monitoring-system
```

#### **Step 2: Install Python Dependencies**
```sh
cd python-server
pip install -r requirements.txt
```

#### **Step 3: Set Up the Blockchain & IPFS Containers**
Run the following command in the root directory to start the blockchain (Ganache) and IPFS services.
```sh
docker-compose up -d
```
This will start the following services:
- **Ganache (Local Ethereum Blockchain) on port 8545**
- **IPFS Node on ports 5001 (API) & 8080 (Gateway)**

#### **Step 4: Compile and Deploy Smart Contract**
```sh
cd blockchain
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

#### **Step 5: Retrieve the Smart Contract ABI**
Copy the ABI from:
```plaintext
blockchain/artifacts/contracts/SensorData.sol/SensorData.json
```
Paste it into `python-server/web3_client.py` where required.

#### **Step 6: Run the Python Server**
```sh
cd python-server
python server.py
```

#### **Step 7: Upload Arduino Code**
- Open `arduino/home_monitor.ino` in **Arduino IDE**.
- Select **Arduino Nano 33 BLE Sense** as the board.
- Upload the code to the board.

#### **Step 8: Send Sensor Data via Bluetooth**
- Ensure the Arduino is powered on.
- The Python server will receive data, store it in IPFS, and log the hash on the blockchain.


---
### With Docker

Only with FastAPI endpoints.


#### **Step 1: Compose Build**
```sh
docker-compose build --no-cache
```

#### **Step 2: Compose Up**
```sh
docker-compose up --build   
```



---



## 📡 API Endpoints

### 🔹 **Send Sensor Data**
**POST** `/sensor/data`
```json
{
  "temperature": 22.5,
  "humidity": 45.3,
  "pressure": 1013.2
}
```
- Stores data on IPFS
- Saves IPFS hash on blockchain

### 🔹 **Retrieve Sensor Data**
**GET** `/sensor/data/{ipfs_hash}`
- Fetches stored sensor data from IPFS

### 🔹 **Check Blockchain Transactions**
**GET** `/blockchain/transactions`
- Lists all recorded IPFS hashes on blockchain

---

## 🛠 Development & Debugging
### 🔍 Check Running Containers
```sh
docker ps
```
### 📝 View FastAPI Logs
```sh
docker logs python-server -f
```
### 📡 Test API with cURL
```sh
curl -X POST "http://localhost:5001/sensor/data" -H "Content-Type: application/json" -d '{"temperature": 22.5, "humidity": 50, "pressure": 1012}'
```

---



## 📌 Future Improvements
- Implement a web dashboard for real-time monitoring.
- Add voice command integration for data queries.
- Optimize data storage using additional compression techniques.
- Implement **authentication** for API endpoints
- Improve **error handling** for failed transactions
- Add **WebSocket** support for real-time updates

## 🤝 Contributing
Feel free to fork this repository, submit issues, or suggest improvements.

curl -X 'POST' 'http://127.0.0.1:8000/store_sensor_data/' -H 'Content-Type: application/json' -d '{"temperature": 22.5,"humidity": 60.5,"pressure": 1012.3,"timestamp": 1618254789 }'
