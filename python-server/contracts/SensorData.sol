// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SensorData {
    struct SensorReading {
        string ipfsHash;  // Hash of the data stored on IPFS
        uint256 timestamp; // Time of data entry
    }

    mapping(address => SensorReading[]) private sensorReadings;

    event DataStored(address indexed sender, string ipfsHash, uint256 timestamp);

    function storeData(string memory _ipfsHash) public {
        sensorReadings[msg.sender].push(SensorReading(_ipfsHash, block.timestamp));
        emit DataStored(msg.sender, _ipfsHash, block.timestamp);
    }

    function getLatestData() public view returns (string memory ipfsHash, uint256 timestamp) {
        require(sensorReadings[msg.sender].length > 0, "No data stored");
        SensorReading memory latest = sensorReadings[msg.sender][sensorReadings[msg.sender].length - 1];
        return (latest.ipfsHash, latest.timestamp);
    }

    function getDataCount() public view returns (uint256) {
        return sensorReadings[msg.sender].length;
    }
}
