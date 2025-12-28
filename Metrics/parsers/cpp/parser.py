import os
import importlib
import re

_hal = importlib.import_module("halstead")
_info = importlib.import_module("information_flow")
_live = importlib.import_module("live_variables")
_defect = importlib.import_module("defect_matrix")
_oop = importlib.import_module("oop_metrics")
run_halstead_analysis = _hal.run_halstead_analysis
run_information_flow_analysis = _info.run_information_flow_analysis
run_live_variable_analysis = _live.run_live_variable_analysis
run_defect_matrix_analysis = _defect.run_defect_matrix_analysis
run_oop_metrics_analysis = _oop.run_oop_metrics_analysis
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
                    var_map = _extract_cpp_variables(path)
                except Exception:
                    try:
                        var_map = _live.analyze_file(path)
                    except Exception:
                        var_map = {}
                variables[path] = var_map

    return dict(Counter(total_ops)), dict(Counter(total_opnds)), variables


def _extract_cpp_variables(filepath):
    """Heuristic extractor for C/C++ that collects variable names visible up to each line.
    Detects simple declarations and assignments. Not a full parser."""
    var_set = set()
    result = {}

    type_re = re.compile(r"\b(?:int|float|double|char|bool|auto|long|short|unsigned|size_t|std::string|string)\b\s+([A-Za-z_]\w*)")
    func_def_re = re.compile(r"^[A-Za-z_\*\s:&<>]+\s+([A-Za-z_]\w*)\s*\((.*?)\)\s*(?:\{|;)")

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, start=1):
        mfunc = func_def_re.match(line.strip())
        if mfunc:
            params = mfunc.group(2)
            for p in [pp.strip() for pp in params.split(',') if pp.strip()]:
                parts = p.split()
                name = parts[-1].replace('*', '').replace('&', '').strip()
                name = name.split('=')[0]
                if name and name.isidentifier():
                    var_set.add(name)

        for m in type_re.findall(line):
            name = m
            if name and name.isidentifier():
                var_set.add(name)

        am = re.findall(r"([A-Za-z_]\w*)\s*=", line)
        for name in am:
            if name and name.isidentifier():
                var_set.add(name)

        result[i] = sorted(var_set)

    return result


def run_metrics(project_dir, ignore_dirs, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    halstead_csv = os.path.join(output_dir, "halstead_report.csv")
    infoflow_csv = os.path.join(output_dir, "information_flow_metrics.csv")
    livevar_csv = os.path.join(output_dir, "live_variable_metrics.csv")
    defect_csv = os.path.join(output_dir, "defect_matrix.csv")
    oop_csv = os.path.join(output_dir, "oop_metrics.csv")

    exts = ('.c', '.cpp', '.cc', '.h', '.hpp')

    total_ops_count, total_opnds_count, variables = _collect_details(project_dir, ignore_dirs, exts)

    print("Running Halstead (C/C++)...")
    run_halstead_analysis(project_dir, ignore_dirs, halstead_csv, file_extensions=exts)

    print("Running Information Flow (C/C++)...")
    run_information_flow_analysis(project_dir, ignore_dirs, infoflow_csv, file_extensions=exts)

    print("Running Live Variable Analysis (C/C++)...")
    run_live_variable_analysis(project_dir, ignore_dirs, livevar_csv, file_extensions=exts, variables_map=variables)

    print("Running Defect Matrix Analysis (C/C++)...")
    run_defect_matrix_analysis(project_dir, ignore_dirs, defect_csv, file_extensions=exts)

    print("Running OOP Metrics Analysis (C/C++)...")
    run_oop_metrics_analysis(project_dir, ignore_dirs, oop_csv, file_extensions=exts)

    return {
        'halstead': halstead_csv,
        'information_flow': infoflow_csv,
        'live_variables': livevar_csv,
        'defect_matrix': defect_csv,
        'oop_metrics': oop_csv,
        'total_ops': total_ops_count,
        'total_opnds': total_opnds_count,
        'variables': variables
    }
