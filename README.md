# TwinSight 

### AI-Powered Digital Twin for Autonomous 5G Network Management

> Enterprise-grade NOC Intelligence Platform for L&T Techgium | 5G/6G Ready

---

## Overview

TwinSight is a full-stack AI-powered Digital Twin platform that provides real-time autonomous management of 5G network infrastructure. It combines Digital Twins, Predictive Analytics, AI-driven anomaly detection, and autonomous orchestration into a self-healing network management ecosystem.

---

## Features

| Module | Description |
|---|---|
| **Dashboard** | Live KPIs, traffic charts, health radar, AI recommendations |
| **Network Slices** | NSI/NSSI lifecycle management (eMBB, URLLC, mMTC, V2X, NTN) |
| **Call Flow Analytics** | VoNR/IMS real-time call monitoring and failure analysis |
| **Authentication Center** | 5G-AKA risk analytics, heatmaps, regional risk assessment |
| **Security SOC** | DDoS detection, threat intelligence, global attack map |
| **Digital Twin** ⭐ | Live SVG network topology with animated simulation modes |
| **AI Control** | Autonomous/manual mode, prediction arcs, action queue |
| **AI Analyzer** 🤖 | Claude Sonnet-powered NOC intelligence chat interface |
| **Incidents** | ITIL-aligned lifecycle, RCA, autonomous recovery queue |
| **Reports** | Daily/Weekly/Monthly with PDF/CSV/Excel export |
| **Settings** | User management, API keys, integrations |

---

## Tech Stack

### Frontend
- **React 18** + **Vite** — fast development & build
- **Recharts** — all data visualizations
- **Lucide React** — icons
- **TailwindCSS** — utility-first styling
- **Space Grotesk** + **Rajdhani** + **JetBrains Mono** — typography

### Backend
- **FastAPI** — async Python API with WebSocket support
- **PostgreSQL** — primary database
- **Redis** — caching & pub/sub
- **SQLAlchemy** + **Alembic** — ORM & migrations

### AI Layer
- **Anthropic Claude Sonnet** — AI Analyzer (NOC intelligence chat)
- **Scikit-learn** — anomaly detection & prediction models
- **PyTorch** — deep learning ready architecture

### DevOps
- **Docker** + **Docker Compose** — containerized deployment
- **Nginx** — reverse proxy & static file serving

---

## Quick Start

### Option A — Standalone Frontend (Recommended for Demo)

The simplest way to run TwinSight — no backend required.

```bash
# 1. Clone / unzip the project
cd twinsight/frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# Open http://localhost:3000
# Login with any credentials
```

The frontend includes all mock data and simulated real-time updates. The AI Analyzer page connects to the Anthropic API directly from the browser.

### Option B — Full Stack with Docker

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Fill in your values (minimum: ANTHROPIC_API_KEY)
nano .env

# 3. Start all services
docker-compose up -d

# Services:
#   Frontend:  http://localhost:3000
#   Backend:   http://localhost:8000
#   API Docs:  http://localhost:8000/api/docs
#   PgAdmin:   http://localhost:5432 (via psql)
```

### Option C — Backend Only

```bash
cd twinsight/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp ../.env.example .env

# Run server
uvicorn main:app --reload --port 8000

# API Docs: http://localhost:8000/api/docs
```

---

## Project Structure

```
twinsight/
├── frontend/
│   ├── src/
│   │   ├── TwinSight.jsx       ← Main application (all 11 pages)
│   │   ├── main.jsx            ← React entry point
│   │   └── index.css           ← Global styles + animations
│   ├── public/
│   │   └── favicon.svg
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── backend/
│   ├── main.py                 ← FastAPI app + WebSocket broadcaster
│   ├── routers/
│   │   ├── dashboard.py        ← KPIs, traffic, radar
│   │   ├── slices.py           ← NSI/NSSI CRUD + actions
│   │   ├── callflow.py         ← VoNR analytics
│   │   ├── auth.py             ← Auth risk analytics
│   │   ├── security.py         ← SOC, threats, DDoS
│   │   ├── twin.py             ← Digital twin state + simulation
│   │   ├── ai_control.py       ← AI predictions + mode control
│   │   ├── incidents.py        ← Incident lifecycle
│   │   └── reports.py          ← Report generation
│   ├── requirements.txt
│   └── Dockerfile
│
├── docs/
│   └── schema.sql              ← Complete PostgreSQL schema
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## API Reference

Full interactive docs: **http://localhost:8000/api/docs**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | System health check |
| GET | `/api/dashboard/metrics` | Live network KPIs |
| GET | `/api/dashboard/traffic` | 24h traffic timeseries |
| GET | `/api/slices/` | List all network slices |
| POST | `/api/slices/{id}/action` | Scale/pause/fail/heal slice |
| GET | `/api/security/threats` | Active threat intelligence |
| GET | `/api/ai/predictions` | AI probability predictions |
| POST | `/api/twin/simulate` | Trigger simulation mode |
| WS | `/ws/telemetry` | Live telemetry stream |

---

## Digital Twin Simulation Modes

| Mode | Affected Nodes | Description |
|---|---|---|
| `normal` | All green | Baseline operation |
| `congestion` | Edge-01, gNB-01/02 | Traffic congestion simulation |
| `ddos` | Core, PCF, Edge-02 | DDoS attack simulation |
| `authfail` | EPC, Edge-01/03 | Authentication failure cascade |
| `overload` | EPC, Edge-03, gNB-05/06 | Slice overload scenario |

Activate **AI Recovery** to watch autonomous healing animate across all affected nodes.

---

## AI Analyzer

The AI Analyzer uses **Claude Sonnet** to provide real-time NOC intelligence. It has full context of the current network state (metrics, incidents, threats, slice status) and can:

- Perform comprehensive network health analysis
- Assess DDoS threats with 3GPP-aligned mitigation strategies
- Recommend slice scaling with capacity calculations
- Review SLA compliance and breach risks
- Predict 24h outage probabilities
- Analyze authentication attack patterns

The Anthropic API is called directly from the browser — ensure `ANTHROPIC_API_KEY` is configured.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | ✓ | For AI Analyzer feature |
| `DATABASE_URL` | Backend only | PostgreSQL connection string |
| `REDIS_URL` | Backend only | Redis connection string |
| `JWT_SECRET` | Backend only | JWT signing secret |

---

## Deployment

### Production Build

```bash
# Frontend
cd frontend
npm run build
# Output: frontend/dist/

# Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Production

```bash
ENVIRONMENT=production docker-compose up -d --build
```

---

## License

Built for **L&T Techgium** — Enterprise 5G Network Intelligence Platform.

---

*TwinSight v1.0.0 — Designed with ♦ for the future of autonomous 5G networks*
