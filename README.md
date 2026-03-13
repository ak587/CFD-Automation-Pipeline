# Automated CFD Post-Processing & Sensitivity Analysis Pipeline

This repository showcases an end-to-end automated pipeline for extracting, processing, and visualizing high-volume computational fluid dynamics (CFD) data. Using **Ansys Fluent**, **Python (PyVista/SciPy)**, and **Matplotlib**, the project analyzes flow field sensitivity across varying Mach numbers, Reynolds numbers, Turbulence Intensities (TI), and Temperatures.

## Project Overview

The core challenge addressed here is the efficient analysis of multiple CFD simulation cases. Instead of manual post-processing, this project utilizes:
1.  **Fluent Automation**: Python-generated Journal files to batch-export 2D surface data in `.cgns` format.
2.  **Data Processing**: A custom Python library to handle 3D mesh interpolation, coordinate transformations (Cartesian to Polar), and normalization.
3.  **Visualization**: Automated generation of comparative plots to identify physical trends in wakes and pressure drops.

---

## Technical Stack
*   **Simulation**: Ansys Fluent (v23.2)
*   **Automation**: Python (Subprocess, Pathlib)
*   **Data Handling**: PyVista (VTK-based mesh processing), NumPy, SciPy (Linear Interpolation)
*   **Visualization**: Matplotlib (Multi-axis subplots)

---

## Analysis & Visualization Explained

The pipeline generates three primary types of visualizations to characterize the flow, likely through a screen or grid.

### 1. Centerline Profiles (Axial Development)

1. Mach Profile Centerlines

<p align="center">
  <img src="Data-analysis_results/Field_variables/TI/Mach_Profile_Centerline.png" width="32%">
  <img src="Data-analysis_results/Field_variables/Re/Mach_Profile_Centerline.png" width="32%">
  <img src="Data-analysis_results/Field_variables/Temperature/Mach_Profile_Centerline.png" width="32%">
</p>

2. Normalized Stagnation Pressure Centerline

<p align="center">
  <img src="Data-analysis_results/Field_variables/TI/PressureStagnation_Profile_Centerline" width="32%">
  <img src="Data-analysis_results/Field_variables/Re/PressureStagnation_Profile_Centerline" width="32%">
  <img src="Data-analysis_results/Field_variables/Temperature/PressureStagnation_Profile_Centerline" width="32%">
</p>

These plots track the evolution of the flow along the $Z$-axis (flow direction).
*   **What it shows**: The transition from inlet conditions through a perforated screen (at $z=0$) into the downstream recovery region.
*   **Key Insight**: By normalizing Stagnation Pressure, we can precisely quantify the pressure loss coefficient of the grid. The Mach number plots reveal the local acceleration as the flow is constricted through the "screen" geometry.

### 2. Downstream Spatial Profiles (X-Y & Polar)

1. Mach Profile downstream

<p align="center">
  <img src="Data-analysis_results/Field_variables/TI/Mach_Profile_downstream" width="32%">
  <img src="Data-analysis_results/Field_variables/Re/Mach_Profile_downstream" width="32%">
  <img src="Data-analysis_results/Field_variables/Temperature/Mach_Profile_downstream" width="32%">
</p>

2. Normalized Stagnation Pressure downstream

<p align="center">
  <img src="Data-analysis_results/Field_variables/TI/PressureStagnation_Profile_downstream.png" width="32%">
  <img src="Data-analysis_results/Field_variables/Re/PressureStagnation_Profile_downstream.png" width="32%">
  <img src="Data-analysis_results/Field_variables/Temperature/PressureStagnation_Profile_downstream.png" width="32%">
</p>

Flow data is extracted from 2D slices downstream of the disturbance.
*   **Cartesian Profiles**: These 2D slices 1D (50mm) downstream of the screen show the periodic Mach deficits caused by the grid.
*   **Polar Profiles**: Mach is sampled at a constant radius ($r = 0.021m$). 
*   **Key Insight**: This is critical for identifying **azimuthal non-uniformity**. It proves whether the flow distorts more in the center or near the duct walls.

### 3. Normalized Stagnation Pressure Contours
Combined contour plots (Reynolds sweep)

![Turbulent Intensity](Data-analysis_results/Combined_Contour_plot/Re/0.90-PressureStagnation_Contour_plots.png)

A comparative look at how Reynolds Number ($Re$) affects the distortion.
*   **What it shows**: Iso-contours of $P_{norm} = 0.90$. 
*   **Key Insight**: As Reynolds number increases, the "islands" of pressure deficit change shape. This visualizes the sensitivity of the separation zones to the inertial-to-viscous force ratio.

---

## Code Structure

### `Fluent_data_export.py`
Automates the "boring" part. It iterates through 21+ simulation case files, creates plane surfaces at specific $d$ (diameters) upstream and downstream, and exports variables (Velocity, Mach, Pressure) to CGNS format.

### `Post_processing_functions.py`
The mathematical engine of the project:
*   **`load_meshes()`**: Efficiently organizes and loads dozens of CGNS files into PyVista objects.
*   **`griddata` Interpolation**: Maps unstructured CFD data onto a uniform grid for clean plotting.
*   **Modular Plotters**: Functions like `downstream_plot` and `centerline_plot` allow the same logic to be applied to any variable (Mach, TI, etc.) with a single call.

### `Post-processing.py`
The main execution script. It manages the metadata (labels, folder structures) and triggers the visualization suite for each study (Mach analysis, Re analysis, etc.).

---

## Key Results Highlight
*   **Reynolds Sensitivity**: The analysis revealed that higher Reynolds numbers result in more distinct, narrower wakes, suggesting reduced lateral mixing.
*   **Temperature Effects**: Mach number profiles remained consistent across temperatures when normalized, confirming the robustness of the non-dimensional analysis.
*   **Automation Efficiency**: Reduced post-processing time from hours of manual labor to a **3-minute automated execution**.

---

## How to Use
1.  **Export**: Run `Fluent_data_export.py` (requires Ansys Fluent installed).
2.  **Process**: Ensure data is in the `/Data-analysis_files/` folder.
3.  **Visualize**: Run `Post-processing.py` to generate all plots in the `/Data-analysis_results/` directory.
