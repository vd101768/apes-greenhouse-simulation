import streamlit as st

# Set up page layout
st.set_page_config(page_title="Greenhouse Effect Simulator", layout="wide")

st.title("The Molecular Basis of Climate Change")
st.caption("Exploring The Greenhouse Effect")

# Create the two tabs
tab1, tab2 = st.tabs(["Molecular View", "Atmospheric Sandbox"])

# =========================================================
# TAB 1: INDIVIDUAL MOLECULE VIEW (ANIMATED HTML5 CANVAS)
# =========================================================
with tab1:
    st.header("Molecular Dipole Moments & Photon Interaction")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Controls")
        molecule = st.selectbox("Select Molecule:", ["Oxygen (O₂)", "Carbon Dioxide (CO₂)"])
        show_dipole = st.checkbox("Show Dipole Vector", value=False)
        send_wave = st.checkbox("Turn On Infrared Radiation Source", value=False)
        
        st.markdown("---")
        if molecule == "Oxygen (O₂)":
            st.info("**Observations:** Note that when the wave passes through $O_2$, the symmetric bonds oscillate like a spring, but both sides move identically. The centers of charge never separate, meaning $\Delta\mu = 0$ at all times.")
        else:
            st.warning("**Observations:** When the IR wave hits $CO_2$, its frequency matches the bending mode of the molecule. The asymmetric shifting of atoms breaks symmetry, oscillating the dipole vector and trapping the energy.")

    with col2:
        mol_type = "O2" if molecule == "Oxygen (O₂)" else "CO2"
        wave_active = "true" if send_wave else "false"
        dipole_active = "true" if show_dipole else "false"

        canvas_html = f"""
        <div style="background-color: #111; padding: 10px; border-radius: 10px; border: 1px solid #333;">
            <canvas id="simCanvas" width="800" height="400" style="width: 100%; max-width: 800px; display: block; margin: auto;"></canvas>
        </div>

        <script>
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');

        const molType = "{mol_type}";
        const waveActive = {wave_active};
        const dipoleActive = {dipole_active};

        let time = 0;
        let waveProgress = 80; 
        let waveHitMolecule = false;

        function draw() {{
            ctx.fillStyle = "#111111";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            const centerX = canvas.width / 2 + 100; 
            const centerY = canvas.height / 2;
            
            time += 0.15;

            // 1. DRAW INFRARED EM SOURCE BOX
            ctx.fillStyle = "#441111";
            ctx.fillRect(0, 0, 80, canvas.height);
            ctx.fillStyle = "#ff5555";
            ctx.font = "14px sans-serif";
            ctx.fillText("IR SOURCE", 5, centerY);

            // 2. DRAW AND ANIMATE PROPAGATING SINE WAVE
            if (waveActive) {{
                ctx.strokeStyle = "#ff3333";
                ctx.lineWidth = 3;
                ctx.beginPath();
                
                // Let the wave front march forward until it hits the molecule, then stay extended
                if (waveProgress < centerX) {{
                    waveProgress += 5; 
                }} else {{
                    waveHitMolecule = true;
                }}

                // Draw the continuous traveling wave up to the current progress point
                // Crucial fix: using canvas.width instead of stopping at centerX ensures the light keeps flowing past!
                let limitX = waveHitMolecule ? canvas.width : waveProgress;
                for (let x = 80; x < limitX; x++) {{
                    let y = centerY + 30 * Math.sin((x * 0.05) - (time * 0.8));
                    if (x === 80) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }}
                ctx.stroke();
            }} else {{
                waveProgress = 80;
                waveHitMolecule = false;
            }}

            // 3. MOLECULAR GEOMETRY CONFIGURATION
            let jiggle = 0;
            if (waveActive && waveHitMolecule) {{
                jiggle = Math.sin(time * 0.8); 
            }}

            if (molType === "O2") {{
                // Continuous spring-like symmetric stretch animation
                let offset = 60 + (jiggle * 15); 
                
                ctx.strokeStyle = "#555";
                ctx.lineWidth = 6;
                ctx.beginPath();
                ctx.moveTo(centerX - offset, centerY - 5); ctx.lineTo(centerX + offset, centerY - 5);
                ctx.moveTo(centerX - offset, centerY + 5); ctx.lineTo(centerX + offset, centerY + 5);
                ctx.stroke();

                ctx.fillStyle = "#3366ff";
                ctx.beginPath(); ctx.arc(centerX - offset, centerY, 25, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(centerX + offset, centerY, 25, 0, Math.PI*2); ctx.fill();
                
                ctx.fillStyle = "#fff"; ctx.font = "16px Arial"; ctx.textAlign = "center";
                ctx.fillText("O", centerX - offset, centerY + 5);
                ctx.fillText("O", centerX + offset, centerY + 5);

                if (dipoleActive) {{
                    ctx.fillStyle = "#aaa"; ctx.font = "14px Arial";
                    ctx.fillText("Symmetric Stretch: Δμ = 0 (No Dipole)", centerX, centerY - 60);
                }}

            }} else if (molType === "CO2") {{
                // Continuous bending animation
                let atomOffsetY = jiggle * 35; 
                
                ctx.strokeStyle = "#555";
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.moveTo(centerX - 120, centerY); ctx.lineTo(centerX, centerY + atomOffsetY);
                ctx.moveTo(centerX + 120, centerY); ctx.lineTo(centerX, centerY + atomOffsetY);
                ctx.stroke();

                ctx.fillStyle = "#ff3333";
                ctx.beginPath(); ctx.arc(centerX - 120, centerY, 25, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(centerX + 120, centerY, 25, 0, Math.PI*2); ctx.fill();
                
                ctx.fillStyle = "#444444";
                ctx.strokeStyle = "#666"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(centerX, centerY + atomOffsetY, 20, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                ctx.fillStyle = "#fff"; ctx.font = "16px Arial"; ctx.textAlign = "center";
                ctx.fillText("O", centerX - 120, centerY + 5);
                ctx.fillText("O", centerX + 120, centerY + 5);
                ctx.fillText("C", centerX, centerY + atomOffsetY + 5);

                // 4. ACTIVE DIPOLE MOMENT VECTOR ARROW
                if (dipoleActive && waveActive && waveHitMolecule) {{
                    if (Math.abs(atomOffsetY) > 2) {{
                        ctx.strokeStyle = "#bb33ff";
                        ctx.lineWidth = 4;
                        ctx.fillStyle = "#bb33ff";
                        
                        ctx.beginPath();
                        ctx.moveTo(centerX, centerY);
                        ctx.lineTo(centerX, centerY + atomOffsetY * 1.3);
                        ctx.stroke(); // Fixed crash line here
                        
                        ctx.beginPath();
                        ctx.moveTo(centerX - 8, centerY + atomOffsetY * 1.1);
                        ctx.lineTo(centerX, centerY + atomOffsetY * 1.4);
                        ctx.lineTo(centerX + 8, centerY + atomOffsetY * 1.1);
                        ctx.fill();
                        
                        ctx.font = "14px Arial";
                        ctx.fillText("Dipole Vector (μ)", centerX + 70, centerY + (atomOffsetY * 0.7));
                    }}
                }}
            }}

            requestAnimationFrame(draw);
        }}

        draw();
        </script>
        """
        st.components.v1.html(canvas_html, height=430)

# =========================================================
# TAB 2: ATMOSPHERIC SANDBOX (MACRO VIEW)
# =========================================================
with tab2:
    st.header("The Macro View: Greenhouse Effect Sandbox")
    st.write("See how changing concentrations of IR-active molecules alters the probability of thermal escape.")
    
    import numpy as np
    import plotly.graph_objects as go
    
    co2_ppm = st.slider("Simulated Atmospheric CO₂ Concentration (PPM)", min_value=280, max_value=800, value=420, step=10)
    
    retention_probability = min(95.0, 50.0 + 15.0 * np.log(co2_ppm / 280.0))
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="Calculated IR Radiation Retention Probability", value=f"{retention_probability:.1f}%")
    with c2:
        escaped = 100.0 - retention_probability
        st.metric(label="Thermal Energy Escape Route", value=f"{escaped:.1f}%")
        
    np.random.seed(42)
    num_photons = 50
    photon_x = np.random.uniform(0, 10, num_photons)
    photon_y = np.random.uniform(0, 10, num_photons)
    
    trapped_mask = np.random.uniform(0, 100, num_photons) < retention_probability
    
    sandbox_fig = go.Figure()
    
    sandbox_fig.add_trace(go.Scatter(
        x=photon_x[~trapped_mask], y=photon_y[~trapped_mask],
        mode='markers', name='Escaping IR Radiation',
        marker=dict(symbol='triangle-up', size=12, color='yellow')
    ))
    
    sandbox_fig.add_trace(go.Scatter(
        x=photon_x[trapped_mask], y=photon_y[trapped_mask],
        mode='markers', name='Trapped / Re-radiated Heat',
        marker=dict(symbol='circle-cross', size=14, color='crimson')
    ))
    
    sandbox_fig.update_layout(
        title=f"Atmospheric Heat Field Visualizer at {co2_ppm} PPM",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='black'
    )
    st.plotly_chart(sandbox_fig, use_container_width=True)