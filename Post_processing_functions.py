from importlib.metadata import files
import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from pathlib import Path

# Loading Data
ROOT = Path.cwd()
def load_meshes():
    Mach_files = [ROOT / "Data-analysis_files" / "Mach_files" / f for f in ["M0.076_TI5_T300K_2bar_down.cgns", "M0.26_TI5_T300K_2bar_down.cgns", "M0.4_TI5_T300K_2bar_down.cgns", 
                "M0.45_TI5_T300K_2bar_down.cgns","M0.47_TI5_T300K_2bar_down.cgns", "M0.48_TI5_T300K_2bar_down.cgns", "M0.076_TI5_T300K_2bar_up.cgns", "M0.26_TI5_T300K_2bar_up.cgns", 
                "M0.4_TI5_T300K_2bar_up.cgns","M0.45_TI5_T300K_2bar_up.cgns","M0.47_TI5_T300K_2bar_up.cgns", "M0.48_TI5_T300K_2bar_up.cgns", "M0.076_TI5_T300K_2bar_slice.cgns", 
                "M0.26_TI5_T300K_2bar_slice.cgns", "M0.4_TI5_T300K_2bar_slice.cgns", "M0.45_TI5_T300K_2bar_slice.cgns","M0.47_TI5_T300K_2bar_slice.cgns", 
                "M0.48_TI5_T300K_2bar_slice.cgns"]]

    TI_files = [ROOT /  "Data-analysis_files" / "TI_files" / f for f in ["TI0.1_M0.4_T300K_2bar_down.cgns", "TI1_M0.4_T300K_2bar_down.cgns", "TI5_M0.4_T300K_2bar_down.cgns", 
                "TI10_M0.4_T300K_2bar_down.cgns","TI0.1_M0.4_T300K_2bar_up.cgns", "TI1_M0.4_T300K_2bar_up.cgns", "TI5_M0.4_T300K_2bar_up.cgns", "TI10_M0.4_T300K_2bar_up.cgns", 
                "TI0.1_M0.4_T300K_2bar_slice.cgns", "TI1_M0.4_T300K_2bar_slice.cgns", "TI5_M0.4_T300K_2bar_slice.cgns", "TI10_M0.4_T300K_2bar_slice.cgns"]]

    Temperature_files = [ROOT / "Data-analysis_files" / "Temperature_files" / f for f in ["T300K_M0.4_TI5_2bar_down.cgns", "T350K_M0.4_TI5_2bar_down.cgns",
                        "T400K_M0.4_TI5_2bar_down.cgns", "T600K_M0.4_TI5_2bar_down.cgns", "T300K_M0.45_TI5_2bar_down.cgns", "T600K_M0.45_TI5_2bar_down.cgns", 
                        "T300K_M0.4_TI5_2bar_up.cgns", "T350K_M0.4_TI5_2bar_up.cgns", "T400K_M0.4_TI5_2bar_up.cgns", "T600K_M0.4_TI5_2bar_up.cgns", "T300K_M0.45_TI5_2bar_up.cgns", 
                        "T600K_M0.45_TI5_2bar_up.cgns", "T300K_M0.4_TI5_2bar_slice.cgns", "T350K_M0.4_TI5_2bar_slice.cgns", "T400K_M0.4_TI5_2bar_slice.cgns", 
                        "T600K_M0.4_TI5_2bar_slice.cgns", "T300K_M0.45_TI5_2bar_slice.cgns", "T600K_M0.45_TI5_2bar_slice.cgns"]]   

    Re_files = [ROOT / "Data-analysis_files" / "Re_files" / f for f in ["1bar_M0.4_TI10_T300K_down.cgns", "2bar_M0.4_TI10_T300K_down.cgns", "5bar_M0.4_TI10_T300K_down.cgns", 
                "10bar_M0.4_TI10_T300K_down.cgns","20bar_M0.4_TI10_T300K_down.cgns","1bar_M0.4_TI10_T300K_up.cgns", "2bar_M0.4_TI10_T300K_up.cgns", "5bar_M0.4_TI10_T300K_up.cgns", 
                "10bar_M0.4_TI10_T300K_up.cgns", "20bar_M0.4_TI10_T300K_up.cgns", "1bar_M0.4_TI10_T300K_slice.cgns", "2bar_M0.4_TI10_T300K_slice.cgns", 
                "5bar_M0.4_TI10_T300K_slice.cgns", "10bar_M0.4_TI10_T300K_slice.cgns", "20bar_M0.4_TI10_T300K_slice.cgns"]]

    Mach_meshes_down = [pv.read(file).combine() for file in Mach_files[0:6]]   # Down (first 6 files), Up (next 6 files), Slice (last 6 files)
    Mach_meshes_up = [pv.read(file).combine() for file in Mach_files[6:12]]
    Mach_meshes_slice = [pv.read(file).combine() for file in Mach_files[12:18]]

    TI_meshes_down = [pv.read(file).combine() for file in TI_files[0:4]]   # Down (first 4 files), Up (next 4 files), Slice (last 4 files)
    TI_meshes_up = [pv.read(file).combine() for file in TI_files[4:8]]
    TI_meshes_slice = [pv.read(file).combine() for file in TI_files[8:12]]

    Temperature_meshes_down = [pv.read(file).combine() for file in Temperature_files[0:6]]   # Down (first 6 files), Up (next 6 files), Slice (last 6 files)
    Temperature_meshes_up = [pv.read(file).combine() for file in Temperature_files[6:12]]
    Temperature_meshes_slice = [pv.read(file).combine() for file in Temperature_files[12:18]]

    Re_meshes_down = [pv.read(file).combine() for file in Re_files[1:5]]   # Down (first 5 files), Up (next 5 files), Slice (last 5 files)
    Re_meshes_up = [pv.read(file).combine() for file in Re_files[6:10]]
    Re_meshes_slice = [pv.read(file).combine() for file in Re_files[11:15]]
    return ROOT, Mach_meshes_down, Mach_meshes_up, Mach_meshes_slice, TI_meshes_down, TI_meshes_up, TI_meshes_slice, Temperature_meshes_down, \
        Temperature_meshes_up, Temperature_meshes_slice, Re_meshes_down, Re_meshes_up, Re_meshes_slice

# Helper Functions
def polar_meshgrid(mesh):
    r = np.sqrt(mesh.points[:, 0]**2 + mesh.points[:, 1]**2)
    theta = np.arctan2(mesh.points[:, 1], mesh.points[:, 0])
    theta = np.mod(theta, 2*np.pi)
    ri = np.linspace(r.min(), r.max(), 200)
    thetai = np.linspace(0, 2*np.pi, 360, endpoint=False)
    Ri, Thetai = np.meshgrid(ri, thetai)
    return r, theta, ri, thetai, Ri, Thetai

def cartesian_meshgrid(mesh):
    xmin, xmax, ymin, ymax = mesh.bounds[0], mesh.bounds[1], mesh.bounds[2], mesh.bounds[3]
    xi = np.linspace(xmin, xmax, 200)
    yi = np.linspace(ymin, ymax, 200)
    Xi, Yi = np.meshgrid(xi, yi)
    return xi, yi, Xi, Yi

def cartesian_meshgrid_slice(mesh):
    ymin, ymax, zmin, zmax = mesh.bounds[2], mesh.bounds[3], mesh.bounds[4], mesh.bounds[5]
    yi = np.linspace(ymin, ymax, 200)
    zi = np.linspace(zmin, zmax, 1420)
    Yi, Zi = np.meshgrid(yi, zi)
    return yi, zi, Yi, Zi

# Interpolate inlet pressure at z=0, y=0 correspoiding to [1, 100] for normalization
def import_inlet_pressure(meshes_slice):
    inlet_pressures = []
    for mesh in meshes_slice:
        _, _, Yi, Zi = cartesian_meshgrid_slice(mesh)
        pressure_grid = griddata((mesh.points[:, 1], mesh.points[:, 2]), mesh.point_data["PressureStagnation"], (Yi, Zi), method="linear")
        inlet_pressures.append(pressure_grid[1, 100])
    return inlet_pressures

# Plotting Functions
def downstream_plot(meshes_down, meshes_slice, field_name, labels, folder, subfolder):
    colors = ['orange', 'green', 'blue', 'red', 'cyan', 'magenta']
    inlet_pressure = import_inlet_pressure(meshes_slice) if field_name == "PressureStagnation" else np.ones(len(meshes_slice))
    plt.figure(figsize=(14, 8))

    # Variable Profile along X-axis
    plt.subplot2grid((2, 2), (0, 0))
    for i, mesh, color, label in zip(range(len(meshes_down)), meshes_down, colors, labels):
        xi, yi, Xi, Yi = cartesian_meshgrid(mesh)
        if field_name == "Velocity":
            field_grid = griddata((mesh.points[:, 0], mesh.points[:, 1]), mesh.point_data[field_name][:, 2], (Xi, Yi), method="linear")
        else:
            field_grid = griddata((mesh.points[:, 0], mesh.points[:, 1]), mesh.point_data[field_name], (Xi, Yi), method="linear")
        yi_min = np.argmin(np.abs(yi))
        field_along_x_normalized = field_grid[yi_min, :] / inlet_pressure[i] if field_name == "PressureStagnation" else field_grid[yi_min, :]
        plt.plot(xi, field_along_x_normalized, color=color, label=label)
    plt.xlabel("x-location [m]")
    plt.ylabel(f"{field_name}_normalized" if field_name == "PressureStagnation" else field_name)
    plt.title(f"{field_name} Profile along X-axis")
    plt.grid()
    plt.legend()

    # Variable Profile along Y-axis
    plt.subplot2grid((2, 2), (0, 1))
    for i, mesh, color, label in zip(range(len(meshes_down)), meshes_down, colors, labels):
        xi, yi, Xi, Yi = cartesian_meshgrid(mesh)
        if field_name == "Velocity":
            field_grid = griddata((mesh.points[:, 0], mesh.points[:, 1]), mesh.point_data[field_name][:, 2], (Xi, Yi), method="linear")
        else:
            field_grid = griddata((mesh.points[:, 0], mesh.points[:, 1]), mesh.point_data[field_name], (Xi, Yi), method="linear")
        xi_min = np.argmin(np.abs(xi))
        field_along_y_normalized = field_grid[:, xi_min] / inlet_pressure[i] if field_name == "PressureStagnation" else field_grid[:, xi_min]
        plt.plot(yi, field_along_y_normalized, color=color, label=label)
    plt.xlabel("y-location [m]")
    plt.ylabel(f"{field_name}_normalized" if field_name == "PressureStagnation" else field_name)
    plt.title(f"{field_name} Profile along Y-axis")
    plt.grid()
    plt.legend()

    # Variable Profile in Polar Coordinates
    plt.subplot2grid((2, 2), (1, 0), colspan=2)
    r0 = 0.021
    for i, mesh, color, label in zip(range(len(meshes_down)), meshes_down, colors, labels):
        r, theta, ri, thetai, Ri, Thetai = polar_meshgrid(mesh)
        if field_name == "Velocity":
            field_polar = griddata((r, theta), mesh.point_data[field_name][:, 2], (Ri, Thetai), method="linear")
        else:
            field_polar = griddata((r, theta), mesh.point_data[field_name], (Ri, Thetai), method="linear")
        ir = np.argmin(np.abs(ri - r0))
        field_theta_normalized = field_polar[:, ir] / inlet_pressure[i] if field_name == "PressureStagnation" else field_polar[:, ir]
        plt.plot(thetai, field_theta_normalized, color=color, label=label)
    plt.xlabel("Theta (rad)")
    plt.ylabel(f"{field_name}_normalized" if field_name == "PressureStagnation" else field_name)
    plt.title(f"{field_name} at r = {r0} [m]")
    plt.grid()
    plt.legend()
    plt.savefig(ROOT / "Data-analysis_results" / folder / subfolder / f"{field_name}_profile_downstream.png")
    print(f"{subfolder}-{field_name} profile downstream created.")

def centerline_plot(meshes_slice, field_name, labels, folder, subfolder):
    colors = ['orange', 'green', 'blue', 'red', 'cyan', 'magenta']
    inlet_pressure = import_inlet_pressure(meshes_slice) if field_name == "PressureStagnation" else np.ones(len(meshes_slice))
    fig = plt.figure(figsize=(18, 10))
    ax0 = plt.subplot2grid((2, 3), (1, 0), colspan=3) # Bottom plot
    ax1 = plt.subplot2grid((2, 3), (0, 0))           # Top Left
    ax2 = plt.subplot2grid((2, 3), (0, 1))           # Top Mid
    ax3 = plt.subplot2grid((2, 3), (0, 2))           # Top Right
    all_axes = [ax0, ax1, ax2, ax3]
    
    for pressure_index, mesh, color, label in zip(range(len(meshes_slice)), meshes_slice, colors, labels):
        yi, zi, Yi, Zi = cartesian_meshgrid_slice(mesh)
        if field_name == "Velocity":
            field_grid = griddata((mesh.points[:, 1], mesh.points[:, 2]), mesh.point_data[field_name][:, 2], (Yi, Zi), method="linear")
        else:
            field_grid = griddata((mesh.points[:, 1], mesh.points[:, 2]), mesh.point_data[field_name], (Yi, Zi), method="linear")
        centerline = np.argmin(np.abs(yi))
        location = [np.s_[:], np.s_[380:400], np.s_[400:420], np.s_[420:440]]

        for location_index, loc in zip(range(len(location)), location):
            field_normalized = field_grid[loc, centerline] / inlet_pressure[pressure_index] if field_name == "PressureStagnation" else field_grid[loc, centerline]
            ax = all_axes[location_index]
            ax.plot(zi[loc], field_normalized, color=color, label=label)
            if location_index == 0 and pressure_index == 0:
                ax.axvline(x=-0.005, color='r', linestyle='--', label="x=-5mm")
                ax.axvline(x=0, color='b', linestyle='--', label="x=0mm")
                ax.axvline(x=0.005, color='g', linestyle='--', label="x=5mm")
                ax.axvline(x=0.01, color='c', linestyle='--', label="x=10mm")
            ax.set_xlabel("z-location [m]")
            ax.set_ylabel(f"{field_name}_normalized" if field_name == "PressureStagnation" else field_name)
            ax.set_title(f"Centerline {field_name} Profile")
    for ax in all_axes:
        ax.grid(True, which='both', linestyle='--', linewidth=0.5) # Explicitly turn on grid
        ax.legend()
    plt.tight_layout()
    plt.savefig(ROOT / "Data-analysis_results" / folder / subfolder / f"{field_name}_Profile_Centerline.png")
    print(f"{subfolder}-{field_name} centerline plot created.")

# Contour Plots
def contour_plot(meshes_down, meshes_slice, field_name, labels, folder, subfolder):
    colors = ['orange', 'green', 'blue', 'red', 'cyan', 'magenta']
    inlet_pressure = import_inlet_pressure(meshes_slice) if field_name == "PressureStagnation" else np.ones(len(meshes_slice))
    xi, yi, Xi, Yi = cartesian_meshgrid(meshes_down[0])

    # Variable Profile along X-axis
    plt.figure(figsize=(18, 8))     
    big = plt.subplot2grid((2, 4), (0, 0), rowspan=2, colspan=2)
    for i, (mesh, label, color) in enumerate(zip(meshes_down, labels, colors)):
        if field_name == "Velocity":
            field_grid = griddata((mesh.points[:, 0], mesh.points[:, 1]), mesh.point_data[field_name][:, 2], (Xi, Yi), method="linear")
        else:
            field_grid = griddata((mesh.points[:, 0], mesh.points[:, 1]), mesh.point_data[field_name], (Xi, Yi), method="linear")
        field_grid_normalized = field_grid / inlet_pressure[i]

        plt.sca(big)
        plt.contour(xi, yi, field_grid_normalized, levels=[1], colors=color)
        plt.title(f"Combined contour lines at P=0.9")
        plt.xlabel("x-location [m]")
        plt.ylabel("y-location [m]")
        plt.legend()

        plt.subplot2grid((2, 4), (0, i+2)) if i<2 else plt.subplot2grid((2, 4), (1, i))
        plt.contourf(xi, yi, field_grid_normalized)
        plt.xlabel("x-location [m]")
        plt.ylabel("y-location [m]")
        plt.title(f"{field_name} Cotour at {label}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(ROOT / "Data-analysis_results" /folder / subfolder / f"{field_name}_Contour_plots")
    print(f"{subfolder}-{field_name} contour plot created")




