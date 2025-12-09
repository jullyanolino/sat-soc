import streamlit as st
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------------
# Helper functions – AEROSPACE ENGINEERING (SATELLITES)
# ----------------------------------------------------------

MU_EARTH = 3.986004418e14  # [m^3/s^2]
R_EARTH = 6_371_000        # [m]

def kepler_period(semi_major_axis_m: float) -> float:
    """Orbital period [s] for circular orbit with semi-major axis a."""
    return 2 * np.pi * np.sqrt(semi_major_axis_m**3 / MU_EARTH)

def orbital_velocity(semi_major_axis_m: float) -> float:
    """Orbital velocity [m/s] for circular orbit with semi-major axis a."""
    return np.sqrt(MU_EARTH / semi_major_axis_m)

def generate_orbit_3d(altitude_km: float, points: int = 400):
    r = R_EARTH + altitude_km * 1000
    theta = np.linspace(0, 2 * np.pi, points)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros_like(theta)
    return x, y, z

def satellite_link_budget(eirp_dbw, path_loss_db, rx_gain_db, sys_loss_db, noise_figure_db):
    """Very simplified carrier-to-noise ratio estimate [dB]."""
    cn0_db = eirp_dbw - path_loss_db + rx_gain_db - sys_loss_db - noise_figure_db
    return cn0_db

# ----------------------------------------------------------
# Helper functions – CYBERSEC / SOC SIDE
# ----------------------------------------------------------

def generate_mock_sat_threat_data():
    np.random.seed(42)
    threats = [
        "GNSS Spoofing",
        "Uplink Jamming",
        "Downlink Jamming",
        "Ground Station Intrusion",
        "Supply Chain Malware",
        "Sat Bus Exploit",
        "Command Injection",
        "Data Exfiltration",
        "Ransomware in Ground IT",
        "Insider Threat",
    ]

    cia_dim = ["Confidentiality", "Integrity", "Availability"]
    rows = []
    for t in threats:
        for dim in cia_dim:
            rows.append({
                "Threat": t,
                "CIA": dim,
                "Likelihood": np.random.randint(1, 5),
                "Impact": np.random.randint(1, 5),
            })
    df = pd.DataFrame(rows)
    df["RiskScore"] = df["Likelihood"] * df["Impact"]
    return df

def generate_mitre_like_matrix():
    tactics = [
        "Reconnaissance", "Initial Access", "Execution", "Persistence",
        "Command & Control", "Impact"
    ]
    techniques = [
        "RF Scanning",
        "Phishing Ground Staff",
        "SATCOM Protocol Abuse",
        "Backdoor in Ground SW",
        "C2 via Compromised GS",
        "Orbit/Attitude Manipulation",
    ]
    data = []
    for t in tactics:
        for tech in techniques:
            data.append({
                "Tactic": t,
                "Technique": tech,
                "Coverage": np.random.choice(["None", "Partial", "Good"]),
            })
    return pd.DataFrame(data)

# ----------------------------------------------------------
# UI CONFIG
# ----------------------------------------------------------

st.set_page_config(
    page_title="Aerospace & Satellite Cybersecurity Lab",
    layout="wide",
)

st.title("🛰️ Aerospace Engineering & Satellite Cybersecurity SOC")

tab1, tab2 = st.tabs([
    "🛰️ Satellite Engineering Lab",
    "🛡️ Satellite Cyber SOC Prototype",
])

# ----------------------------------------------------------
# TAB 1 – AEROSPACE ENGINEERING
# ----------------------------------------------------------

with tab1:
    st.header("Satellite Engineering Principles")

    st.markdown(
        """
This tab lets you **play with realistic orbital parameters**, see how they affect
**orbits, velocity, and link budget**, and visualize a **3D orbit** around Earth.
        """
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Orbital Parameters")

        altitude_km = st.slider(
            "Orbit altitude [km]",
            min_value=200,
            max_value=36_000,
            value=700,
            step=50,
            help="Approximate circular orbit altitude above Earth's surface.",
        )

        inclination_deg = st.slider(
            "Inclination [deg]",
            min_value=0,
            max_value=120,
            value=98,
            step=1,
            help="Inclination relative to Earth's equator.",
        )

        ecc = st.slider(
            "Eccentricity (simplified)",
            min_value=0.0,
            max_value=0.5,
            value=0.0,
            step=0.01,
            help="We will still treat orbit as near-circular for calculations.",
        )

        a = R_EARTH + altitude_km * 1000
        T = kepler_period(a)
        v = orbital_velocity(a)

        st.markdown("#### Key Orbital Outputs")
        st.metric("Orbital Period", f"{T/60:.1f} minutes")
        st.metric("Orbital Velocity", f"{v/1000:.2f} km/s")

        st.caption(
            "Using Kepler's 3rd law:  T = 2π√(a³/μ),  and v = √(μ/a), "
            "with μ ≈ 3.986×10¹⁴ m³/s²."
        )

    with col2:
        st.subheader("Simple Link Budget (Toy Model)")

        eirp_dbw = st.slider("Satellite EIRP [dBW]", 20.0, 70.0, 45.0, 1.0)
        path_loss_db = st.slider("Path Loss [dB]", 150.0, 220.0, 190.0, 1.0)
        rx_gain_db = st.slider("Ground Antenna Gain [dB]", 20.0, 60.0, 35.0, 1.0)
        sys_loss_db = st.slider("System Losses [dB]", 0.0, 10.0, 3.0, 0.5)
        noise_fig_db = st.slider("Noise Figure [dB]", 0.0, 10.0, 4.0, 0.5)

        cn0 = satellite_link_budget(
            eirp_dbw, path_loss_db, rx_gain_db, sys_loss_db, noise_fig_db
        )
        st.metric("Estimated C/N₀ [dB-Hz]", f"{cn0:.1f}")

        st.caption(
            "Toy model: C/N0 ≈ EIRP − PathLoss + G_rx − L_sys − NF. "
            "In a real design, you'd include bandwidth, temperature, "
            "modulation and coding, rain fade, etc."
        )

    st.markdown("---")
    st.subheader("3D Orbit Visualization")

    x, y, z = generate_orbit_3d(altitude_km)

    fig3d = go.Figure()

    # Earth (sphere approximation)
    u, v_angle = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
    xe = R_EARTH * np.cos(u) * np.sin(v_angle)
    ye = R_EARTH * np.sin(u) * np.sin(v_angle)
    ze = R_EARTH * np.cos(v_angle)

    fig3d.add_surface(
        x=xe, y=ye, z=ze,
        opacity=0.6,
        showscale=False,
    )

    # Orbit
    fig3d.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode="lines",
        name="Orbit",
    ))

    # Satellite at some point
    fig3d.add_trace(go.Scatter3d(
        x=[x[0]],
        y=[y[0]],
        z=[z[0]],
        mode="markers",
        marker=dict(size=4),
        name="Satellite",
    ))

    fig3d.update_layout(
        scene=dict(
            xaxis_title="x [m]",
            yaxis_title="y [m]",
            zaxis_title="z [m]",
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        height=600,
    )

    st.plotly_chart(fig3d, use_container_width=True)

    st.markdown("---")
    st.subheader("Parameter Sweep & Statistical View")

    st.markdown("Play with a sweep over altitudes and see how **period** changes.")

    sweep_min = st.slider("Sweep min altitude [km]", 200, 30_000, 300, 100)
    sweep_max = st.slider("Sweep max altitude [km]", sweep_min + 100, 36_000, 2000, 100)
    sweep_step = st.slider("Sweep step [km]", 100, 5_000, 500, 100)

    altitudes = np.arange(sweep_min, sweep_max + sweep_step, sweep_step)
    periods_min = []
    velocities_kms = []

    for alt in altitudes:
        a_sweep = R_EARTH + alt * 1000
        periods_min.append(kepler_period(a_sweep) / 60)
        velocities_kms.append(orbital_velocity(a_sweep) / 1000)

    df_orbit_stats = pd.DataFrame({
        "Altitude_km": altitudes,
        "Period_min": periods_min,
        "Velocity_km_s": velocities_kms,
    })

    col_a, col_b = st.columns(2)
    with col_a:
        fig_period = px.line(
            df_orbit_stats,
            x="Altitude_km",
            y="Period_min",
            title="Orbital Period vs Altitude",
        )
        st.plotly_chart(fig_period, use_container_width=True)

    with col_b:
        fig_vel = px.line(
            df_orbit_stats,
            x="Altitude_km",
            y="Velocity_km_s",
            title="Orbital Velocity vs Altitude",
        )
        st.plotly_chart(fig_vel, use_container_width=True)

    st.dataframe(df_orbit_stats.style.highlight_max(axis=0), use_container_width=True)

    st.markdown(
        """
**Facility / infrastructure notes (for context):**

- **Launch segment:** pads, integration facilities, fueling, safety systems.  
- **Space segment:** spacecraft bus, payloads, TT&C subsystem, power, thermal control.  
- **Ground segment:** mission control, ground antennas, network infrastructure, secure enclaves.  
- **Links:** uplink (command), downlink (telemetry & data), inter-satellite links (ISL).  

These are the “assets” you’ll map in the SOC tab.
        """
    )

# ----------------------------------------------------------
# TAB 2 – SATELLITE CYBER SOC PROTOTYPE
# ----------------------------------------------------------

with tab2:
    st.header("Satellite Cybersecurity SOC Prototype")

    st.markdown(
        """
Here we build a **toy SOC console** focused on **space systems**: satellites,
ground stations, RF links and mission networks.

You can:

- Explore **threats/vulnerabilities** mapped to **CIA**.
- See a **risk heatmap**.
- Inspect a minimal **MITRE-like matrix** for space operations.
- Filter by segment (space / ground / link) and tune a risk threshold.
        """
    )

    segment = st.selectbox(
        "Operational segment",
        ["All", "Space Segment", "Ground Segment", "Link Segment"],
    )

    risk_threshold = st.slider(
        "Minimum Risk Score for Highlight",
        min_value=1,
        max_value=16,
        value=9,
    )

    # Mock threat data
    df_threats = generate_mock_sat_threat_data()

    # Map segment to subset (just as an example)
    if segment == "Space Segment":
        mask = df_threats["Threat"].isin([
            "Sat Bus Exploit", "Command Injection", "Data Exfiltration"
        ])
        df_seg = df_threats[mask]
    elif segment == "Ground Segment":
        mask = df_threats["Threat"].isin([
            "Ground Station Intrusion", "Ransomware in Ground IT", "Insider Threat"
        ])
        df_seg = df_threats[mask]
    elif segment == "Link Segment":
        mask = df_threats["Threat"].isin([
            "GNSS Spoofing", "Uplink Jamming", "Downlink Jamming"
        ])
        df_seg = df_threats[mask]
    else:
        df_seg = df_threats.copy()

    high_risk = df_seg[df_seg["RiskScore"] >= risk_threshold]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Risk Heatmap (Likelihood x Impact)")

        # Aggregate counts
        heatmap_data = (
            df_seg.groupby(["Likelihood", "Impact"])
            .size()
            .reset_index(name="Count")
        )

        fig_heat = px.density_heatmap(
            heatmap_data,
            x="Likelihood",
            y="Impact",
            z="Count",
            nbinsx=4,
            nbinsy=4,
            title="Threat Density by Likelihood and Impact",
        )
        fig_heat.update_xaxes(dtick=1)
        fig_heat.update_yaxes(dtick=1)
        st.plotly_chart(fig_heat, use_container_width=True)

    with col2:
        st.subheader("Risk Distribution per CIA Dimension")

        fig_bar = px.box(
            df_seg,
            x="CIA",
            y="RiskScore",
            points="all",
            title="Risk Score per CIA Dimension",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### High-Risk Findings (Filtered)")
    st.dataframe(
        high_risk.sort_values("RiskScore", ascending=False),
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader("MITRE-like Coverage Matrix (Space-flavored)")

    df_mitre = generate_mitre_like_matrix()

    coverage_map = {"None": 0, "Partial": 1, "Good": 2}
    df_mitre["CoverageScore"] = df_mitre["Coverage"].map(coverage_map)

    pivot = df_mitre.pivot_table(
        index="Technique",
        columns="Tactic",
        values="CoverageScore",
        aggfunc="mean",
    )

    fig_cov = px.imshow(
        pivot,
        title="Detection/Prevention Coverage (0=None, 1=Partial, 2=Good)",
        aspect="auto",
    )
    st.plotly_chart(fig_cov, use_container_width=True)

    st.markdown(
        """
In a real SOC you would map these to frameworks like:

- **MITRE ATT&CK for Enterprise/ICS/Space (emerging)**  
- **NIST 800-53 / 800-172**, **NIST 800-160 Vol.2** (systems security engineering, including space)  
- **ESA / NASA / DoD space cybersecurity guidelines**  
- Satellite and ground network baselines (zero trust, network segmentation, RF monitoring).  
        """
    )

    st.markdown("---")
    st.subheader("Hunting Playbook Sketch (for you to refine)")

    st.markdown(
        """
**Example playbook: GNSS spoofing & link manipulation**

1. **Hypothesis**  
   - Adversary is manipulating GNSS signals or uplink commands to alter satellite attitude or orbit.

2. **Data Sources**  
   - Telemetry streams (attitude, propulsion, GNSS residuals).  
   - RF spectrum captures around GNSS and SATCOM bands.  
   - Ground station auth logs and admin activity.  
   - Network flow logs from mission control LAN.

3. **Detections**  
   - Anomalous delta-V or attitude maneuvers not in flight plan.  
   - GNSS position residuals exceeding threshold over sliding window.  
   - RF anomalies: unexpected carriers, high power levels, non-orthodox modulation.  
   - Failed or unusual command sequences from rare operators or IP ranges.

4. **Hunt Queries (examples)**  
   - Time-correlate RF interference events with control anomalies.  
   - Cluster orbits/attitude deviations against normal operations per mission phase.  
   - Look for new TAS / TTPs in threat intel that mention satellite uplink toolkits.

5. **Mitigations / Response**  
   - Switch to **safe mode** with hardened command sequences.  
   - Enforce **multi-factor auth** and **out-of-band confirmation** for critical commands.  
   - Tighten **whitelists** for ground station IP ranges & certificates.  
   - Coordinate with RF monitoring networks and AIS/space situational awareness feeds.
        """
    )

    st.info(
        "All data here is mock / synthetic. You can later replace it with real logs, "
        "telemetry, or threat feeds (CSV, APIs, Kafka, etc.)."
    )
