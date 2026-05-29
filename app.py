import streamlit as st

# Set up page layout
st.set_page_config(page_title="APES Greenhouse Gas Simulator", layout="wide")

st.title("The Greenhouse Effect: A Molecular and Atmospheric Exploration")
st.caption("APES Capstone Project: Exploring What Makes Greenhouse Gases Absorb Energy")

# Create the two tabs
tab1, tab2 = st.tabs(["Microscopic Scale", "Atmospheric Scale"])

# =========================================================
# TAB 1: INDIVIDUAL MOLECULE VIEW (ANIMATED HTML5 CANVAS)
# =========================================================
with tab1:
    st.header("Molecular Dipole Moments & Photon Interaction")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Controls")
        molecule = st.selectbox("Select Molecule:", [
            "Oxygen (O₂)", 
            "Carbon Dioxide (CO₂)", 
            "Methane (CH₄)", 
            "Water Vapor (H₂O)",
            "Carbon Monoxide (CO)",
            "CFC-12"
        ])
        show_dipole = st.checkbox("Show Dipole Vector", value=False)
        send_wave = st.checkbox("Turn On Infrared Radiation Source", value=False)
        
        st.markdown("---")
        if molecule == "Oxygen (O₂)":
            st.info("**Observations:** When the wave passes through $O_2$, the symmetric bonds oscillate like a spring, but both sides move identically. The centers of charge never separate, meaning $\Delta\mu = 0$ at all times.")
        elif molecule == "Carbon Dioxide (CO₂)":
            st.warning("**Observations:** When the wave hits $CO_2$, its frequency matches the bending of the molecule. The temporary dipole of the molecule is amplified, trapping the energy in the wave.")
        elif molecule == "Methane (CH₄)":
            st.error("**Observations:** Methane starts off with a weak dipole moment due to oscillations among its bonds. When IR radiation hits it, multiple bonds bend and stretch out of alignment at once. This creates massive, chaotic dipole fluctuations, making it a very powerful greenhouse gas.")
        elif molecule == "Water Vapor (H₂O)":
            st.info("**Observations:** Water is naturally asymmetrical due to its bent geometry and highly polar O-H bonds, so a permanent dipole vector exists. When IR hits it, the bonds bounce intensely, making it great at absorbing heat.")
        elif molecule == "Carbon Monoxide (CO)":
            st.success("**Observations:** CO has a permanent, strong asymmetric dipole vector. However, when the IR wave hits it, nothing happens! Its triple-bond requires a much higher frequency photon than what Earth's heat provides, proving dipole moments are useless without the sufficient amount of energy.")
        elif molecule == "CFC-12":
            st.error("**Observations:** CFC-12 is a synthetic compound. When hit by IR radiation, its highly polar Fluorine and Chlorine bonds stretch asymmetrically and bounce around. Because its quantum frequency bands lie perfectly along Earth's open infrared re-radiation spectrum, its capacity to trap heat is extremely high.")

    with col2:
        if molecule == "Oxygen (O₂)":
            mol_type = "O2"
        elif molecule == "Carbon Dioxide (CO₂)":
            mol_type = "CO2"
        elif molecule == "Methane (CH₄)":
            mol_type = "CH4"
        elif molecule == "Water Vapor (H₂O)":
            mol_type = "H2O"
        elif molecule == "Carbon Monoxide (CO)":
            mol_type = "CO"
        else:
            mol_type = "CFC12"
            
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

            // 1. DRAW SLEEK LASER EMITTER SOURCE
            let gradient = ctx.createLinearGradient(0, 0, 70, 0);
            gradient.addColorStop(0, "#222"); gradient.addColorStop(0.5, "#444"); gradient.addColorStop(1, "#333");
            ctx.fillStyle = gradient; ctx.fillRect(0, 20, 65, canvas.height - 40);
            
            ctx.strokeStyle = "#555"; ctx.lineWidth = 2; ctx.strokeRect(0, 20, 65, canvas.height - 40);

            let lensGradient = ctx.createRadialGradient(65, centerY, 2, 65, centerY, 15);
            lensGradient.addColorStop(0, "#ff9999"); lensGradient.addColorStop(0.3, "#ff3333"); lensGradient.addColorStop(1, "transparent");
            ctx.fillStyle = lensGradient; ctx.beginPath(); ctx.arc(65, centerY, 15, -Math.PI/2, Math.PI/2); ctx.fill();

            ctx.save(); ctx.translate(25, centerY); ctx.rotate(-Math.PI / 2);
            ctx.fillStyle = waveActive ? "#ff5555" : "#888"; ctx.font = "bold 12px sans-serif";
            ctx.shadowColor = waveActive ? "#ff0000" : "transparent"; ctx.shadowBlur = 8;
            ctx.fillText(waveActive ? "LASER ACTIVE" : "SYSTEM READY", 0, 5); ctx.restore();

            // 2. DRAW AND ANIMATE PROPAGATING SINE WAVE
            if (waveActive) {{
                ctx.strokeStyle = "#ff3333"; ctx.lineWidth = 3; ctx.beginPath();
                if (waveProgress < canvas.width) waveProgress += 5; 
                if (waveProgress >= centerX) waveHitMolecule = true;

                for (let x = 80; x < waveProgress; x++) {{
                    let y = centerY + 30 * Math.sin((x * 0.05) - (time * 0.8));
                    if (x === 80) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }}
                ctx.stroke();
            }} else {{
                waveProgress = 80; waveHitMolecule = false;
            }}

            // 3. MOLECULAR GEOMETRY CONFIGURATION
            let jiggle = (waveActive && waveHitMolecule && molType !== "CO") ? Math.sin(time * 0.8) : 0;

            if (molType === "O2") {{
                let offset = 60 + (jiggle * 15); 
                ctx.strokeStyle = "#555"; ctx.lineWidth = 6; ctx.beginPath();
                ctx.moveTo(centerX - offset, centerY - 5); ctx.lineTo(centerX + offset, centerY - 5);
                ctx.moveTo(centerX - offset, centerY + 5); ctx.lineTo(centerX + offset, centerY + 5);
                ctx.stroke();

                ctx.fillStyle = "#3366ff";
                ctx.beginPath(); ctx.arc(centerX - offset, centerY, 25, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(centerX + offset, centerY, 25, 0, Math.PI*2); ctx.fill();
                
                ctx.fillStyle = "#fff"; ctx.font = "16px Arial"; ctx.textAlign = "center";
                ctx.fillText("O", centerX - offset, centerY + 5); ctx.fillText("O", centerX + offset, centerY + 5);

                if (dipoleActive) {{
                    ctx.fillStyle = "#aaa"; ctx.font = "14px Arial"; ctx.textAlign = "center";
                    ctx.fillText("Symmetric Stretch: Δμ = 0 (No Dipole)", centerX, centerY - 60);
                }}

            }} else if (molType === "CO2") {{
                let atomOffsetY = jiggle * 35; 
                ctx.strokeStyle = "#555"; ctx.lineWidth = 4; ctx.beginPath();
                ctx.moveTo(centerX - 120, centerY); ctx.lineTo(centerX, centerY + atomOffsetY);
                ctx.moveTo(centerX + 120, centerY); ctx.lineTo(centerX, centerY + atomOffsetY);
                ctx.stroke();

                ctx.fillStyle = "#ff3333";
                ctx.beginPath(); ctx.arc(centerX - 120, centerY, 25, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(centerX + 120, centerY, 25, 0, Math.PI*2); ctx.fill();
                
                ctx.fillStyle = "#444444"; ctx.strokeStyle = "#666"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(centerX, centerY + atomOffsetY, 20, 0, Math.PI*2); ctx.fill(); ctx.stroke();

                ctx.fillStyle = "#fff"; ctx.font = "16px Arial"; ctx.textAlign = "center";
                ctx.fillText("O", centerX - 120, centerY + 5); ctx.fillText("O", centerX + 120, centerY + 5); ctx.fillText("C", centerX, centerY + atomOffsetY + 5);

                if (dipoleActive && waveActive && waveHitMolecule && Math.abs(atomOffsetY) > 2) {{
                    ctx.strokeStyle = "#bb33ff"; ctx.lineWidth = 4; ctx.fillStyle = "#bb33ff"; ctx.beginPath();
                    ctx.moveTo(centerX, centerY); ctx.lineTo(centerX, centerY + atomOffsetY * 1.3); ctx.stroke(); 
                    
                    ctx.beginPath();
                    ctx.moveTo(centerX - 8, centerY + atomOffsetY * 1.1);
                    ctx.lineTo(centerX, centerY + atomOffsetY * 1.4);
                    ctx.lineTo(centerX + 8, centerY + atomOffsetY * 1.1);
                    ctx.fill();
                }}
            }} else if (molType === "CH4") {{
                let legLength = 80;
                let topLegY = centerY - legLength + (jiggle * 25);
                let bottomLegY = centerY + legLength + (Math.cos(time * 0.8) * 15);
                let leftLegX = centerX - legLength + (Math.sin(time * 0.5) * 20);
                let rightLegX = centerX + legLength + (jiggle * 10);

                let carbonX = centerX + (Math.sin(time * 0.8) * 8);
                let carbonY = centerY + (jiggle * 8);

                ctx.strokeStyle = "#555"; ctx.lineWidth = 4; ctx.beginPath();
                ctx.moveTo(centerX, topLegY); ctx.lineTo(carbonX, carbonY);
                ctx.moveTo(centerX, bottomLegY); ctx.lineTo(carbonX, carbonY);
                ctx.moveTo(leftLegX, centerY); ctx.lineTo(carbonX, carbonY);
                ctx.moveTo(rightLegX, centerY); ctx.lineTo(carbonX, carbonY);
                ctx.stroke();

                ctx.fillStyle = "#444444"; ctx.strokeStyle = "#666"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(carbonX, carbonY, 22, 0, Math.PI*2); ctx.fill(); ctx.stroke();
                ctx.fillStyle = "#fff"; ctx.font = "16px Arial"; ctx.textAlign = "center";
                ctx.fillText("C", carbonX, carbonY + 5);

                ctx.fillStyle = "#e0e0e0";
                ctx.beginPath(); ctx.arc(centerX, topLegY, 16, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(centerX, bottomLegY, 16, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(leftLegX, centerY, 16, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(rightLegX, centerY, 16, 0, Math.PI*2); ctx.fill();

                ctx.fillStyle = "#222"; ctx.font = "14px Arial";
                ctx.fillText("H", centerX, topLegY + 5); ctx.fillText("H", centerX, bottomLegY + 5);
                ctx.fillText("H", leftLegX, centerY + 5); ctx.fillText("H", rightLegX, centerY + 5);

                if (dipoleActive && waveActive && waveHitMolecule) {{
                    let netDipoleX = (leftLegX + rightLegX) / 2 - carbonX;
                    let netDipoleY = (topLegY + bottomLegY) / 2 - carbonY;
                    ctx.strokeStyle = "#bb33ff"; ctx.lineWidth = 4; ctx.fillStyle = "#bb33ff"; ctx.beginPath();
                    ctx.moveTo(carbonX, carbonY);
                    let targetX = carbonX + netDipoleX * 2.5; let targetY = carbonY + netDipoleY * 2.5;
                    ctx.lineTo(targetX, targetY); ctx.stroke();
                    ctx.beginPath(); ctx.arc(targetX, targetY, 6, 0, Math.PI*2); ctx.fill();
                }}
            }} else if (molType === "H2O") {{
                let oxygenX = centerX; let oxygenY = centerY - 30 + (jiggle * 5); 
                let hydrogenDistX = 70 + (jiggle * 12); let hydrogenDistY = 80 + (Math.cos(time * 0.8) * 15); 
                let h1X = centerX - hydrogenDistX; let h1Y = centerY + hydrogenDistY;
                let h2X = centerX + hydrogenDistX; let h2Y = centerY + hydrogenDistY;

                ctx.strokeStyle = "#555"; ctx.lineWidth = 4; ctx.beginPath();
                ctx.moveTo(oxygenX, oxygenY); ctx.lineTo(h1X, h1Y); ctx.moveTo(oxygenX, oxygenY); ctx.lineTo(h2X, h2Y);
                ctx.stroke();

                ctx.fillStyle = "#ff3333"; ctx.beginPath(); ctx.arc(oxygenX, oxygenY, 25, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#fff"; ctx.font = "16px Arial"; ctx.textAlign = "center";
                ctx.fillText("O", oxygenX, oxygenY + 5);

                ctx.fillStyle = "#e0e0e0";
                ctx.beginPath(); ctx.arc(h1X, h1Y, 16, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(h2X, h2Y, 16, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#222"; ctx.font = "14px Arial";
                ctx.fillText("H", h1X, h1Y + 5); ctx.fillText("H", h2X, h2Y + 5);

                // FIXED: Adding Water Dipole Vector
                if (dipoleActive) {{
                    ctx.strokeStyle = "#bb33ff"; ctx.lineWidth = 4; ctx.fillStyle = "#bb33ff";
                    ctx.beginPath();
                    ctx.moveTo(oxygenX, oxygenY);
                    let vectorLengthY = 60 + (hydrogenDistY * 0.5);
                    ctx.lineTo(oxygenX, oxygenY + vectorLengthY);
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(oxygenX - 8, oxygenY + vectorLengthY - 12);
                    ctx.lineTo(oxygenX, oxygenY + vectorLengthY);
                    ctx.lineTo(oxygenX + 8, oxygenY + vectorLengthY - 12);
                    ctx.fill();
                }}
            }} else if (molType === "CO") {{
                let offsetC = -50; let offsetO = 50;
                ctx.strokeStyle = "#555"; ctx.lineWidth = 8; ctx.beginPath();
                ctx.moveTo(centerX + offsetC, centerY - 8); ctx.lineTo(centerX + offsetO, centerY - 8);
                ctx.moveTo(centerX + offsetC, centerY); ctx.lineTo(centerX + offsetO, centerY);
                ctx.moveTo(centerX + offsetC, centerY + 8); ctx.lineTo(centerX + offsetO, centerY + 8);
                ctx.stroke();

                ctx.fillStyle = "#444444"; ctx.beginPath(); ctx.arc(centerX + offsetC, centerY, 22, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#ff3333"; ctx.beginPath(); ctx.arc(centerX + offsetO, centerY, 25, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#fff"; ctx.font = "16px Arial"; ctx.textAlign = "center";
                ctx.fillText("C", centerX + offsetC, centerY + 5); ctx.fillText("O", centerX + offsetO, centerY + 5);

                // FIXED: Adding Carbon Monoxide Dipole Vector
                if (dipoleActive) {{
                    ctx.strokeStyle = "#bb33ff"; ctx.lineWidth = 4; ctx.fillStyle = "#bb33ff";
                    ctx.beginPath();
                    ctx.moveTo(centerX + offsetC, centerY - 45);
                    ctx.lineTo(centerX + offsetO - 10, centerY - 45);
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(centerX + offsetO - 20, centerY - 52);
                    ctx.lineTo(centerX + offsetO - 10, centerY - 45);
                    ctx.lineTo(centerX + offsetO - 20, centerY - 38);
                    ctx.fill();
                }}
            }} else if (molType === "CFC12") {{
                let arm = 85;
                let f1X = centerX - arm + (jiggle * 12); let f1Y = centerY - arm + (jiggle * 12);
                let f2X = centerX + arm + (Math.cos(time * 0.8) * 10); let f2Y = centerY - arm - (Math.cos(time * 0.8) * 10);
                let cl1X = centerX - arm - (jiggle * 15); let cl1Y = centerY + arm + (jiggle * 15);
                let cl2X = centerX + arm + (Math.sin(time * 0.6) * 15); let cl2Y = centerY + arm + (Math.sin(time * 0.6) * 15);

                ctx.strokeStyle = "#555"; ctx.lineWidth = 4; ctx.beginPath();
                ctx.moveTo(centerX, centerY); ctx.lineTo(f1X, f1Y); ctx.moveTo(centerX, centerY); ctx.lineTo(f2X, f2Y);
                ctx.moveTo(centerX, centerY); ctx.lineTo(cl1X, cl1Y); ctx.moveTo(centerX, centerY); ctx.lineTo(cl2X, cl2Y);
                ctx.stroke();
                ctx.fillStyle = "#444444"; ctx.beginPath(); ctx.arc(centerX, centerY, 20, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#ccff33"; ctx.beginPath(); ctx.arc(f1X, f1Y, 16, 0, Math.PI*2); ctx.arc(f2X, f2Y, 16, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#00cc66"; ctx.beginPath(); ctx.arc(cl1X, cl1Y, 18, 0, Math.PI*2); ctx.arc(cl2X, cl2Y, 18, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "#fff"; ctx.font = "14px Arial"; ctx.textAlign = "center"; ctx.fillText("C", centerX, centerY + 5);
                ctx.fillStyle = "#222"; ctx.fillText("F", f1X, f1Y + 5); ctx.fillText("F", f2X, f2Y + 5);
                ctx.fillStyle = "#fff"; ctx.fillText("Cl", cl1X, cl1Y + 5); ctx.fillText("Cl", cl2X, cl2Y + 5);

                // FIXED: Adding CFC-12 Asymmetric Stretching Dipole Vector
                if (dipoleActive) {{
                    let dx = (f1X + f2X + cl1X + cl2X) / 4 - centerX;
                    let dy = (f1Y + f2Y + cl1Y + cl2Y) / 4 - centerY;
                    ctx.strokeStyle = "#bb33ff"; ctx.lineWidth = 5; ctx.fillStyle = "#bb33ff";
                    ctx.beginPath();
                    ctx.moveTo(centerX, centerY);
                    ctx.lineTo(centerX + dx * 6, centerY + dy * 6);
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.arc(centerX + dx * 6, centerY + dy * 6, 6, 0, Math.PI*2);
                    ctx.fill();
                }}
            }}

            requestAnimationFrame(draw);
        }}
        draw();
        </script>
        """
        st.components.v1.html(canvas_html, height=430)

# =========================================================
# UNDER-CANVAS: GWP METRICS & APES CURRICULUM EXPLAINER
# =========================================================
        st.markdown("### Quantitative Data & Analysis")
        with st.expander("Show Global Warming Potential (GWP) & Quantum Spectrum Matching"):
            import numpy as np
            import plotly.graph_objects as go

            wavelengths = np.linspace(2, 25, 300)
            earth_emission = (1 / wavelengths**5) / (np.exp(50 / wavelengths) - 1)
            earth_emission = (earth_emission / np.max(earth_emission)) * 100

            absorption_center = None
            absorption_width = 0.5
            
            if molecule == "Oxygen (O₂)":
                gwp_val = "0"
                lifetime = "N/A"
                potency = "Transparent to thermal radiation."
                apes_note = "Because $O_2$ has zero net dipole shift ($\Delta \mu = 0$), it cannot trap heat. It has no quantum absorption lines in the infrared spectrum."
            elif molecule == "Carbon Dioxide (CO₂)":
                gwp_val = "1 (The Baseline)"
                lifetime = "Variable (100 - 1,000+ years)"
                potency = "Standard reference value for all greenhouse gases."
                apes_note = "While $CO_2$ has a lower radiative efficiency than methane, its immense atmospheric residence time and high concentrations due to fossil fuel combustion make it the primary driver of anthropogenic climate change."
                absorption_center = 15.0; absorption_width = 1.2
            elif molecule == "Methane (CH₄)":
                gwp_val = "28 - 36"
                lifetime = "~12 years"
                potency = "Roughly 30x more effective at trapping heat than $CO_2$ over 100 years."
                apes_note = "Methane's multi-legged asymmetric structure allows for massive chaotic dipole oscillations. Even though it breaks down quickly via chemical reactions, its extreme radiative efficiency makes it a critical near-term target for climate mitigation (e.g., landfills and livestock management)."
                absorption_center = 7.7; absorption_width = 0.6
            elif molecule == "Water Vapor (H₂O)":
                gwp_val = "N/A (Effectively 0)"
                lifetime = "Short (~9 to 10 Days)"
                potency = "Highest absolute absorption capacity, but controlled entirely by thermal balance, not direct human emission."
                apes_note = "**Crucial APES Concept:** Water vapor is the primary contributor to Earth's *natural* greenhouse effect. However, it participates in a **Positive Climate Feedback Loop**. Carbon dioxide warms the air $\\rightarrow$ increased evaporation rates $\\rightarrow$ more atmospheric water vapor $\\rightarrow$ accelerated thermal entrapment."
                absorption_center = 18.5; absorption_width = 4.0
            elif molecule == "Carbon Monoxide (CO)":
                gwp_val = "0 (Indirectly ~3)"
                lifetime = "Short (~2 months)"
                potency = "Possesses a strong permanent dipole, but cannot absorb Earth's thermal emission wavelengths."
                apes_note = "**The Quantum Exemption:** Carbon Monoxide has a high-contrast permanent dipole vector. However, because its C-O triple bond is incredibly stiff, its quantized vibrational energy states are highly separated. It requires an incoming light wavelength of around **$4.67\ \mu\text{m}$** to react. Because Earth's surface heat radiates out at much cooler, longer wavelengths (**$10\ \mu\text{m} - 15\ \mu\text{m}$**), the thermal photons pass directly through it without matching resonance requirements."
                absorption_center = 4.67; absorption_width = 0.3
            else: # CFC-12
                gwp_val = "10,200"
                lifetime = "100 Years"
                potency = "Over ten thousand times more powerful than $CO_2$ at trapping atmospheric heat."
                apes_note = "**The Atmospheric Window Exploit:** CFCs are exceptionally dangerous because their polar carbon-fluorine and carbon-chlorine stretching modes require a quantum wavelength absorption of exactly **$9.2\ \mu\text{m}$**. This lands precisely in the dead center of the **Atmospheric Window**—the exact wavelength gap where natural gases are transparent and Earth's heat output reaches its maximum intensity. By blocking our environment's primary structural escape hatch, synthetic chemicals like CFC-12 trigger extreme climate forcing, which led to their global ban under the Montreal Protocol."
                absorption_center = 9.2; absorption_width = 0.8

            c1, c2 = st.columns(2)
            with c1:
                st.metric(label=f"100-Year GWP ({molecule})", value=gwp_val)
                st.caption(f"**Radiative Potency:** {potency}")
            with c2:
                st.metric(label="Average Atmospheric Lifetime", value=lifetime)
            
            st.markdown("---")
            
            # 4. BUILD THE PLOTLY INTERACTIVE QUANTUM SPECTRUM MATCHING CHART
            fig_spec = go.Figure()

            # Forced bright labels for the baseline data trace
            fig_spec.add_trace(go.Scatter(
                x=wavelengths, y=earth_emission, mode='lines', 
                name="Earth's Outgoing Thermal IR Emission",
                line=dict(color='#ff5555', width=3), 
                fill='tozeroy', fillcolor='rgba(255, 85, 85, 0.15)'
            ))

            if absorption_center is not None:
                fig_spec.add_vrect(
                    x0=absorption_center - absorption_width, x1=absorption_center + absorption_width,
                    fillcolor="rgba(187, 51, 255, 0.4)", opacity=0.7, layer="below", line_width=0,
                    annotation_text=f"{molecule} Quantum Resonance Band", annotation_position="top left",
                    annotation_font=dict(size=13, color="#e099ff") 
                )

            # FULL HIGH-CONTRAST TEXT OVERRIDES ON BLACK LAYOUT (Answers Removed for Student Analysis)
            fig_spec.update_layout(
                title=dict(
                    text=f"Quantum Frequency Matching Layout ({molecule})", 
                    font=dict(size=18, color='#ffffff') 
                ),
                xaxis=dict(
                    title=dict(text="Wavelength (μm) [Lower frequency ➔]", font=dict(size=14, color='#ffffff')),
                    tickfont=dict(size=12, color='#cccccc'), 
                    gridcolor='#252525', range=[2, 25]
                ),
                yaxis=dict(
                    title=dict(text="Relative Thermal Intensity / Absorption Probability (%)", font=dict(size=14, color='#ffffff')),
                    tickfont=dict(size=12, color='#cccccc'), 
                    gridcolor='#252525', range=[0, 110]
                ),
                plot_bgcolor='#111111',
                paper_bgcolor='#111111',
                showlegend=True,
                legend=dict(
                    x=0.55, y=0.95,
                    font=dict(size=12, color='#ffffff'), 
                    bgcolor='rgba(17, 17, 17, 0.8)',
                    bordercolor='#444444',
                    borderwidth=1
                )
            )
            st.plotly_chart(fig_spec, use_container_width=True)

# =========================================================
# TAB 2: ATMOSPHERIC SANDBOX (MACRO VIEW)
# =========================================================
with tab2:
    st.header("A Greenhouse Effect Sandbox")
    st.caption("Instructions: The simulation is currently paused. Click anywhere inside an atmospheric zone to launch its targeted radiation loop. Click another zone to shift models.")

    sandbox_html = f"""
    <div style="background-color: #111; padding: 5px; border-radius: 12px; border: 1px solid #333; overflow: hidden;">
        <canvas id="worldCanvas" width="1000" height="540" style="width: 100%; height: auto; aspect-ratio: 1000 / 540; display: block;"></canvas>
    </div>

    <script>
    const canvas = document.getElementById('worldCanvas');
    const ctx = canvas.getContext('2d');

    let mouseX = 0;
    let mouseY = 0;
    let activeThird = 1; 
    let selectedThird = -1; // Paused by default until clicked
    let time = 0;
    let photons = [];

    function spawnPhoton() {{
        let w3 = canvas.width / 3;
        let targetMinX = selectedThird * w3 + 30;
        let targetMaxX = (selectedThird + 1) * w3 - 30;
        
        photons.push({{
            x: 60, y: 60,                  
            targetX: targetMinX + Math.random() * (targetMaxX - targetMinX),
            targetY: canvas.height - 65, 
            stage: 0,                      
            speed: 4 + Math.random() * 2
        }});
    }}

    canvas.addEventListener('mousemove', (e) => {{
        const rect = canvas.getBoundingClientRect();
        mouseX = (e.clientX - rect.left) * (canvas.width / rect.width);
        mouseY = (e.clientY - rect.top) * (canvas.height / rect.height);
        
        if (mouseX < canvas.width / 3) activeThird = 0;
        else if (mouseX < (canvas.width / 3) * 2) activeThird = 1;
        else activeThird = 2;
    }});

    canvas.addEventListener('click', () => {{
        if (selectedThird !== activeThird) {{
            selectedThird = activeThird;
            photons = []; 
        }}
    }});

    function animateSandbox() {{
        if (selectedThird !== -1) {{
            time += 0.05;
        }}
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 1. ENVIRONMENT BACKGROUND (Sky Blue)
        ctx.fillStyle = "#87CEEB"; 
        ctx.fillRect(0, 0, canvas.width, canvas.height - 65);

        // 2. INTERACTIVE ZONE HOVER INTERACTION
        ctx.fillStyle = "rgba(255, 255, 255, 0.15)";
        ctx.fillRect((activeThird * canvas.width / 3), 0, canvas.width / 3, canvas.height - 65);

        // Active Zone Outline Box
        if (selectedThird !== -1) {{
            ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
            ctx.lineWidth = 3;
            ctx.strokeRect((selectedThird * canvas.width / 3) + 2, 2, (canvas.width / 3) - 4, canvas.height - 69);
        }}

        // 3. ECOSYSTEM PLATFORM (Green Grass & Radiant Sun)
        ctx.fillStyle = "#32CD32"; 
        ctx.fillRect(0, canvas.height - 65, canvas.width, 65);

        let sunGrad = ctx.createRadialGradient(50, 50, 10, 50, 50, 60);
        sunGrad.addColorStop(0, "#FFF700"); sunGrad.addColorStop(1, "transparent");
        ctx.fillStyle = sunGrad; ctx.beginPath(); ctx.arc(50, 50, 60, 0, Math.PI*2); ctx.fill();

        let w3 = canvas.width / 3;
        
        // 4. THE MOLECULAR MATRIX DRAW ENGINE
        // Left Third: Oxygen (O2)
        ctx.fillStyle = "#0055ff";
        for(let i=0; i<4; i++) {{
            let oy = 130 + (selectedThird === 0 ? Math.sin(time + i) * 12 : 0);
            let ox = 30 + (i * 65);
            ctx.beginPath(); ctx.arc(ox, oy, 9, 0, Math.PI*2); ctx.arc(ox+14, oy, 9, 0, Math.PI*2); ctx.fill();
        }}
        ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.font = "bold 14px Arial"; ctx.textAlign = "left";
        ctx.fillText("Oxygen (O₂)", 15, canvas.height - 80);

        // Center Third: Carbon Dioxide (CO2)
        ctx.fillStyle = "#ff3333";
        for(let i=0; i<4; i++) {{
            let cx = w3 + 45 + (i * 65); 
            let cy = 150 + (selectedThird === 1 ? Math.cos(time + i) * 15 : 0);
            let bend = selectedThird === 1 ? Math.sin(time * 2 + i) * 7 : 0;
            ctx.fillStyle = "#ff3333"; 
            ctx.beginPath(); ctx.arc(cx - 18, cy, 9, 0, Math.PI*2); ctx.arc(cx + 18, cy, 9, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#444"; 
            ctx.beginPath(); ctx.arc(cx, cy + bend, 8, 0, Math.PI*2); ctx.fill();
        }}
        ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillText("Carbon Dioxide (CO₂)", w3 + 15, canvas.height - 80);

        // Right Third: Methane (CH4)
        for(let i=0; i<3; i++) {{
            let mx = (w3 * 2) + 65 + (i * 80); 
            let my = 160 + (selectedThird === 2 ? Math.sin(time * 1.5 + i) * 20 : 0);
            let pulse = selectedThird === 2 ? Math.sin(time * 3 + i) * 5 : 0;
            
            ctx.strokeStyle = "#444"; ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(mx - 18 + pulse, my); ctx.lineTo(mx + 18 - pulse, my);
            ctx.moveTo(mx, my - 18); ctx.lineTo(mx, my + 18);
            ctx.stroke();

            ctx.fillStyle = "#444444"; ctx.beginPath(); ctx.arc(mx, my, 10, 0, Math.PI*2); ctx.fill(); 
            
            ctx.fillStyle = "#ffffff"; 
            ctx.fillRect(mx - 23 + pulse, my - 5, 10, 10);
            ctx.fillRect(mx + 13 - pulse, my - 5, 10, 10);
            ctx.fillRect(mx - 5, my - 23, 10, 10);
            ctx.fillRect(mx - 5, my + 13, 10, 10);
        }}
        ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillText("Methane (CH₄)", (w3*2) + 15, canvas.height - 80);

        // 5. THERMODYNAMIC RADIATION ENGINE
        if (selectedThird !== -1) {{
            if (Math.random() < 0.08) spawnPhoton();

            for (let i = photons.length - 1; i >= 0; i--) {{
                let p = photons[i];
                let currentZone = 0;
                if (p.x >= w3 && p.x < w3 * 2) currentZone = 1;
                if (p.x >= w3 * 2) currentZone = 2;

                ctx.fillStyle = (p.stage === 0) ? "#FFFF00" : "#FF3333";
                ctx.beginPath(); 
                ctx.arc(p.x, p.y, 5, 0, Math.PI*2); 
                ctx.fill();

                if (p.stage === 0) {{
                    let dx = p.targetX - p.x; let dy = p.targetY - p.y;
                    let dist = Math.sqrt(dx*dx + dy*dy);
                    if (dist > 5) {{
                        p.x += (dx / dist) * p.speed; p.y += (dy / dist) * p.speed;
                    }} else {{
                        p.stage = 1; 
                    }}
                }} else if (p.stage === 1) {{
                    p.y -= p.speed * 0.7;
                    
                    if (currentZone === selectedThird && p.y < 320 && p.y > 100) {{
                        if (selectedThird === 1 && Math.random() < 0.02) {{ 
                            p.stage = 2; 
                        }} else if (selectedThird === 2 && Math.random() < 0.06) {{ 
                            p.stage = 2; 
                        }}
                    }}
                    if (p.y < 0) photons.splice(i, 1);
                }} else if (p.stage === 2) {{
                    p.y += p.speed * 0.7;
                    if (p.y > canvas.height - 65) {{
                        p.stage = 1; 
                        p.targetX = p.x + (Math.random() * 80 - 40);
                    }}
                }}
            }}
        }} else {{
            ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.font = "bold 20px sans-serif"; ctx.textAlign = "center";
            ctx.fillText("⏸️ CLICK ANY ATMOSPHERIC ZONE TO START THE MODEL", canvas.width / 2, canvas.height / 2);
        }}

        requestAnimationFrame(animateSandbox);
    }}
    animateSandbox();
    </script>
    """
    st.components.v1.html(sandbox_html, height=1000)
