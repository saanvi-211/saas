# AI-Powered SaaS Automation Platform

A multi-tenant SaaS platform with JWT auth, role-based dashboards & modular API-driven workflows.

## Tech Stack
- **Backend**: Python, FastAPI, MongoDB, JWT
- **Frontend**: React, TypeScript
- **Auth**: JWT + Role-based access control

## Features
- Multi-tenant architecture
- JWT authentication with role-based dashboards
- Async FastAPI microservices with background task execution
- MongoDB aggregation pipelines for analytics
- Reusable React + TypeScript components

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Structure
```
saas-platform/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── core/         # Config, security
│   │   ├── models/       # Pydantic models
│   │   └── services/     # Business logic
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/   # Reusable UI components
    │   ├── pages/        # Page-level components
    │   ├── hooks/        # Custom React hooks
    │   └── utils/        # Helpers & API client
    └── package.json
```
