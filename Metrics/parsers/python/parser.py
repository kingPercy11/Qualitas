import os
import importlib
from collections import Counter
import re

# Import metric implementations from Metrics/PY via importlib. The project
# prepends the Metrics/PY directory to sys.path in `quality_metrics.py`, so
# these module names should resolve at runtime.
_hal = importlib.import_module("halstead")
_info = importlib.import_module("information_flow")
_live = importlib.import_module("live_variables")
run_halstead_analysis = _hal.run_halstead_analysis
run_information_flow_analysis = _info.run_information_flow_analysis
run_live_variable_analysis = _live.run_live_variable_analysis


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
                    # Python-specific variable extraction (scope approximation)
                    var_map = _extract_python_variables(path)
                    print(f"  Extracted {len(var_map)} lines of variables from {path}")
                except Exception as e:
                    print(f"  Error extracting Python variables from {path}: {e}")
                    # fallback to live analyzer if available
                    try:
                        var_map = _live.analyze_file(path)
                    except Exception:
                        var_map = {}
                variables[path] = var_map
    print("😀😃😄😁😆🥹😅😂")
    return dict(Counter(total_ops)), dict(Counter(total_opnds)), variables


def _extract_python_variables(filepath):
    """Heuristic-based extractor that returns a mapping of
    line number -> list of variables visible up to that line. It detects
    assignments, function parameters, for-loop variables, etc."""
    var_set = set()
    func_def_re = re.compile(r"\bdef\s+[A-Za-z_]\w*\s*\((.*?)\)\s*:")
    # Match assignments - handles indented code
    assign_re = re.compile(r"\b([A-Za-z_]\w*)\s*=(?!=)")
    # For loop variables: for x in ... or for i, j in ...
    for_re = re.compile(r"\bfor\s+([A-Za-z_][\w,\s]*)\s+in\s+")
    # Class definition parameters
    class_re = re.compile(r"\bclass\s+[A-Za-z_]\w*")
    # With statement variables: with x as y
    with_re = re.compile(r"\bwith\s+.*\s+as\s+([A-Za-z_]\w*)")

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    result = {}
    for i, line in enumerate(lines, start=1):
        # Function parameters
        m = func_def_re.search(line)
        if m:
            params = m.group(1)
            for p in [p.strip() for p in params.split(',') if p.strip()]:
                # ignore default values and annotations
                name = p.split('=')[0].split(':')[0].strip()
                # Handle *args, **kwargs
                name = name.lstrip('*').strip()
                if name and name.isidentifier():
                    var_set.add(name)

        # For loop variables
        mfor = for_re.search(line)
        if mfor:
            vars_part = mfor.group(1)
            for v in [vv.strip() for vv in vars_part.split(',')]:
                if v and v.isidentifier():
                    var_set.add(v)

        # With statement variables
        mwith = with_re.search(line)
        if mwith:
            name = mwith.group(1)
            if name and name.isidentifier():
                var_set.add(name)

        # Assignments (filter out keywords and common false positives)
        for name in assign_re.findall(line):
            # Skip if it's a keyword or looks like a comparison
            if name and name.isidentifier() and name not in ('if', 'elif', 'while', 'for', 'def', 'class', 'return'):
                var_set.add(name)

        # snapshot of visible variable names at this line
        result[i] = sorted(var_set)
    print("😀😃😄😁😆🥹😅😂")
    print(f"  Extracted {len(result)} lines of variables from {filepath}")
    print(result)
    return result


def run_metrics(project_dir, ignore_dirs, output_dir):
    print(f"🚀 PYTHON PARSER run_metrics called with project_dir={project_dir}")
    os.makedirs(output_dir, exist_ok=True)
    halstead_csv = os.path.join(output_dir, "halstead_report.csv")
    infoflow_csv = os.path.join(output_dir, "information_flow_metrics.csv")
    livevar_csv = os.path.join(output_dir, "live_variable_metrics.csv")

    # For Python, only analyze .py files
    exts = ('.py',)
    # Collect detailed tokens and variables from source files first
    print(f"🚀 Calling _collect_details...")
    total_ops_count, total_opnds_count, variables = _collect_details(project_dir, ignore_dirs, exts)
    print(f"🚀 _collect_details complete. Variables dict has {len(variables)} files")

    print("Running Halstead (Python)...")
    run_halstead_analysis(project_dir, ignore_dirs, halstead_csv, file_extensions=exts)

    print("Running Information Flow (Python)...")
    run_information_flow_analysis(project_dir, ignore_dirs, infoflow_csv, file_extensions=exts)

    print("Running Live Variable Analysis (Python)...")
    run_live_variable_analysis(project_dir, ignore_dirs, livevar_csv, file_extensions=exts, variables_map=variables)

    return {
        'halstead': halstead_csv,
        'information_flow': infoflow_csv,
        'live_variables': livevar_csv,
        'total_ops': total_ops_count,
        'total_opnds': total_opnds_count,
        'variables': variables
    }
