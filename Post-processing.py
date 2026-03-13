import numpy as np
from Post_processing_functions import load_meshes, downstream_plot, centerline_plot, contour_plot

ROOT, Mach_meshes_slice, Mach_meshes_upstream_1d, Mach_meshes_upstream_2d, Mach_meshes_downstream_1d, Mach_meshes_downstream_2d, Mach_meshes_downstream_3d, Mach_meshes_downstream_4d, Mach_meshes_downstream_5d, \
        Re_meshes_slice, Re_meshes_upstream_1d, Re_meshes_upstream_2d, Re_meshes_downstream_1d, Re_meshes_downstream_2d, Re_meshes_downstream_3d, Re_meshes_downstream_4d, Re_meshes_downstream_5d, \
        Temperature_meshes_slice, Temperature_meshes_upstream_1d, Temperature_meshes_upstream_2d, Temperature_meshes_downstream_1d, Temperature_meshes_downstream_2d, Temperature_meshes_downstream_3d, Temperature_meshes_downstream_4d, Temperature_meshes_downstream_5d, \
        TI_meshes_slice, TI_meshes_upstream_1d, TI_meshes_upstream_2d, TI_meshes_downstream_1d, TI_meshes_downstream_2d, TI_meshes_downstream_3d, TI_meshes_downstream_4d, TI_meshes_downstream_5d = load_meshes()

# Arguments for plotting
# Labels
Mach_labels = ['M=0.08', 'M=0.26', 'M=0.4', 'M=0.45', 'M=0.47', 'M=0.48']
TI_labels = ['TI=0.1', 'TI=1', 'TI=5', 'TI=10']
Temperature_labels = ['T=300K', 'T=350K', 'T=400K', 'T=600K_M0.4', 'T=300K_M0.45', 'T=600K_M0.45']
Re_labels = ['Re=4.1e5', 'Re=8.3e5', 'Re=2.1e6', 'Re=4.2e6', 'Re=8.3e6']

# Field variables
field_variables = ["Mach", "PressureStagnation"]
field_meshes_down = [TI_meshes_downstream_1d, Temperature_meshes_downstream_1d, Re_meshes_downstream_1d]
field_meshes_slice = [TI_meshes_slice, Temperature_meshes_slice, Re_meshes_slice]
field_labels = [TI_labels, Temperature_labels, Re_labels]
variable_folders = ["TI", "Temperature", "Re"]

# Field Variable Plots ----------------------------------------------------------------------------------------------------------------------
for meshes_down, meshes_slice, labels, folder in zip(field_meshes_down, field_meshes_slice, field_labels, variable_folders):
    (ROOT / "Data-analysis_results" / "Field_variables" / folder).mkdir(parents=True, exist_ok=True)
    for field_name in field_variables:
        downstream_plot(meshes_down, meshes_slice, field_name, labels, "Field_variables", folder)
        centerline_plot(meshes_slice, field_name, labels, "Field_variables", folder)

# Pressure Contour downstream plots
print(Re_meshes_downstream_1d[0].point_data.keys())
(ROOT / "Data-analysis_results" / "Combined_Contour_plot" / "Re").mkdir(parents=True, exist_ok=True)
contour_plot(Re_meshes_downstream_1d, Re_meshes_slice, "PressureStagnation", Re_labels, "Combined_Contour_plot", "Re")



