import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# =================================================================
# 1. PROFESSIONAL PHYSICS ENGINE CLASS
# =================================================================
class ElementalProEngine:
    """
    Core Engine for Material Science Calculations.
    Includes: Thermal, Electrical, Mechanical, and Crystallographic logic.
    """
    def __init__(self):
        self.data = self._load_comprehensive_database()

    def _load_comprehensive_database(self):
        # Database containing: Density (g/cm³), Modulus (GPa), 
        # Thermal Expansion (µm/m·K), Conductivity (MS/m), Lattice (pm)
        raw = {
            "Element": ["Aluminum", "Copper", "Iron", "Gold", "Titanium", "Tungsten", "Silicon", "Nickel", "Silver", "Lead", "Platinum", "Magnesium", "Zinc"],
            "Symbol": ["Al", "Cu", "Fe", "Au", "Ti", "W", "Si", "Ni", "Ag", "Pb", "Pt", "Mg", "Zn"],
            "Density": [2.70, 8.96, 7.87, 19.30, 4.51, 19.25, 2.33, 8.91, 10.49, 11.34, 21.45, 1.74, 7.13],
            "YoungsModulus": [70, 130, 211, 78, 116, 411, 170, 200, 83, 16, 168, 45, 108],
            "ThermalExpansion": [23.1, 16.5, 11.8, 14.2, 8.6, 4.5, 2.6, 13.4, 18.9, 28.9, 8.8, 24.8, 30.2],
            "ElectricalConductivity": [35.0, 59.6, 10.0, 41.0, 2.38, 17.9, 0.0004, 14.3, 63.0, 4.8, 9.4, 22.6, 16.6],
            "CrystalStructure": ["FCC", "FCC", "BCC", "FCC", "HCP", "BCC", "Diamond", "FCC", "FCC", "FCC", "FCC", "HCP", "HCP"],
            "Lattice_a": [404.9, 361.5, 286.6, 407.8, 295.1, 316.5, 543.1, 352.4, 408.5, 495.1, 392.4, 320.9, 266.5],
            "Lattice_c": [0, 0, 0, 0, 468.6, 0, 0, 0, 0, 0, 0, 521.0, 494.7]
        }
        return pd.DataFrame(raw)

    def calculate_thermal_strain(self, element, l0, delta_t):
        """Calculates linear expansion: ΔL = L₀ * α * ΔT"""
        alpha = self.data[self.data['Element'] == element]['ThermalExpansion'].values[0] * 1e-6
        return l0 * alpha * delta_t

    def calculate_electrical_resistance(self, element, length, area):
        """Calculates Resistance R = L / (σ * A)"""
        sigma = self.data[self.data['Element'] == element]['ElectricalConductivity'].values[0] * 1e6
        if sigma == 0: return float('inf')
        return length / (sigma * area)

    def get_unit_cell_volume(self, element):
        """Calculates the geometric volume of the crystal unit cell in pm³"""
        row = self.data[self.data['Element'] == element].iloc[0]
        a = row['Lattice_a']
        c = row['Lattice_c']
        struct = row['CrystalStructure']
        
        if struct in ["FCC", "BCC", "Diamond"]:
            return a**3
        elif struct == "HCP":
            # Volume = (3 * √3 / 2) * a² * c
            return 2.598 * (a**2) * c
        return 0

# =================================================================
# 2. UI AND DASHBOARD LAYOUT
# =================================================================
def main():
    st.set_page_config(page_title="Elemental Pro | Industrial Engine", layout="wide")
    engine = ElementalProEngine()

    # Custom Professional CSS
    st.markdown("""
        <style>
        .stMetric { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6; }
        .main-title { color: #1e3a8a; font-size: 38px; font-weight: 800; border-bottom: 2px solid #1e3a8a; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="main-title">🛡️ ELEMENTAL DYNAMICS PROFESSIONAL</p>', unsafe_allow_html=True)
    
    # --- SIDEBAR CONTROLS ---
    with st.sidebar:
        st.header("Control Panel")
        target_el = st.selectbox("Select Element", engine.data['Element'])
        st.divider()
        st.write("### Simulation Inputs")
        in_temp = st.slider("Temperature Change (ΔK)", -273, 1000, 100)
        in_len = st.number_input("Specimen Length (m)", value=1.0, step=0.1)
        in_area = st.number_input("Cross Section (m²)", value=0.0001, format="%.6f")

    # --- TOP METRICS ---
    el_info = engine.data[engine.data['Element'] == target_el].iloc[0]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Density", f"{el_info['Density']} g/cm³")
    m2.metric("Young's Modulus", f"{el_info['YoungsModulus']} GPa")
    m3.metric("Conductivity", f"{el_info['ElectricalConductivity']} MS/m")
    m4.metric("Crystal Lattice", f"{el_info['CrystalStructure']}")

    # --- DASHBOARD TABS ---
    t1, t2, t3 = st.tabs(["🏗️ Mechanical & Thermal", "💎 Crystallography", "📈 Analytics"])

    with t1:
        st.subheader("Structural Simulation Results")
        col_a, col_b = st.columns(2)
        
        with col_a:
            exp = engine.calculate_thermal_strain(target_el, in_len, in_temp)
            st.info(f"**Thermal Expansion (ΔL):** {exp:.6f} meters")
            st.caption("Calculated based on Linear Coefficient of Thermal Expansion.")

        with col_b:
            res = engine.calculate_electrical_resistance(target_el, in_len, in_area)
            st.success(f"**Electrical Resistance:** {res:.2e} Ohms")
            st.caption("Calculated using cross-sectional area and material conductivity.")

    with t2:
        st.subheader("Atomic Lattice Configuration")
        vol = engine.get_unit_cell_volume(target_el)
        
        c_left, c_right = st.columns([1, 2])
        with c_left:
            st.write(f"**Parameter a:** {el_info['Lattice_a']} pm")
            if el_info['Lattice_c'] > 0:
                st.write(f"**Parameter c:** {el_info['Lattice_c']} pm")
            st.write(f"**Unit Cell Volume:** {vol:,.2f} pm³")
        
        with c_right:
            # Simple visualization of density vs modulus for context
            fig_lat = px.bar(engine.data, x='Element', y='Lattice_a', color='CrystalStructure', title="Global Lattice Comparison (pm)")
            st.plotly_chart(fig_lat, use_container_width=True)

    with t3:
        st.subheader("Multi-Factor Property Analysis")
        fig = px.scatter(
            engine.data, 
            x="Density", 
            y="YoungsModulus", 
            size="ElectricalConductivity", 
            color="ThermalExpansion",
            hover_name="Element",
            text="Symbol",
            template="plotly_white",
            labels={"YoungsModulus": "Stiffness (GPa)", "Density": "Density (g/cm³)"}
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- DATA EXPORT ---
    st.divider()
    if st.button("Generate Technical Report (CSV)"):
        csv = engine.data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Report", csv, "element_report.csv", "text/csv")

if __name__ == "__main__":
    main()
