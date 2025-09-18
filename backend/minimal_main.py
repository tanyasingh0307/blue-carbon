"""
Minimal FastAPI backend for Blue Carbon MRV Platform
Simplified version that should work without complex dependencies
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Blue Carbon MRV Platform API",
    description="Minimal API for Blue Carbon platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Blue Carbon MRV Platform API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Demo authentication endpoint
@app.post("/api/auth/login")
async def login(email: str, password: str):
    """Demo login endpoint"""
    demo_users = {
        'ngo@example.com': {'role': 'ngo', 'name': 'NGO User'},
        'auditor@example.com': {'role': 'auditor', 'name': 'Auditor User'},
        'corporate@example.com': {'role': 'corporate', 'name': 'Corporate User'}
    }
    
    if email in demo_users and password == 'demo123':
        return {
            'access_token': f'demo-token-{demo_users[email]["role"]}',
            'user': {
                'email': email,
                'role': demo_users[email]['role'],
                'name': demo_users[email]['name']
            }
        }
    
    return {"error": "Invalid credentials"}

@app.get("/api/projects/")
async def get_projects():
    """Demo projects endpoint"""
    return [
        {
            "id": 1,
            "name": "Mangrove Restoration Bay Area",
            "location": "Florida Keys, USA",
            "project_type": "mangroves",
            "area_hectares": 25.5,
            "status": "active"
        }
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
</parameter>