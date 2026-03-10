import os
import re
import csv
import matplotlib.pyplot as plt

# ================= CONFIGURATION =================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
FOLDER_PATH = os.path.join(SCRIPT_DIR, "Fluent_results")  # Define folder path relative to script location
LOG_FILE_PATH = os.path.join(FOLDER_PATH, "fluent_output.log")  # Define log file path relative to folder
# =================================================


def parse_header_line(line):
    """Extract column headers from a header line."""
    quoted_headers = re.findall(r'"(.*?)"', line)
    if len(quoted_headers) >= 2:
        return quoted_headers[0], quoted_headers[1]

    parts = line.strip().split()
    if len(parts) >= 2:
        return parts[0], parts[1]

    return "X", "Y"


def plot_out_file(file_path):
    """
    Reads a Fluent .out file, plots data,
    and returns final converged values.
    """
    try:
        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        x_label, y_label = "X", "Y"
        data_start_index = -1

        # Locate first numeric data line
        for i, line in enumerate(lines):
            try:
                float(line.split()[0])
                data_start_index = i
                break
            except Exception:
                continue

        if data_start_index == -1:
            print(f"Skipping {os.path.basename(file_path)} (no numeric data)")
            return None

        # Header line is assumed just above data
        if data_start_index > 0:
            x_label, y_label = parse_header_line(lines[data_start_index - 1])

        x_data, y_data = [], []

        for line in lines[data_start_index:]:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    x_data.append(float(parts[0]))
                    y_data.append(float(parts[1]))
                except ValueError:
                    continue

        if not x_data:
            print(f"Skipping {os.path.basename(file_path)} (empty data)")
            return None

        # ===== FINAL RESULT =====
        final_x = x_data[-1]
        final_y = y_data[-1]

        # ===== PLOTTING =====
        plt.figure(figsize=(10, 6))
        plt.plot(x_data, y_data, label=y_label)
        plt.xlabel(x_label.replace("-", " ").title())
        plt.ylabel(y_label.replace("-", " ").title())
        plt.title(f"{y_label} vs {x_label}")
        plt.grid(True)
        plt.legend()

        png_path = file_path.rsplit(".", 1)[0] + ".png"
        plt.savefig(png_path, dpi=150)
        plt.close()

        return {
            "file": os.path.basename(file_path),
            "x_label": x_label,
            "y_label": y_label,
            "final_x": final_x,
            "final_y": final_y,
            "png": png_path
        }

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def process_folder(folder):
    """Process all .out files and extract final results."""
    out_files = [f for f in os.listdir(folder) if f.endswith(".out")]

    if not out_files:
        print("No .out files found.")
        return []

    results = []

    print(f"Processing {len(out_files)} .out files...\n")

    for fname in out_files:
        path = os.path.join(folder, fname)
        result = plot_out_file(path)
        if result:
            results.append(result)
            print(
                f"{result['file']}: "
                f"{result['y_label']} = {result['final_y']} "
                f"({result['x_label']} = {result['final_x']})"
            )

    return results


def save_final_results_csv(results, output_path):
    """Save final results to CSV with fixed 8 decimal places."""
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["File", "X Label", "Final X", "Y Label", "Final Y"])

        for r in results:
            writer.writerow([
                r["file"],
                r["x_label"],
                f"{r['final_x']:.8f}",
                r["y_label"],
                f"{r['final_y']:.8f}"
            ])

    print(f"\nFinal results written to: {output_path}")


def plot_residuals_from_log(log_file_path):
    """Plot Fluent residuals from .log file."""
    iterations = []
    residuals = {
        "continuity": [],
        "x-velocity": [],
        "y-velocity": [],
        "z-velocity": [],
        "energy": [],
        "k": [],
        "omega": []
    }

    pattern = re.compile(
        r"^\s*(\d+)\s+([-+eE0-9.]+)\s+([-+eE0-9.]+)\s+([-+eE0-9.]+)\s+"
        r"([-+eE0-9.]+)\s+([-+eE0-9.]+)\s+([-+eE0-9.]+)\s+([-+eE0-9.]+)"
    )

    with open(log_file_path, "r") as f:
        for line in f:
            m = pattern.match(line)
            if m:
                iterations.append(int(m.group(1)))
                for i, key in enumerate(residuals.keys(), start=2):
                    residuals[key].append(float(m.group(i)))

    plt.figure(figsize=(10, 7))
    for key, vals in residuals.items():
        plt.plot(iterations, vals, label=key)

    plt.yscale("log")
    plt.xlabel("Iteration")
    plt.ylabel("Residual")
    plt.title("Residual Convergence History")
    plt.grid(True, which="both")
    plt.legend()

    out_path = log_file_path.rsplit(".", 1)[0] + "_residuals.png"
    plt.savefig(out_path, dpi=150)
    plt.close()

    print(f"Residual plot saved to: {out_path}")


# ===================== MAIN ======================
if __name__ == "__main__":
    results = process_folder(FOLDER_PATH)

    if results:
        csv_path = os.path.join(FOLDER_PATH, "final_results.csv")
        save_final_results_csv(results, csv_path)

    plot_residuals_from_log(LOG_FILE_PATH)
