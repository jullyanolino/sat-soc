# 🛰️ Aerospace Engineering & Satellite Cybersecurity SOC Dashboard

A **unified, interactive, research-grade dashboard** built with **Streamlit**, combining:

- **Aerospace Engineering Principles**  
- **Satellite Dynamics & 3D Orbit Visualization**  
- **RF Link Budget Exploration**  
- **Statistical Orbital Analysis**  
- **A Prototype Satellite-Focused Cybersecurity SOC**  
- **Threat Intelligence + Hunting Playbooks + MITRE-like Matrix**  

This project is ideal for:
- Aerospace engineers  
- Cybersecurity analysts  
- Threat hunters  
- Space mission architects  
- Researchers working on **space security**, **satellite resilience**, and **dual-domain analysis**  

---

## 🚀 Overview

The dashboard provides **two main tabs**:

---

## **1️⃣ Satellite Engineering Lab**

A hands-on environment to explore:

### **🔭 Orbital Mechanics**
- Adjustable altitude, inclination, and eccentricity  
- Automatic computation of orbital period and velocity  
- Sweep analysis to visualize physical relationships:
  - **Altitude × Period**
  - **Altitude × Velocity**

### **🌍 Stunning 3D Orbit Visualization**
- Realistic Earth model (spherical approximation)  
- Satellite orbit path  
- Interactive rotation/zoom with Plotly  

### **📡 Link Budget (Toy Model)**
Tunables include:
- EIRP  
- Path Loss  
- Antenna Gains  
- System Losses  
- Noise Figure  

Instant **C/N₀** feedback for conceptual RF analysis.

### **🏗️ Infrastructure Context**
Short descriptions of:
- Launch segment  
- Space segment  
- Ground segment  
- Link architecture  

To contextualize the cybersecurity tab.

---

## **2️⃣ Satellite Cyber SOC Prototype**

A full mini-SOC console tailored for **space systems**.

### **🛡️ Threat Intelligence Layer**
Synthetic but realistic threats such as:
- GNSS spoofing  
- Uplink jamming  
- Ground station intrusion  
- Satellite bus exploitation  

Automatic classification by **CIA impact dimensions**.

### **🔥 Risk Analytics**
- Risk heatmap (Likelihood × Impact)  
- Boxplots comparing risk across CIA dimensions  
- High-risk filtering  
- Segment selection:
  - Space Segment  
  - Ground Segment  
  - Link Segment  

### **🧰 MITRE-Inspired Matrix for Space**
A simplified detection/coverage matrix:
- Reconnaissance → Impact  
- Techniques mapped with coverage levels  
- Heatmap visualization  

### **🔍 Hunting Playbook**
A structured example focused on:
- GNSS spoofing  
- RF anomalies  
- Command injection attempts  
- Telemetry deviations  
- Correlations between RF, orbit, and authentication data  

Built to be easily extended into a fully operational huntbook.

---

## 🧩 Architecture

```

app.py
├─ Satellite Engineering Tab
│   ├─ Orbital mechanics engine
│   ├─ Link budget estimation
│   ├─ 3D orbit visualization
│   └─ Sweep analysis & statistics
│
└─ Satellite Cyber SOC Tab
├─ Threat modeling & scoring
├─ Risk heatmaps and CIA scoring
├─ MITRE-like space matrix
└─ Hunting & detection logic

````

The code is modular and can easily be integrated with:
- Real TLEs (`sgp4`)
- Real threat intel feeds  
- Telemetry logs  
- SIEM exports  
- Space situational awareness tools  

---

## 🛠️ Installation

### **1. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate          # Windows
````

### **2. Install dependencies**

```bash
pip install -r requirements.txt
```

### **3. Run the dashboard**

```bash
streamlit run app.py
```

---

## 📡 How to Extend

### **Aerospace side**

* Add SGP4 orbital propagation
* Insert real mission profiles
* Add environmental perturbations (J2, drag)
* Simulate ground station passes

### **Cyber side**

* Integrate with SIEM (Elastic, Splunk, OpenSearch)
* Map to real satellite standards (NIST 800-160, CCSDS security)
* Add RF anomaly detection models
* Inject real threat feeds (MISP, STIX/TAXII)

---

## 🏁 Roadmap

* [ ] Multi-satellite constellations (e.g., Walker, Starlink-like)
* [ ] Constellation-wide risk propagation model
* [ ] Time-series anomaly detection (telemetry + RF + IT logs)
* [ ] Zero-Trust architecture modeling for ground stations
* [ ] Replay + simulation engine for cyber-attack scenarios

---

## 💡 Why this project matters

Space systems are inherently **dual-domain**:
they require **precision engineering** and **ruthless cybersecurity**.

This dashboard gives you:

* A physics-accurate sandbox
* A SOC-style analytic engine
* A unified view of **space mission assurance**

Perfect for **research, presentations, teaching, and experimentation**.

---

## 🧑‍🚀 Author & Contact

If you need help extending this to:

* PQC-protected satellite links
* QKD over space channels
* RF anomaly detection
* Digital twins for spacecraft

Just call.
We can push this into **mission-grade territory** together.

````

---

# ✅ **requirements.txt**

This includes only what the current dashboard needs.

```txt
streamlit
plotly
pandas
numpy
````

