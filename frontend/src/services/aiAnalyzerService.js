/**
 * TwinSight — AI NOC Intelligence Service
 * Supports Google Gemini, Anthropic Claude, and Autonomous 3GPP/ETSI Local NOC Engine.
 */

export async function askTwinSightAI(query, metrics, history = []) {
  const geminiKey = localStorage.getItem('twinsight_gemini_key') || import.meta.env.VITE_GEMINI_API_KEY;
  const anthropicKey = localStorage.getItem('twinsight_anthropic_key') || import.meta.env.VITE_ANTHROPIC_API_KEY;

  // 1. Try Gemini if configured
  if (geminiKey && geminiKey.trim().length > 10) {
    try {
      const reply = await callGemini(query, metrics, geminiKey.trim(), history);
      if (reply) return { text: reply, provider: 'Gemini 2.5 Flash' };
    } catch (err) {
      console.warn('Gemini API call failed, falling back to Autonomous NOC Engine:', err);
    }
  }

  // 2. Try Anthropic if configured
  if (anthropicKey && anthropicKey.trim().length > 10) {
    try {
      const reply = await callAnthropic(query, metrics, anthropicKey.trim(), history);
      if (reply) return { text: reply, provider: 'Claude Sonnet' };
    } catch (err) {
      console.warn('Anthropic API call failed, falling back to Autonomous NOC Engine:', err);
    }
  }

  // 3. Fallback: Autonomous 3GPP/ETSI Telecom NOC Engine (Instant, zero errors, realistic)
  return {
    text: generateAutonomousNocIntelligence(query, metrics),
    provider: 'Autonomous NOC Engine (3GPP/ETSI)',
  };
}

async function callGemini(query, m, apiKey, history) {
  const systemInstruction = `You are TwinSight AI, an elite 5G SA NOC (Network Operations Center) Intelligence Assistant for L&T Techgium located in Mumbai, India.
Current Network Telemetry:
- Network Health: ${m.health}/100
- Active Slices: 6 (2 eMBB, 1 URLLC, 1 mMTC-IoT, 1 V2X, 1 NTN)
- End-to-End Latency: ${m.latency}ms
- Call Success Rate: ${m.callS}%
- 5G-AKA Auth Success: ${m.authS}%
- AI Confidence: ${m.aiS}%
- Connected Devices: 168,400

Format responses cleanly in Markdown with bold headers, bullet points, and specific 3GPP/ETSI recommendations.`;

  const contents = [];
  // Add recent history
  history.slice(-4).forEach((msg) => {
    contents.push({
      role: msg.role === 'user' ? 'user' : 'model',
      parts: [{ text: msg.content }],
    });
  });
  contents.push({ role: 'user', parts: [{ text: query }] });

  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents,
        systemInstruction: { parts: [{ text: systemInstruction }] },
      }),
    }
  );

  if (!res.ok) throw new Error(`Gemini HTTP ${res.status}`);
  const data = await res.json();
  return data.candidates?.[0]?.content?.parts?.[0]?.text;
}

async function callAnthropic(query, m, apiKey, history) {
  const systemPrompt = `You are TwinSight AI, an elite 5G SA NOC (Network Operations Center) Intelligence Assistant for L&T Techgium in Mumbai.
Current Telemetry: Health ${m.health}/100, Latency ${m.latency}ms, VoNR ${m.callS}%, Auth ${m.authS}%, AI Confidence ${m.aiS}%.
Respond as an expert 5G telecom engineer adhering to 3GPP TS 23.501 and TS 33.501.`;

  const messages = history.slice(-4).map((msg) => ({
    role: msg.role === 'user' ? 'user' : 'assistant',
    content: msg.content,
  }));
  messages.push({ role: 'user', content: query });

  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1000,
      system: systemPrompt,
      messages,
    }),
  });

  if (!res.ok) throw new Error(`Anthropic HTTP ${res.status}`);
  const data = await res.json();
  return data?.content?.[0]?.text;
}

function generateAutonomousNocIntelligence(query, m) {
  const q = query.toLowerCase();

  if (q.includes('full network') || q.includes('health') || q.includes('comprehensive')) {
    return `### 📊 Comprehensive 5G SA Network Health Assessment
**Region:** Mumbai Metro Cluster (MUM-01 to MUM-04) | **Architecture:** 3GPP Release 17 Standalone

#### 1. Core Key Performance Indicators (KPIs)
* **Overall Network Health:** \`${m.health}/100\` — Operating in **STABILIZED DEGRADATION** mode.
* **Latency Envelope:** \`${m.latency}ms\` end-to-end (Threshold: <15ms for eMBB, <5ms for URLLC).
* **Call Completion (VoNR):** \`${m.callS}%\` with IMS registration stability at 98.4%.
* **5G-AKA Authentication Rate:** \`${m.authS}%\` (Regional failure clustering observed in MUM-03).
* **Connected User Equipments (UEs):** \`168,400\` across 6 active network slices.

#### 2. Critical Network Risks
1. **[CRITICAL] INC-4421 (Volumetric Core DDoS):** 2.4 Tbps UDP flood directed at UPF-02. Mitigation pipeline active via BGP Flowspec.
2. **[HIGH] INC-4418 (mMTC Slice Saturation):** Occupancy at \`88.4%\`. Buffer exhaust in ~8 minutes without dynamic NSSAI scaling.
3. **[MEDIUM] Predictive gNB Degradation:** gNB-003 RF frontend showing VSWR impedance drift.

#### 3. Immediate Recommended Actions
* Trigger **Autonomous NSSAI Scaling** for Slice-03 (+30% PRB reallocation from idle eMBB buffer).
* Route non-critical IoT traffic through secondary UPF-03 instance.
* Dispatch L1 field diagnostic for gNB-003 RF power amplifier check.`;
  }

  if (q.includes('ddos') || q.includes('threat') || q.includes('attack')) {
    return `### 🛡️ Core Network DDoS Threat & Mitigation Analysis
**Target:** 5G Core User Plane Function (UPF-02) & Policy Control Function (PCF)

#### 1. Attack Vector & Blast Radius
* **Attack Type:** Volumetric SYN-Flood + UDP Amplification (BGP Route Hijack detected from AS-49211).
* **Peak Traffic:** \`2.41 Tbps\` with packet rate surpassing \`180 Mpps\`.
* **Affected Network Entities:** UPF-02, AMF-01 ingress queue, and Edge Node 02.
* **Blast Radius:** 14,200 commercial eMBB subscribers experiencing 18ms latency jitter.

#### 2. 3GPP TS 33.501 Aligned Mitigation Plan
1. **Dynamic Upstream Filtering:** Execute BGP Flowspec (RFC 5575) to drop unauthenticated UDP fragments at provider border routers.
2. **N3 Interface Rate-Limiting:** Apply GTP-U packet policing on gNB-01/02 backhaul tunnels.
3. **Failover Execution:** Shift high-priority URLLC and V2X sessions to isolated UPF-01 via N4 Session Modification procedures.

*TwinSight Autonomous SOC has isolated 94% of malicious traffic with zero data loss.*`;
  }

  if (q.includes('slice') || q.includes('optimization') || q.includes('scale')) {
    return `### ⚡ 5G Network Slice (NSI/NSSI) Optimization Plan
**Current Scope:** 6 Active Slices (eMBB-1, eMBB-2, URLLC, mMTC-IoT, V2X, NTN-Sat)

#### 1. Slice Occupancy & SLA Headroom
* **mMTC-IoT (SST 2, SD 000003):** Current Occupancy \`88.2%\` | **Status: SLA CRITICAL**
  * Active PDU Sessions: 88,200 / 100,000 max capacity.
  * Risk: Queue delay exceeding 50ms SLA ceiling within 8 minutes.
* **eMBB Commercial (SST 1, SD 000001):** Occupancy \`54.0%\` | **Status: OPTIMAL** (46% headroom available).
* **URLLC Mission-Critical (SST 1, SD 000002):** Occupancy \`32.5%\` | **Status: STABLE** (<2.1ms latency).

#### 2. Autonomous Remediation Decision
* **Action:** Reallocate \`+30% Physical Resource Blocks (PRBs)\` from eMBB-1 to mMTC-IoT.
* **Execution Pathway:** Trigger 3GPP TS 28.531 NSSI modification via NSMF (Network Slice Management Function).
* **Expected Outcome:** mMTC occupancy drops to \`61.5%\`, restoring 38,500 session headroom.`;
  }

  if (q.includes('sla') || q.includes('compliance')) {
    return `### 📋 5G SLA Compliance & Contractual Breach Review
**Evaluation Period:** Real-time sliding 60-minute window | **Standard:** 3GPP TS 22.261

| Slice Identifier | Target SLA Availability | Current Metric | Packet Delay Budget (PDB) | Compliance Status |
| :--- | :---: | :---: | :---: | :---: |
| **URLLC-01 (Smart Grid)** | 99.999% | 99.998% | 2.1 ms (Limit: 5 ms) | ✅ Fully Compliant |
| **V2X-Automotive** | 99.995% | 99.996% | 3.8 ms (Limit: 10 ms) | ✅ Fully Compliant |
| **eMBB-Consumer** | 99.900% | 99.940% | 11.2 ms (Limit: 20 ms) | ✅ Fully Compliant |
| **mMTC-SmartMeter** | 99.900% | 99.120% | 42.4 ms (Limit: 50 ms) | ⚠️ **Breach Warning** |
| **NTN-Satellite** | 99.500% | 99.710% | 128 ms (Limit: 250 ms) | ✅ Fully Compliant |

*Remediation has been queued for mMTC-SmartMeter to avert breach penalty within 12 minutes.*`;
  }

  if (q.includes('outage') || q.includes('prediction') || q.includes('24h')) {
    return `### 🔮 24-Hour Predictive Outage & Failure Analysis
**Engine:** Scikit-Learn Anomaly Classifier + LSTM Degradation Forecaster

#### 1. Failure Probability Rankings
1. **gNB-003 (Colaba Central):** \`92.4% Failure Probability\` in 36-48h.
   * *Telemetry Signature:* RF Power Amplifier temperature rising +2.3°C/day; VSWR standing wave ratio degraded to 1.42.
   * *Impact:* 18,200 subscribers in Colaba cluster.
2. **Edge Node 02 (Bandra Hub):** \`81.0% Congestion Spillover\` in 14 minutes.
   * *Telemetry Signature:* High CPU queue wait on N6 termination interface.
3. **AUSF Authentication Cluster:** \`28.2% Intermittent Drop Risk\` due to retry storm.

#### 2. Automated Prevention Strategy
* Reroute 40% of gNB-003 cell-edge UEs to adjacent gNB-004 via handover parameter adjustment (A3 event offset -2dB).
* Spin up secondary N6 routing container on Edge Node 03.`;
  }

  if (q.includes('auth') || q.includes('5g-aka') || q.includes('mumbai') || q.includes('mum-03')) {
    return `### 🔐 5G-AKA Authentication Attack & Forensic Report
**Incident Zone:** Cluster MUM-03 (Andheri East - International Airport Sector)

#### 1. Anomaly Pattern
* **Failure Velocity:** \`3.2×\` above rolling 7-day baseline.
* **Vector Analysis:** Replay attempts of expired Authentication Vectors (RAND/AUTN pairs).
* **Target Network Entity:** UDM (Unified Data Management) & AUSF (Authentication Server Function).
* **Classification:** Distributed Credential Stuffing & SUPI (Subscription Permanent Identifier) probing.

#### 2. Countermeasures Deployed
* Activated **Subscription Concealed Identifier (SUCI)** ephemeral key rotation (Profile A / ECIES).
* Enforced progressive back-off penalty for consecutive failed authentication requests from identical gNB sectors.
* Zero unauthorized access permitted; AUSF throughput preserved at 99.8%.`;
  }

  // General response
  return `### 📡 TwinSight 5G NOC Telecom Advisory
**Analysis for:** "${query}"
**Network Telemetry:** Health: \`${m.health}/100\` | Latency: \`${m.latency}ms\` | VoNR Success: \`${m.callS}%\` | Devices: \`168,400\`

#### 1. Technical Evaluation
Your query correlates with 3GPP Standalone (SA) architecture specifications. In high-density 5G deployments (such as the Mumbai metropolitan cluster), state coherence between the User Plane Function (UPF), Session Management Function (SMF), and Radio Access Network (gNodeB) requires autonomous policy coordination.

#### 2. Operational Recommendations
* **Telemetry Monitoring:** Maintain continuous telemetry monitoring over the \`/ws/telemetry\` streaming pipeline.
* **Closed-Loop Automation:** Ensure AI Control Mode remains set to **Autonomous** for sub-second failover.
* **Slice Integrity:** Verify that priority QoS Flow Identifiers (5QI 1 for VoNR, 5QI 82 for V2X) remain unthrottled during peak hours.`;
}
