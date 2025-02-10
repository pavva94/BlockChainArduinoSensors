require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28",
  networks: {
    ganache: {
      url: "http://ganache:8545",
      accounts: ["0x0cb722dc6d52099482594ca293e5b2c19ef4934d05a610ffcdf05b33cb1ac0cc"]
    }
  }
};
