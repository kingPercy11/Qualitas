
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HALSTEAD_PATH = os.path.join(CURRENT_DIR, "Metrics", "PY")
sys.path.append(HALSTEAD_PATH)

from halstead import run_halstead_analysis  

def get_user_input():
    """Take project directory, ignore list, and output directory from user."""
    project_dir = input("Enter project directory path to analyze: ").strip()
    while not os.path.exists(project_dir):
        print("Directory not found. Try again.")
        project_dir = input("Enter project directory path to analyze: ").strip()

    ignore_input = input("Enter comma-separated folder/file names to ignore: ").strip()
    ignore_dirs = set(map(str.strip, ignore_input.split(","))) if ignore_input else set()

    output_dir = input("Enter directory path to save CSV report: ").strip()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created directory: {output_dir}")

    output_csv = os.path.join(output_dir, "halstead_report.csv")

    return project_dir, ignore_dirs, output_csv


def run_quality_metrics():
    """Main entry function for running project quality metrics."""
    print("\n=== Project Quality Metrics ===\n")
    project_dir, ignore_dirs, output_csv = get_user_input()

    print("\nRunning Halstead Complexity Analysis...\n")
    run_halstead_analysis(project_dir, ignore_dirs, output_csv)

    print("\nAnalysis complete.")


if __name__ == "__main__":
    run_quality_metrics()