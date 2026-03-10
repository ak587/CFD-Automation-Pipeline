from pathlib import Path 
import subprocess

FLUENT_EXE = Path(r"C:\Program Files\ANSYS Inc\v232\fluent\ntbin\win64\fluent.exe")
cmd = [
    str(FLUENT_EXE),
    "3ddp",
    "-g",
    "-t1",
]

print("Launching Fluent...")
subprocess.run(cmd)

print("Done.")
