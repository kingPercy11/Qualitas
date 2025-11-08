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
    """Take project directory, ignore list, and output directory from user."""
    project_dir = input("Enter project directory path to analyze: ").strip()
    while not os.path.exists(project_dir):
        print("❌ Directory not found. Try again.")
        project_dir = input("Enter project directory path to analyze: ").strip()

    ignore_input = input("Enter comma-separated folder/file names to ignore: ").strip()
    ignore_dirs = set(map(str.strip, ignore_input.split(","))) if ignore_input else set()

    output_dir = input("Enter directory path to save CSV reports: ").strip()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created directory: {output_dir}")

    # Paths for all reports
    halstead_csv = os.path.join(output_dir, "halstead_report.csv")
    infoflow_csv = os.path.join(output_dir, "information_flow_metrics.csv")
    livevar_csv = os.path.join(output_dir, "live_variables_report.csv")

    return project_dir, ignore_dirs, halstead_csv, infoflow_csv, livevar_csv


def run_quality_metrics():
    """Main entry function to run Halstead, Info Flow, and Live Variable metrics."""
    print("\n=== 🚀 Project Quality Metrics Suite ===\n")
    project_dir, ignore_dirs, halstead_csv, infoflow_csv, livevar_csv = get_user_input()

    print("\n🧮 Running Halstead Complexity Analysis...\n")
    run_halstead_analysis(project_dir, ignore_dirs, halstead_csv)

    print("\n🔄 Running Information Flow Analysis...\n")
    run_information_flow_analysis(project_dir, ignore_dirs, infoflow_csv)

    print("\n📊 Running Live Variable Analysis...\n")
    run_live_variable_analysis(project_dir, ignore_dirs, livevar_csv)

    print("\n✅ All analyses complete! Reports saved at:")
    print(f"   • {halstead_csv}")
    print(f"   • {infoflow_csv}")
    print(f"   • {livevar_csv}")


if __name__ == "__main__":
    run_quality_metrics()