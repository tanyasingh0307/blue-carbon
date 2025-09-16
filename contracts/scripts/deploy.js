const { ethers } = require("hardhat");

async function main() {
  console.log("🌊 Deploying Blue Carbon Credits contract...");

  // Get the contract factory
  const BlueCarbonCredits = await ethers.getContractFactory("BlueCarbonCredits");

  // Deploy the contract
  const blueCarbonCredits = await BlueCarbonCredits.deploy();
  await blueCarbonCredits.deployed();

  console.log("✅ BlueCarbonCredits deployed to:", blueCarbonCredits.address);

  // Get network information
  const network = await ethers.provider.getNetwork();
  console.log("📡 Network:", network.name, "Chain ID:", network.chainId);

  // Get deployer information
  const [deployer] = await ethers.getSigners();
  console.log("👤 Deployed by:", deployer.address);
  console.log("💰 Account balance:", ethers.utils.formatEther(await deployer.getBalance()), "ETH");

  // Verify contract has correct roles
  const DEFAULT_ADMIN_ROLE = await blueCarbonCredits.DEFAULT_ADMIN_ROLE();
  const AUDITOR_ROLE = await blueCarbonCredits.AUDITOR_ROLE();
  
  const hasAdminRole = await blueCarbonCredits.hasRole(DEFAULT_ADMIN_ROLE, deployer.address);
  const hasAuditorRole = await blueCarbonCredits.hasRole(AUDITOR_ROLE, deployer.address);
  
  console.log("🔐 Deployer has admin role:", hasAdminRole);
  console.log("🔍 Deployer has auditor role:", hasAuditorRole);

  // Save deployment info
  const deploymentInfo = {
    contractAddress: blueCarbonCredits.address,
    network: network.name,
    chainId: network.chainId,
    deployer: deployer.address,
    deploymentTime: new Date().toISOString(),
    blockNumber: await ethers.provider.getBlockNumber()
  };

  console.log("\n📋 Deployment Summary:");
  console.log(JSON.stringify(deploymentInfo, null, 2));

  // Instructions for backend integration
  console.log("\n🔧 Backend Integration:");
  console.log("1. Update your .env file with:");
  console.log(`   CONTRACT_ADDRESS=${blueCarbonCredits.address}`);
  console.log(`   WEB3_PROVIDER_URL=${network.name === 'localhost' ? 'http://127.0.0.1:8545' : 'your-rpc-url'}`);
  console.log("\n2. Make sure your private key has the AUDITOR_ROLE to mint credits");
  console.log("\n3. The contract supports ERC1155 standard with additional features:");
  console.log("   - mintCredits(): Mint new carbon credits (auditor only)");
  console.log("   - retireCredits(): Permanently retire credits");
  console.log("   - setMRVReport(): Link IPFS hash for transparency");

  return blueCarbonCredits.address;
}

main()
  .then((address) => {
    console.log(`\n🎉 Deployment completed successfully!`);
    console.log(`Contract address: ${address}`);
    process.exit(0);
  })
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });