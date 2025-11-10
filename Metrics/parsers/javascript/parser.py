import os
import importlib

# Load metric modules via importlib (halstead, information_flow, live_variables)
_hal = importlib.import_module("halstead")
_info = importlib.import_module("information_flow")
_live = importlib.import_module("live_variables")
run_halstead_analysis = _hal.run_halstead_analysis
run_information_flow_analysis = _info.run_information_flow_analysis
run_live_variable_analysis = _live.run_live_variable_analysis
from collections import Counter


def _collect_details(project_dir, ignore_dirs, exts):
    total_ops = []
    total_opnds = []
    variables = {}

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if f.endswith(exts):
                path = os.path.join(root, f)
                try:
                    ops, opnds, _ = _hal.extract_operators_operands(path)
                except Exception:
                    ops, opnds = [], []
                total_ops.extend(ops)
                total_opnds.extend(opnds)

                try:
                    var_map = _live.analyze_file(path)
                except Exception:
                    var_map = {}
                variables[path] = var_map

    return dict(Counter(total_ops)), dict(Counter(total_opnds)), variables


def run_metrics(project_dir, ignore_dirs, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    halstead_csv = os.path.join(output_dir, "halstead_report.csv")
    infoflow_csv = os.path.join(output_dir, "information_flow_metrics.csv")
    livevar_csv = os.path.join(output_dir, "live_variable_metrics.csv")

    exts = ('.js', '.jsx', '.ts')

    # Collect details before running CSV output so parser returns them
    total_ops_count, total_opnds_count, variables = _collect_details(project_dir, ignore_dirs, exts)

    print("Running Halstead (JavaScript)...")
    run_halstead_analysis(project_dir, ignore_dirs, halstead_csv, file_extensions=exts)

    print("Running Information Flow (JavaScript)...")
    run_information_flow_analysis(project_dir, ignore_dirs, infoflow_csv, file_extensions=exts)

    print("Running Live Variable Analysis (JavaScript)...")
    run_live_variable_analysis(project_dir, ignore_dirs, livevar_csv, file_extensions=exts)

    return {
        'halstead': halstead_csv,
        'information_flow': infoflow_csv,
        'live_variables': livevar_csv,
        'total_ops': total_ops_count,
        'total_opnds': total_opnds_count,
        'variables': variables
    }
