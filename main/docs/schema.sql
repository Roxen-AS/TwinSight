-- ═══════════════════════════════════════════════════════════════
-- TwinSight — PostgreSQL Schema
-- AI-Powered Digital Twin for 5G Network Management
-- ═══════════════════════════════════════════════════════════════

-- Users & Auth
CREATE TABLE IF NOT EXISTS users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) UNIQUE NOT NULL,
    name        VARCHAR(255) NOT NULL,
    role        VARCHAR(50) DEFAULT 'noc_engineer',
    region      VARCHAR(100),
    hashed_pw   TEXT NOT NULL,
    is_active   BOOLEAN DEFAULT TRUE,
    last_login  TIMESTAMPTZ,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Network Slices
CREATE TABLE IF NOT EXISTS slices (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slice_id      VARCHAR(50) UNIQUE NOT NULL,
    name          VARCHAR(255) NOT NULL,
    type          VARCHAR(20) NOT NULL CHECK (type IN ('eMBB','URLLC','mMTC','V2X','NTN')),
    status        VARCHAR(20) DEFAULT 'active',
    occupancy_pct NUMERIC(5,2) DEFAULT 0,
    throughput    VARCHAR(50),
    latency_ms    NUMERIC(8,2),
    active_users  INTEGER DEFAULT 0,
    sla_target    NUMERIC(6,3) DEFAULT 99.0,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Telemetry (time-series)
CREATE TABLE IF NOT EXISTS telemetry (
    id                  BIGSERIAL PRIMARY KEY,
    timestamp           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    network_health      NUMERIC(5,2),
    avg_latency_ms      NUMERIC(8,2),
    call_success_rate   NUMERIC(6,3),
    auth_success_rate   NUMERIC(6,3),
    connected_devices   INTEGER,
    uplink_gbps         NUMERIC(8,2),
    downlink_gbps       NUMERIC(8,2),
    threat_score        SMALLINT
);
CREATE INDEX IF NOT EXISTS idx_telemetry_ts ON telemetry(timestamp DESC);

-- Incidents
CREATE TABLE IF NOT EXISTS incidents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id     VARCHAR(20) UNIQUE NOT NULL,
    title           TEXT NOT NULL,
    severity        VARCHAR(20) NOT NULL CHECK (severity IN ('critical','high','medium','low')),
    status          VARCHAR(30) DEFAULT 'active',
    ai_handled      BOOLEAN DEFAULT FALSE,
    root_cause      TEXT,
    resolution      TEXT,
    detected_at     TIMESTAMPTZ DEFAULT NOW(),
    resolved_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Threats
CREATE TABLE IF NOT EXISTS threats (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    threat_id   VARCHAR(20) UNIQUE NOT NULL,
    type        VARCHAR(50) NOT NULL,
    severity    VARCHAR(20) NOT NULL,
    origin      TEXT,
    target      TEXT,
    risk_score  SMALLINT,
    status      VARCHAR(30) DEFAULT 'active',
    detected_at TIMESTAMPTZ DEFAULT NOW(),
    mitigated_at TIMESTAMPTZ
);

-- AI Predictions
CREATE TABLE IF NOT EXISTS predictions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name      VARCHAR(100) NOT NULL,
    prediction_type VARCHAR(100) NOT NULL,
    input_data      JSONB,
    output_value    NUMERIC(8,4),
    confidence_pct  NUMERIC(5,2),
    threshold       NUMERIC(8,4),
    breached        BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Digital Twin State
CREATE TABLE IF NOT EXISTS twin_state (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp   TIMESTAMPTZ DEFAULT NOW(),
    sync_pct    NUMERIC(5,2) DEFAULT 100,
    sim_mode    VARCHAR(50) DEFAULT 'normal',
    ai_active   BOOLEAN DEFAULT FALSE,
    node_states JSONB DEFAULT '{}',
    edge_states JSONB DEFAULT '{}'
);

-- Reports
CREATE TABLE IF NOT EXISTS reports (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_type     VARCHAR(20) NOT NULL CHECK (report_type IN ('daily','weekly','monthly')),
    status          VARCHAR(20) DEFAULT 'generating',
    format          VARCHAR(10),
    file_path       TEXT,
    generated_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- API Keys
CREATE TABLE IF NOT EXISTS api_keys (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(255) NOT NULL,
    key_hash    TEXT NOT NULL UNIQUE,
    permissions VARCHAR(50) DEFAULT 'read',
    is_active   BOOLEAN DEFAULT TRUE,
    user_id     UUID REFERENCES users(id),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    last_used   TIMESTAMPTZ
);

-- Seed data
INSERT INTO slices (slice_id, name, type, occupancy_pct, throughput, latency_ms, active_users, sla_target)
VALUES
  ('sl1','eMBB-Enterprise',  'eMBB',  72.0, '12.4 Gbps', 8.0,   4821,   99.7),
  ('sl2','URLLC-Industrial', 'URLLC', 45.0, '2.1 Gbps',  1.2,   312,    99.99),
  ('sl3','mMTC-IoT',         'mMTC',  88.0, '820 Mbps',  48.0,  142000, 98.2),
  ('sl4','eMBB-Consumer',    'eMBB',  61.0, '8.2 Gbps',  12.0,  18400,  99.1),
  ('sl5','V2X-Automotive',   'V2X',   33.0, '1.5 Gbps',  0.8,   890,    99.99),
  ('sl6','NTN-Satellite',    'NTN',   19.0, '400 Mbps',  600.0, 2100,   97.8)
ON CONFLICT (slice_id) DO NOTHING;
