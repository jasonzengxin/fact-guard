#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up FactGuard project...${NC}"

# Initialize Git repository if not already initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
    echo -e "${GREEN}Git repository initialized${NC}"
fi

# Create project structure
echo -e "${YELLOW}Creating project structure...${NC}"

# Create directories
mkdir -p backend/app/{api,core,models,services,static}
mkdir -p frontend/{public,src/components}

# Function to safely move files
safe_move() {
    if [ -f "$1" ]; then
        mv "$1" "$2"
        echo -e "${GREEN}Moved $1 to $2${NC}"
    else
        echo -e "${YELLOW}Warning: $1 not found, skipping...${NC}"
    fi
}

# Move or create backend files
if [ -f "main.py" ]; then
    # If files exist, move them
    safe_move "main.py" "backend/"
    safe_move "requirements.txt" "backend/"
    
    if [ -d "app" ]; then
        for dir in api core models services; do
            if [ -d "app/$dir" ]; then
                safe_move "app/$dir/*" "backend/app/$dir/"
            fi
        done
    fi
else
    # Create basic backend files
    echo -e "${YELLOW}Creating basic backend files...${NC}"
    
    # Create main.py
    cat > backend/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FactGuard API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to FactGuard API"}
EOF

    # Create requirements.txt
    cat > backend/requirements.txt << 'EOF'
fastapi==0.68.1
uvicorn==0.15.0
python-dotenv==0.19.0
openai==0.27.0
pydantic==1.8.2
EOF
fi

# Move or create frontend files
if [ -d "src" ]; then
    safe_move "src/*" "frontend/src/"
    safe_move "public/*" "frontend/public/"
    safe_move "package.json" "frontend/"
    safe_move "tailwind.config.js" "frontend/"
else
    # Create basic frontend files
    echo -e "${YELLOW}Creating basic frontend files...${NC}"
    
    # Create package.json
    cat > frontend/package.json << 'EOF'
{
  "name": "fact-guard",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "@tailwindcss/forms": "^0.5.7",
    "tailwindcss": "^3.4.1",
    "animate.css": "^4.1.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
EOF
fi

# Create necessary Python package files
for dir in backend/app{,/api,/core,/models,/services}; do
    touch "$dir/__init__.py"
    echo -e "${GREEN}Created $dir/__init__.py${NC}"
done

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << 'EOF'
# Backend
OPENAI_API_KEY=your_api_key
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Frontend
REACT_APP_API_URL=http://localhost:8000
EOF
    echo -e "${GREEN}Created .env file${NC}"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo -e "${YELLOW}Creating .gitignore file...${NC}"
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.env

# Node
node_modules/
/frontend/build
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo
EOF
    echo -e "${GREEN}Created .gitignore file${NC}"
fi

echo -e "${GREEN}Project structure setup completed!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
echo -e "2. cd frontend && npm install"
echo -e "3. Update .env file with your OpenAI API key"
echo -e "4. Start development servers:"
echo -e "   - Backend: cd backend && uvicorn main:app --reload"
echo -e "   - Frontend: cd frontend && npm start" 