import paramiko
from pathlib import Path

# -----------------------------
# CHANGE THESE
# -----------------------------
HPC_HOST = "hpc2013.hpc.iitk.ac.in"
HPC_USER = "makash24"

ROOT = Path.cwd()

# ==============================
# FOLDER CONFIGURATION
# Each entry:
#   remote folder
#   local subfolder
#   base filename
# ==============================
FOLDERS= [

    {
        "remote": "/home/makash24/Analysis/Mach-analysis/TI_5_SST-K-Omega_small_yplus/run_44370.54Pa",
        "local_subfolder": "Mach-analysis",
        "base_name": "M0.45_TI5_T300K_2bar",
    },
    {
        "remote": "/home/makash24/Analysis/Mach-analysis/TI_5_SST-K-Omega_small_yplus/run_32057.72Pa",
        "local_subfolder": "Mach-analysis",
        "base_name": "M0.47_TI5_T300K_2bar",
    },
    {
        "remote": "/home/makash24/Analysis/Re-analysis/M0.39_TI10/PIN_2bar",
        "local_subfolder": "Re-analysis",
        "base_name": "2bar_M0.4_TI10_T300K",
    },
]

# -----------------------------
# CONNECT
# -----------------------------
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HPC_HOST, username=HPC_USER, password="Ak@sh587")

sftp = ssh.open_sftp()

# ==============================
# DOWNLOAD LOOP
# ==============================

for folder in FOLDERS:

    remote_folder = folder["remote"]
    local_folder = ROOT / folder["local_subfolder"]
    base_name = folder["base_name"]

    local_folder.mkdir(parents=True, exist_ok=True)

    print(f"\nScanning {remote_folder}")

    try:
        files = sftp.listdir(remote_folder)
    except FileNotFoundError:
        print("Folder not found. Skipping.")
        continue

    for file in files:

        if file.endswith(".cas.h5"):
            new_name = base_name + ".cas.h5"

        elif file.endswith(".dat.h5"):
            new_name = base_name + ".dat.h5"

        else:
            continue

        remote_path = remote_folder + "/" + file
        local_path = local_folder / new_name

        print("Downloading:", file)
        print("Saving as:", local_path)

        sftp.get(remote_path, str(local_path))

# ==============================
# CLOSE CONNECTION
# ==============================

sftp.close()
ssh.close()

print("\nAll downloads completed.")

# Archive
# FOLDERS = [
#     {
#         "remote": "/home/makash24/Analysis/TI-analysis/TI_5",
#         "local_subfolder": "Temperature-analysis",
#         "base_name": "T300K_M0.4_TI5_2bar",
#     },    
#     {
#         "remote": "/home/makash24/Analysis/Temperature-analysis/T350K",
#         "local_subfolder": "Temperature-analysis",
#         "base_name": "T350K_M0.4_TI5_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Temperature-analysis/T400K",
#         "local_subfolder": "Temperature-analysis",
#         "base_name": "T400K_M0.4_TI5_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Temperature-analysis/T600K_M0.4",
#         "local_subfolder": "Temperature-analysis",
#         "base_name": "T600K_M0.4_TI5_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Temperature-analysis/T600K_M0.45",
#         "local_subfolder": "Temperature-analysis",
#         "base_name": "T600K_M0.45_TI5_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Re-analysis/M0.39/PIN_2bar",
#         "local_subfolder": "TI-analysis",
#         "base_name": "TI0.1_M0.4_T300K_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/TI-analysis/TI_1",
#         "local_subfolder": "TI-analysis",
#         "base_name": "TI1_M0.4_T300K_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/TI-analysis/TI_5",
#         "local_subfolder": "TI-analysis",
#         "base_name": "TI5_M0.4_T300K_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Re-analysis/M0.39_TI10/PIN_2bar",
#         "local_subfolder": "TI-analysis",
#         "base_name": "TI10_M0.4_T300K_2bar",
#     },   
#     {
#         "remote": "/home/makash24/Analysis/Mach-analysis/TI_5_SST-K-Omega_small_yplus/run_100000Pa",
#         "local_subfolder": "Mach-analysis",
#         "base_name": "M0.076_TI5_T300K_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Mach-analysis/TI_5_SST-K-Omega_small_yplus/run_85000Pa",
#         "local_subfolder": "Mach-analysis",
#         "base_name": "M0.26_TI5_T300K_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Mach-analysis/TI_5_SST-K-Omega_small_yplus/run_61412.5Pa",
#         "local_subfolder": "Mach-analysis",
#         "base_name": "M0.4_TI5_T300K_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Mach-analysis/TI_5_SST-K-Omega_small_yplus/run_44370.54Pa",
#         "local_subfolder": "Mach-analysis",
#         "base_name": "M0.45_TI5_T300K_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Mach-analysis/TI_5_SST-K-Omega_small_yplus/run_32057.72Pa",
#         "local_subfolder": "Mach-analysis",
#         "base_name": "M0.47_TI5_T300K_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Mach-analysis/TI_5_SST-K-Omega_small_yplus/run_23161.7Pa",
#         "local_subfolder": "Mach-analysis",
#         "base_name": "M0.48_TI5_T300K_2bar",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Re-analysis/M0.39_TI10/PIN_1bar",
#         "local_subfolder": "Re-analysis",
#         "base_name": "1bar_M0.4_TI10_T300K",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Re-analysis/M0.39_TI10/PIN_2bar",
#         "local_subfolder": "Re-analysis",
#         "base_name": "2bar_M0.4_TI10_T300K",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Re-analysis/M0.39_TI10/PIN_5bar",
#         "local_subfolder": "Re-analysis",
#         "base_name": "5bar_M0.4_TI10_T300K",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Re-analysis/M0.39_TI10/PIN_10bar",
#         "local_subfolder": "Re-analysis",
#         "base_name": "10bar_M0.4_TI10_T300K",
#     },
#     {
#         "remote": "/home/makash24/Analysis/Re-analysis/M0.39_TI10/PIN_20bar",
#         "local_subfolder": "Re-analysis",
#         "base_name": "20bar_M0.4_TI10_T300K",
#     },
# ]
