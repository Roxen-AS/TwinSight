# TwinSight ⚡

### AI-Powered Digital Twin for Autonomous 5G Network Management

> Enterprise-grade NOC Intelligence Platform for L&T Techgium | 5G/6G Ready

[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![3GPP](https://img.shields.io/badge/3GPP-Release_17_SA-blue)](https://www.3gpp.org/)
[![License](https://img.shields.io/badge/License-Proprietary-emerald)](LICENSE)

---

## Overview

TwinSight is a full-stack AI-powered Digital Twin platform providing real-time autonomous management of 5G network infrastructure. It combines Digital Twins, Predictive Analytics, AI-driven anomaly detection, and autonomous orchestration into a self-healing network management ecosystem.

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
| **AI Analyzer** 🤖 | Multi-engine NOC intelligence (Autonomous 3GPP Engine, Gemini 2.5 Flash, Claude) |
| **Incidents** | ITIL-aligned lifecycle, RCA, autonomous recovery queue |
| **Reports** | Daily/Weekly/Monthly with PDF/CSV/Excel export |
| **Settings** | User management, API keys, AI provider configuration |

---

## Tech Stack

### Frontend
- **React 18** + **Vite** — ultra-fast development & production bundling
- **Recharts** — real-time responsive data visualizations
- **Lucide React** — NOC icons
- **TailwindCSS** — utility-first dark cyberpunk styling
- **Space Grotesk** + **Rajdhani** + **JetBrains Mono** — telemetry typography

### Backend
- **FastAPI** — async Python API with WebSocket support
- **PostgreSQL** — primary database
- **Redis** — caching & pub/sub
- **SQLAlchemy** + **Alembic** — ORM & migrations

### AI Layer
- **Autonomous 3GPP/ETSI NOC Engine** — built-in offline intelligence engine with zero setup
- **Google Gemini 2.5 Flash & Anthropic Claude** — multi-provider LLM support with live API keys
- **Scikit-learn** — anomaly detection & degradation forecasting
- **PyTorch** — deep learning ready architecture

### DevOps
- **Docker** + **Docker Compose** — containerized deployment
- **Vercel** — instant frontend deployment support
- **Nginx** — reverse proxy & static file serving

---

## Quick Start

### Option A — Standalone Frontend (Recommended for Demo)

Run TwinSight directly in your browser — zero backend required.

```bash
# 1. Clone repository
git clone https://github.com/Roxen-AS/TwinSight.git
cd TwinSight/frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# Open http://localhost:3000
# Login with any credentials
```

The frontend includes full mock data, simulated real-time updates, and an autonomous AI NOC analyzer with optional Gemini/Claude API key integration.

### Option B — Full Stack with Docker

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Start all services
docker-compose up -d

# Services:
#   Frontend:  http://localhost:3000
#   Backend:   http://localhost:8000
#   API Docs:  http://localhost:8000/api/docs
#   PgAdmin:   http://localhost:5432 (via psql)
```

### Option C — Backend Only

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --port 8000

# API Docs: http://localhost:8000/api/docs
```

---

## Project Structure

```
TwinSight/
├── frontend/
│   ├── src/
│   │   ├── services/
│   │   │   └── aiAnalyzerService.js   ← Multi-provider AI NOC engine
│   │   ├── TwinSight.jsx             ← Main application (all 11 pages)
│   │   ├── main.jsx                  ← React entry point
│   │   └── index.css                 ← Global styles + animations
│   ├── public/
│   │   └── favicon.svg
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── vercel.json
│   └── Dockerfile
│
├── backend/
│   ├── main.py                       ← FastAPI app + WebSocket broadcaster
│   ├── routers/
│   │   ├── dashboard.py              ← KPIs, traffic, radar
│   │   ├── slices.py                 ← NSI/NSSI CRUD + actions
│   │   ├── callflow.py               ← VoNR analytics
│   │   ├── auth.py                   ← Auth risk analytics
│   │   ├── security.py               ← SOC, threats, DDoS
│   │   ├── twin.py                   ← Digital twin state + simulation
│   │   ├── ai_control.py             ← AI predictions + mode control
│   │   ├── incidents.py              ← Incident lifecycle
│   │   └── reports.py                ← Report generation
│   ├── requirements.txt
│   └── Dockerfile
│
├── docs/
│   └── schema.sql                    ← Complete PostgreSQL schema
│
├── docker-compose.yml
├── .env.example
├── vercel.json
└── README.md
```

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

## 👤 Author

Developed for **L&T Techgium** by [**Roxen-AS**](https://github.com/Roxen-AS).
