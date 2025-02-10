# FastAPI Server for Home Monitoring System

## 📌 Project Overview
This FastAPI server acts as the backend for the home monitoring system. It receives sensor data via Bluetooth from an Arduino Nano 33 BLE Sense, stores it on **IPFS**, and records the corresponding **IPFS hash** on a **Ganache (Ethereum) blockchain** for immutable storage.

## ⚡ Features
- Receives **temperature, humidity, and pressure** data from Arduino over Bluetooth
- Stores sensor data on **IPFS** for decentralized storage
- Saves the **IPFS hash** on **Ganache blockchain** for verification
- Exposes **FastAPI endpoints** to retrieve stored data and blockchain transactions

## 🛠 Technologies Used
- **FastAPI** → REST API framework
- **Web3.py** → Interact with Ganache blockchain
- **IPFS HTTP API** → Store and retrieve sensor data
- **Bluetooth (BLE)** → Receive data from Arduino
- **Docker** → Containerized deployment

---

## 🚀 Installation & Setup

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-repo.git
cd your-repo
```

### 2️⃣ **Set Up Environment Variables**
Create a `.env` file in the FastAPI directory with the following:
```ini
GANACHE_URL=http://ganache:8545
IPFS_API_URL=http://ipfs:5001
PRIVATE_KEY=your_private_key_here
CONTRACT_ADDRESS=your_contract_address_here
```

### 3️⃣ **Run the FastAPI Server with Docker**
Ensure **Docker** and **Docker Compose** are installed, then run:
```sh
docker-compose up -d
```
This will start FastAPI along with Ganache and IPFS.

### 4️⃣ **Run the Server Without Docker** (Optional)
If running locally, install dependencies:
```sh
pip install -r requirements.txt
```
Run the FastAPI server:
```sh
uvicorn app.main:app --host 0.0.0.0 --port 5001
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

## 📌 Next Steps
- Implement **authentication** for API endpoints
- Improve **error handling** for failed transactions
- Add **WebSocket** support for real-time updates

---

### 💡 Need Help?
If you encounter any issues, feel free to open an issue or contribute to the repository!

🚀 Happy Coding!

