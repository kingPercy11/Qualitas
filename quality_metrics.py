import os
import sys
import csv
from collections import Counter

# === Setup paths ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS_PATH = os.path.join(CURRENT_DIR, "Metrics", "PY")
sys.path.append(METRICS_PATH)

# === Imports ===
from halstead import run_halstead_analysis
from information_flow import run_information_flow_analysis
from live_variables import run_live_variable_analysis
from importlib import import_module

# Dynamically import language detector from Metrics/parsers
language_detector = import_module("Metrics.parsers.language_detector")


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

    # Detect all languages present and run each parser separately. Each
    # language will write CSVs into a subfolder under output_dir.
    langs = language_detector.detect_languages(project_dir)
    print(f"Detected languages: {langs}")

    if not langs:
        print("No recognizable source files found. Please provide a valid project directory.")
        return {}

    all_results = {}
    for lang in langs:
        try:
            parser_mod = import_module(f"Metrics.parsers.{lang}.parser")
        except Exception as e:
            print(f"Parser for language '{lang}' not found or failed to load: {e}")
            all_results[lang] = {"error": str(e)}
            continue

        lang_output = os.path.join(output_dir, lang)
        os.makedirs(lang_output, exist_ok=True)

        print(f"Running metrics using parser for: {lang}")
        try:
            results = parser_mod.run_metrics(project_dir, ignore_dirs, lang_output)
            all_results[lang] = results
        except Exception as e:
            print(f"Error running parser for {lang}: {e}")
            all_results[lang] = {"error": str(e)}

    print("\nAll analyses complete!")
    # Build combined metrics across all languages
    combined = {
        "total_ops": {},
        "total_opnds": {},
        "variables": {},
        "halstead_csv": os.path.join(output_dir, "combined_halstead.csv"),
        "information_flow_csv": os.path.join(output_dir, "combined_information_flow.csv"),
        "live_variables_csv": os.path.join(output_dir, "combined_live_variables.csv"),
    }

    # Aggregate counters
    ops_counter = Counter()
    opnds_counter = Counter()

    # helpers to collect CSVs
    halstead_files = []
    infoflow_files = []
    livevar_files = []

    for lang, res in all_results.items():
        if not isinstance(res, dict):
            continue
        if res.get("total_ops"):
            ops_counter.update(res.get("total_ops", {}))
        if res.get("total_opnds"):
            opnds_counter.update(res.get("total_opnds", {}))
        if res.get("variables"):
            # merge variable maps (file paths should be unique)
            combined_vars = res.get("variables")
            for p, vm in combined_vars.items():
                combined["variables"][p] = vm

        # collect csv paths if present
        if res.get("halstead"):
            halstead_files.append(res.get("halstead"))
        if res.get("information_flow"):
            infoflow_files.append(res.get("information_flow"))
        if res.get("live_variables"):
            livevar_files.append(res.get("live_variables"))

    combined["total_ops"] = dict(ops_counter)
    combined["total_opnds"] = dict(opnds_counter)

    # Function to concatenate CSVs with a header from the first file
    def _concat_csvs(sources, dest_path):
        if not sources:
            return None
        first = True
        with open(dest_path, "w", newline="", encoding="utf-8") as out_f:
            writer = None
            for src in sources:
                try:
                    with open(src, "r", encoding="utf-8", errors="ignore") as in_f:
                        reader = csv.reader(in_f)
                        rows = list(reader)
                        if not rows:
                            continue
                        header, data_rows = rows[0], rows[1:]
                        if first:
                            writer = csv.writer(out_f)
                            writer.writerow(header)
                            first = False
                        for r in data_rows:
                            writer.writerow(r)
                except FileNotFoundError:
                    continue
        return dest_path

    # write combined CSVs
    _concat_csvs(halstead_files, combined["halstead_csv"]) if halstead_files else None
    _concat_csvs(infoflow_files, combined["information_flow_csv"]) if infoflow_files else None
    _concat_csvs(livevar_files, combined["live_variables_csv"]) if livevar_files else None

    all_results["combined"] = combined
    return all_results


if __name__ == "__main__":
    run_quality_metrics()