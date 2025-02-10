const hre = require("hardhat");

async function main() {
  const SensorData = await hre.ethers.getContractFactory("SensorData");
  const sensorData = await SensorData.deploy();

  await sensorData.waitForDeployment();  // ✅ Replaces "deployed()"

  console.log(`Contract deployed to: ${await sensorData.getAddress()}`);  // ✅ Use "getAddress()" instead of "address"
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
