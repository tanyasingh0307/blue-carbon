# Blue Carbon MRV + Carbon Credit Trading Platform

A complete fullstack platform for Blue Carbon project monitoring, reporting, verification (MRV), and carbon credit trading with blockchain integration. Built with React, FastAPI, Solidity smart contracts, and AI-powered analysis.

## 🌊 Overview

The Blue Carbon MRV Platform is a comprehensive solution that enables NGOs, auditors, corporates, and government agencies to collaborate in ocean restoration projects while creating, verifying, and trading blockchain-verified carbon credits from mangroves, seagrasses, and salt marshes.

### Key Features
- **Multi-Stakeholder Platform**: Role-based dashboards for NGOs, auditors, corporates, and government
- **AI-Powered MRV**: Machine learning models for biomass estimation and CO₂ calculations
- **Blockchain Integration**: ERC-1155 smart contracts for tokenized carbon credits on Polygon
- **Transparent Marketplace**: Secure trading platform with immutable transaction records
- **Real-time Analytics**: Interactive dashboards with project monitoring and market insights

## 🚀 Features

### 🌱 NGO Dashboard
- Register new blue carbon restoration projects
- Upload monitoring data (satellite imagery, field measurements, water quality)
- Run AI-powered MRV analysis for CO₂ sequestration calculations
- Track project progress with real-time analytics
- Generate comprehensive MRV reports for auditor review

### 🔍 Auditor Portal
- Review pending MRV reports with detailed analysis
- Verify carbon calculations using scientific methodologies
- Approve reports and mint ERC-1155 carbon credit tokens
- Maintain audit trails with blockchain transparency
- Quality assurance dashboard with confidence scoring

### 💼 Corporate Marketplace
- Browse verified carbon credits with detailed project information
- Purchase credits with secure blockchain transactions
- Retire credits for carbon neutrality claims
- Portfolio management with transaction history
- Real-time market analytics and pricing data

### 🏛️ Government Oversight
- Monitor regional restoration progress and compliance
- Access comprehensive reporting and analytics
- Track policy impact on blue carbon initiatives
- Oversee marketplace transactions and credit retirement

## 🏗️ Getting Started

### Prerequisites
- **Node.js** (v18 or higher)
- **Python** (3.8 or higher) - Optional for backend
- **npm** or **yarn**
- **Git** for version control
- **Modern web browser** with MetaMask (optional, for blockchain features)

### 🚀 Quick Start

#### Option 1: Frontend Only (Demo Mode)
```bash
# 1. Clone and install
git clone <repository-url>
cd bluecarbon-mrv-platform
npm install

# 2. Start frontend (works without backend)
npm run dev

# 3. Open http://localhost:5173
# Login with: ngo@example.com / demo123
```

#### Option 2: Full Stack Development

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd bluecarbon-mrv-platform
   ```

2. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

3. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

4. **Install Smart Contract Dependencies**
   ```bash
   cd contracts
   npm install
   cd ..
   ```

5. **Set Up Environment Variables**
   ```bash
   # Backend configuration
   cp backend/.env.example backend/.env
   
   # Smart contracts configuration
   cp contracts/.env.example contracts/.env
   
   # Edit the .env files with your configuration
   ```

6. **Start the Development Environment**
   
   **Terminal 1 - Blockchain (Optional)**:
   ```bash
   cd contracts
   npx hardhat node
   ```
   
   **Terminal 2 - Deploy Smart Contract (Optional)**:
   ```bash
   cd contracts
   npx hardhat run scripts/deploy.js --network localhost
   ```
   
   **Terminal 3 - Backend API**:
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   **Terminal 4 - Frontend**:
   ```bash
   npm run dev
   ```

7. **Access the Application**
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/api/docs
   - **Blockchain Explorer**: http://localhost:8545 (if running local node)

## 🎯 Demo Mode Features

The platform works perfectly **without the backend** for demonstration purposes:

- **Authentication**: Demo users with different roles
- **Project Management**: Create and manage restoration projects
- **MRV Analysis**: Simulated AI-powered carbon calculations
- **Credit Trading**: Mock marketplace with purchase/retirement flows
- **Data Visualization**: Real-time charts and analytics
- **Blockchain Integration**: Simulated smart contract interactions

### Demo Accounts
- **NGO**: `ngo@example.com` / `demo123`
- **Auditor**: `auditor@example.com` / `demo123`  
- **Corporate**: `corporate@example.com` / `demo123`

## 🔄 Backend Integration

When the backend is running, the frontend automatically switches from demo mode to live API integration:

- **Real Authentication**: JWT tokens and user management
- **Database Storage**: Persistent project and user data
- **ML Processing**: Actual AI-powered MRV analysis
- **Blockchain**: Real smart contract interactions
- **File Uploads**: Monitoring data and document storage
## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Blockchain    │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Hardhat)     │
│                 │    │                 │    │                 │
│ • NGO Dashboard │    │ • REST API      │    │ • ERC-1155      │
│ • Auditor Portal│    │ • ML Service    │    │ • Smart Contract│
│ • Marketplace   │    │ • Web3 Bridge   │    │ • Token Minting │
│ • Analytics     │    │ • Database      │    │ • Transactions  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   ML Engine     │
                    │   (Python)      │
                    │                 │
                    │ • CO₂ Calculator│
                    │ • Biomass Model │
                    │ • Confidence    │
                    │ • Validation    │
                    └─────────────────┘
```

## 👥 Demo User Accounts

The platform includes pre-configured demo accounts for testing:

### NGO User
- **Email**: `ngo@example.com`
- **Password**: `demo123`
- **Role**: Register projects, upload data, run MRV analysis

### Auditor
- **Email**: `auditor@example.com`
- **Password**: `demo123`
- **Role**: Verify reports, mint carbon credits, quality assurance

### Corporate Buyer
- **Email**: `corporate@example.com`
- **Password**: `demo123`
- **Role**: Purchase credits, manage portfolio, retire credits

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Projects
- `POST /api/projects/` - Create new project
- `GET /api/projects/` - List projects
- `GET /api/projects/{id}` - Get project details
- `POST /api/projects/{id}/monitoring-data` - Upload monitoring data

### MRV Analysis
- `POST /api/mrv/{project_id}/generate-report` - Generate MRV report
- `GET /api/mrv/reports` - List MRV reports
- `PUT /api/mrv/reports/{id}/verify` - Verify report (auditor)

### Carbon Credits
- `POST /api/credits/mint` - Mint carbon credits (auditor)
- `GET /api/credits/` - List available credits
- `POST /api/credits/{id}/retire` - Retire credits

### Marketplace
- `GET /api/marketplace/credits` - Browse marketplace
- `POST /api/marketplace/purchase` - Purchase credits
- `GET /api/marketplace/portfolio` - User portfolio

## 🧪 Smart Contract Functions

### BlueCarbonCredits.sol (ERC-1155)

```solidity
// Mint carbon credits (auditor only)
function mintCredits(
    address to,
    uint256 tokenId,
    uint256 amount,
    string memory projectName,
    string memory projectType,
    // ... additional parameters
) public onlyRole(AUDITOR_ROLE)

// Retire carbon credits
function retireCredits(
    uint256 tokenId,
    uint256 amount,
    string memory reason
) public

// Set MRV report IPFS hash
function setMRVReport(
    uint256 tokenId,
    string memory ipfsHash
) public onlyRole(AUDITOR_ROLE)
```

## 🤖 ML Analysis Engine

The platform includes a sophisticated ML engine for carbon sequestration analysis:

### Features
- **Species-Specific Models**: Tailored calculations for mangroves, seagrass, and salt marshes
- **Environmental Factors**: Temperature, salinity, tidal range, soil conditions
- **Growth Curves**: Age-based sequestration rate adjustments
- **Data Integration**: Satellite imagery, field measurements, water quality data
- **Confidence Scoring**: Statistical confidence in CO₂ estimates

### Usage Example
```python
from ml.co2_calculator import BlueCarbonCalculator

calculator = BlueCarbonCalculator()
results = calculator.calculate_sequestration(
    project_type="mangroves",
    area_hectares=25.5,
    age_years=2.5,
    environmental_data=env_data,
    monitoring_data=monitoring_data
)
```

## 📊 Sample Data

The platform includes comprehensive sample datasets:

- **`data/sample_projects.json`**: Example blue carbon projects
- **`data/sample_monitoring_data.json`**: Monitoring data examples
- **Sample environmental conditions and baseline data**
- **Realistic CO₂ sequestration calculations**

## 🏗️ Project Structure
```
bluecarbon-mrv-platform/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Main application pages
│   │   ├── contexts/       # React contexts
│   │   └── services/       # API service layer
│   └── package.json
├── backend/                 # FastAPI backend
│   ├── routers/            # API route handlers
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic services
│   ├── database/           # Database configuration
│   └── requirements.txt
├── contracts/              # Solidity smart contracts
│   ├── contracts/          # Contract source files
│   ├── scripts/            # Deployment scripts
│   ├── test/              # Contract tests
│   └── hardhat.config.js
├── ml/                     # Machine learning modules
│   └── co2_calculator.py   # CO₂ sequestration calculator
├── data/                   # Sample datasets
│   ├── sample_projects.json
│   └── sample_monitoring_data.json
└── README.md
```

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Recharts** for data visualization
- **Lucide React** for icons
- **Axios** for API communication

### Backend
- **FastAPI** (Python) for REST API
- **SQLAlchemy** ORM with SQLite database
- **Pydantic** for data validation
- **Web3.py** for blockchain integration
- **JWT** authentication
- **CORS** enabled for frontend integration

### Blockchain
- **Solidity** smart contracts
- **Hardhat** development framework
- **OpenZeppelin** contract libraries
- **ERC-1155** multi-token standard
- **Polygon** network support

### Machine Learning
- **Python** with NumPy and Pandas
- **Scikit-learn** for ML models
- **Custom algorithms** for blue carbon calculations
- **Environmental factor analysis**

## 🚀 Deployment Options

### Local Development
```bash
# Start all services locally
npm run dev          # Frontend
uvicorn main:app --reload  # Backend
npx hardhat node     # Blockchain (optional)
```

### Production Deployment

#### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy dist/ folder to hosting service
```

#### Backend (Railway/Heroku)
```bash
# Set environment variables
# Deploy backend/ folder
```

#### Smart Contracts (Polygon Mumbai)
```bash
cd contracts
npx hardhat run scripts/deploy.js --network mumbai
```

## 🧪 Testing

### Frontend Tests
```bash
npm run test
```

### Backend Tests
```bash
cd backend
pytest
```

### Smart Contract Tests
```bash
cd contracts
npx hardhat test
```

## 📈 Demo Workflow

1. **NGO Registration**: Create account and register a blue carbon project
2. **Data Upload**: Upload monitoring data (satellite, field measurements)
3. **MRV Analysis**: Run AI-powered CO₂ sequestration analysis
4. **Report Generation**: Generate comprehensive MRV report
5. **Auditor Review**: Auditor verifies calculations and methodology
6. **Credit Minting**: Approved reports mint ERC-1155 carbon credit tokens
7. **Marketplace Listing**: Credits become available for purchase
8. **Corporate Purchase**: Companies buy credits for carbon offsetting
9. **Credit Retirement**: Permanent retirement for carbon neutrality claims
10. **Transparency**: All transactions recorded on blockchain

## 🔐 Security Features

- **JWT Authentication** with role-based access control
- **Smart Contract Security** with OpenZeppelin libraries
- **Data Validation** with Pydantic schemas
- **SQL Injection Protection** with SQLAlchemy ORM
- **CORS Configuration** for secure API access
- **Blockchain Audit Trail** for all transactions

## 🌍 Environmental Impact

This platform directly supports:
- **UN SDG 13**: Climate Action through carbon sequestration
- **UN SDG 14**: Life Below Water via ocean ecosystem restoration
- **UN SDG 15**: Life on Land through coastal habitat protection
- **Paris Agreement**: Carbon market mechanisms for climate goals

## 📚 Scientific Methodology

The platform uses peer-reviewed scientific methodologies:
- **IPCC Wetlands Supplement** for carbon calculations
- **Verified Carbon Standard (VCS)** methodologies
- **Blue Carbon Initiative** best practices
- **Remote sensing** validation techniques
- **Allometric equations** for biomass estimation

## 🤝 Contributing

We welcome contributions from developers, scientists, and sustainability experts:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines
- Follow TypeScript/Python best practices
- Write comprehensive tests
- Update documentation
- Ensure security compliance
- Test blockchain integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Blue Carbon Initiative** for scientific guidance
- **OpenZeppelin** for secure smart contract libraries
- **FastAPI** and **React** communities for excellent frameworks
- **Ocean restoration organizations** for real-world validation
- **Climate tech community** for inspiration and support

## 📧 Support & Contact

- **Documentation**: [Project Wiki](wiki-url)
- **Issues**: [GitHub Issues](issues-url)
- **Discussions**: [GitHub Discussions](discussions-url)
- **Email**: support@bluecarbon-platform.org
- **Twitter**: @BlueCarbonMRV

---

**Building a sustainable future through verified ocean restoration and transparent carbon markets.**

## 🚀 Quick Demo Commands

```bash
# 1. Install dependencies
npm install

# 2. Install backend dependencies
cd backend && pip install -r requirements.txt && cd ..

# 3. Install contract dependencies
cd contracts && npm install && cd ..

# 4. Set up environment variables
cp .env.example .env
cp backend/.env.example backend/.env
cp contracts/.env.example contracts/.env

# 5. Start blockchain (Terminal 1 - Optional)
cd contracts && npx hardhat node

# 6. Deploy contracts (Terminal 2 - Optional)
cd contracts && npx hardhat run scripts/deploy.js --network localhost

# 7. Start backend (Terminal 3)
cd backend && uvicorn main:app --reload

# 8. Start frontend (Terminal 4)
npm run dev

# 9. Open http://localhost:5173 and start exploring!
```

## 🔧 Development Scripts

```bash
# Start frontend only
npm run dev

# Start backend only
npm run dev:backend

# Start blockchain node
npm run dev:contracts

# Deploy smart contracts
npm run deploy:contracts
```

## 🌐 API Integration

The frontend automatically connects to the backend API. If the backend is not running, it falls back to demo mode with mock data.

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Blockchain Node**: http://localhost:8545 (optional)

**Demo Flow**: Login as NGO → Create Project → Upload Data → Run MRV → Switch to Auditor → Verify Report → Mint Credits → Switch to Corporate → Purchase Credits → Retire for Impact! 🌊

## 🌍 System Architecture

### Frontend (Current Implementation)
- React SPA with role-based authentication
- Responsive design optimized for all devices
- Real-time data visualization and analytics
- Intuitive user interfaces for each stakeholder type

### Planned Backend Integration
- **FastAPI** backend with SQLAlchemy ORM
- **PostgreSQL** database for production scalability
- **Web3.py** integration for blockchain interactions
- **Machine Learning** pipeline for automated MRV analysis
- **IPFS** integration for decentralized data storage

### Blockchain Components (Planned)
- **Smart Contracts**: ERC-1155 tokens for carbon credits
- **Polygon Network**: Low-cost, environmentally friendly blockchain
- **Hardhat**: Development and deployment framework
- **MetaMask Integration**: Web3 wallet connectivity

## 📊 Data Flow

1. **Project Registration**: NGOs submit restoration projects with baseline data
2. **MRV Analysis**: AI models process satellite imagery and field measurements
3. **Verification**: Certified auditors review and approve carbon calculations
4. **Credit Minting**: Blockchain smart contracts mint verified carbon tokens
5. **Marketplace Trading**: Corporates purchase and retire credits transparently
6. **Impact Tracking**: Real-time monitoring of restoration progress and carbon impact

## 🔐 Security Features

- Role-based access control with JWT authentication
- Blockchain-based audit trails for all transactions
- IPFS storage for tamper-proof documentation
- Smart contract security for credit issuance and trading
- Multi-signature verification for high-value transactions

## 🌱 Sustainability Impact

The platform directly supports UN Sustainable Development Goals:
- **SDG 13**: Climate Action through carbon sequestration
- **SDG 14**: Life Below Water via ocean ecosystem restoration
- **SDG 15**: Life on Land through coastal habitat protection

## 🚀 Deployment

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm run preview
```

### Environment Variables (for full backend integration)
```bash
VITE_API_URL=https://api.bluecarbon.org
VITE_BLOCKCHAIN_RPC=https://polygon-rpc.com
VITE_IPFS_GATEWAY=https://ipfs.io/ipfs/
```

## 🤝 Contributing

We welcome contributions from developers, scientists, and sustainability experts:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Blue carbon research community for methodology guidance
- Blockchain carbon credit pioneers for tokenization standards
- Open source contributors to the underlying technology stack
- Ocean restoration organizations for real-world validation

## 📧 Contact

For questions, partnerships, or support:
- **Website**: https://bluecarbon-platform.org
- **Email**: support@bluecarbon-platform.org
- **Twitter**: @BlueCarbonMRV

---

*Building a sustainable future through verified ocean restoration and transparent carbon markets.*