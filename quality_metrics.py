import os
import sys

# === Setup paths ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS_PATH = os.path.join(CURRENT_DIR, "Metrics", "PY")
sys.path.append(METRICS_PATH)

# === Imports ===
from halstead import run_halstead_analysis
from information_flow import run_information_flow_analysis
from live_variables import run_live_variable_analysis


def get_user_input():
    project_dir = input("Enter project directory path to analyze: ").strip()
    while not os.path.exists(project_dir):
        print("Directory not found. Try again.")
        project_dir = input("Enter project directory path to analyze: ").strip()

    ignore_input = input("Enter comma-separated folder/file names to ignore: ").strip()
    ignore_dirs = set(map(str.strip, ignore_input.split(","))) if ignore_input else set()

    output_dir = input("Enter directory path to save CSV reports: ").strip()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Paths for all reports
    halstead_csv = os.path.join(output_dir, "halstead_report.csv")
    infoflow_csv = os.path.join(output_dir, "information_flow_metrics.csv")
    livevar_csv = os.path.join(output_dir, "live_variables_report.csv")

    return project_dir, ignore_dirs, halstead_csv, infoflow_csv, livevar_csv


def run_quality_metrics(project_dir=None, ignore_dirs=None, output_dir=None):
    if not project_dir:
        project_dir = input("Enter project directory: ").strip()
    if not ignore_dirs:
        ignore_input = input("Enter comma-separated folders to ignore: ").strip()
        ignore_dirs = set(map(str.strip, ignore_input.split(","))) if ignore_input else set()
    if not output_dir:
        output_dir = input("Enter output directory for CSVs: ").strip()

    os.makedirs(output_dir, exist_ok=True)

    halstead_csv = os.path.join(output_dir, "halstead_report.csv")
    infoflow_csv = os.path.join(output_dir, "information_flow_metrics.csv")
    livevar_csv = os.path.join(output_dir, "live_variable_metrics.csv")

    print("\nRunning Halstead Analysis...")
    run_halstead_analysis(project_dir, ignore_dirs, halstead_csv)

    print("\nRunning Information Flow Analysis...")
    run_information_flow_analysis(project_dir, ignore_dirs, infoflow_csv)

    print("\nRunning Live Variable Analysis...")
    run_live_variable_analysis(project_dir, ignore_dirs, livevar_csv)

    print("\nAll analyses complete!")

    return {
        "halstead": halstead_csv,
        "information_flow": infoflow_csv,
        "live_variables": livevar_csv
    }


if __name__ == "__main__":
    run_quality_metrics()