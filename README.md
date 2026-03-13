# Automated CFD Post-Processing & Visualization Pipeline

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![Ansys](https://img.shields.io/badge/Solver-Ansys%20Fluent-orange.svg)](https://www.ansys.com/products/fluids/ansys-fluent)
[![Library](https://img.shields.io/badge/Library-PyVista%20%7C%20Matplotlib-green.svg)](https://docs.pyvista.org/)

## Project Overview
This project provides a fully automated end-to-end pipeline for extracting, processing, and visualizing high-fidelity CFD (Computational Fluid Dynamics) data from ANSYS Fluent. 

In industrial CFD workflows, analyzing dozens of design points manually is prone to error and time-consuming. This toolkit automates the export of specific flow surfaces across multiple simulation cases and generates publication-quality comparisons of aerodynamic performance metrics like **Mach Number** and **Stagnation Pressure** across varying Reynolds numbers, Temperatures, and Turbulence Intensities.

## Key Features
*   **Automated Data Extraction:** Python-driven generation of Fluent journal files (`.jou`) to batch-export CGNS data from 20+ simulation cases without manual GUI interaction.
*   **High-Fidelity Interpolation:** Uses `SciPy` and `PyVista` to map unstructured CFD mesh data onto structured Cartesian and Polar grids for precise cross-case comparison.
*   **Multi-Variate Analysis:** Systematically compares three key physical parameters.
    *   **Reynolds Number ($Re$)**
    *   **Turbulence Intensity ($TI$)**
    *   **Stagnation Temperature ($T$)**
*   **Advanced Visualization:** 
    *   **Centerline Profiles:** Capturing flow evolution across specific Z-locations.
    *   **Downstream field Analysis:** Polar plots at specific radii to evaluate flow uniformity.
    *   **Normalized Contours:** Comparison of stagnation pressure recovery ($P/P_{inlet}$).

## Tech Stack
*   **Core:** Python
*   **CFD Solver:** ANSYS Fluent (v23.2)
*   **Data Handling:** NumPy, SciPy (Griddata interpolation)
*   **Visualization:** Matplotlib (Multi-panel layouts), PyVista (VTK-based mesh processing)
*   **Automation:** Subprocess (Fluent CLI integration), Pathlib

## 📊 Technical Analysis & Results
The automated pipeline generates a 4x3 matrix of analytical plots, systematically evaluating the flow field's sensitivity to four physical parameters (**$Re, TI, T, M$**) across three distinct visualization perspectives.

### 1. Axial Flow Development (Centerline Analysis)
**Objective:** To quantify flow acceleration and stagnation pressure recovery through the geometry.
*   **Visualization:** 4-panel subplots featuring a full-domain overview (bottom) and three high-resolution zoomed views of the inlet, throat, and recovery zones (top).
*   **Key Observations:** 
    *   **Reynolds Sensitivity:** Higher $Re$ numbers (red lines) demonstrate delayed pressure recovery, indicating thinner boundary layers and reduced viscous dissipation.
    *   **Mach Number:** The centerline Mach profile captures the transition from subsonic to transonic regimes, with clear visualization of the "jump" across the $x=0mm$ plane.
    *   **Normalization:** Stagnation pressure is normalized by inlet conditions ($P/P_{inlet}$), allowing for an "apples-to-apples" comparison of efficiency across varying operating pressures.

### 2. Transverse Wake Characteristics (Downstream Profiles)
**Objective:** To evaluate the uniformity and symmetry of the flow field downstream of the test section.
*   **Visualization:** 3-panel layout comparing profiles along the **X-axis**, **Y-axis**, and a **Polar transformation** at a constant radius ($r = 21mm$).
*   **Key Observations:**
    *   **Wake Topology:** The X and Y profiles reveal a multi-lobed wake structure. Variations in Turbulence Intensity ($TI$) significantly alter the depth of these wake deficits, with higher $TI$ promoting faster mixing and wake recovery.
    *   **Azimuthal Uniformity:** The polar plots provide a "circumferential" view of the flow. Recruiters in turbomachinery or aerospace look for this specific analysis to understand how downstream components (like blades or probes) would be loaded.

### 3. Stagnation Pressure Topology (Normalized Contours)
**Objective:** To visualize the 2D shape and magnitude of energy losses ($P_{stag}$ drop).
*   **Visualization:** Combined contour plots at a fixed recovery level (e.g., $P_{norm} = 0.90$). This features a "Master Overlay" for direct comparison and individual sub-grids for each case.
*   **Key Observations:**
    *   **Separation Zones:** The contours clearly map the "pressure islands" where energy loss is most significant. 
    *   **Temperature Effects:** Analysis shows that while Mach profiles remain relatively consistent across different temperatures, the stagnation pressure distribution shifts, reflecting changes in air density and kinematic viscosity.

## Repository Structure
*   `Fluent_data_export.py`: Automates the ANSYS Fluent export process by generating journals and managing the CLI lifecycle.
*   `Post_processing_functions.py`: The core engine containing interpolation logic, polar transformations, and specialized plotting routines.
*   `Post-processing.py`: The entry point script that orchestrates the analysis for all study groups (TI, Re, Temp).
*   `Fluent_local_no_gui.py`: A utility script for launching Fluent in background mode for local environments.

## Engineering Insights Demonstrated
*   **Efficiency:** Reduced post-processing time by ~90% compared to manual export methods.
*   **Accuracy:** Implemented linear interpolation to ensure data from different mesh densities could be compared on a 1:1 basis.
*   **Scalability:** The architecture allows for adding new simulation cases by simply updating a list of file paths.

---

### How to Use
1.  **Export Data:** Ensure ANSYS Fluent is in your system path. Run `python Fluent_data_export.py` to generate CGNS files from your `.cas.h5` files.
2.  **Generate Plots:** Run `python Post-processing.py`. The script will crawl the `Data-analysis_files` directory and output plots into `Data-analysis_results`.

---

## Author
**[Akash Mishra]**
*   [linkedin.com/in/ak587]
