import os
import re
import csv
from collections import defaultdict

# Regex patterns
FUNC_DEF_PATTERN = re.compile(r'function\s+([A-Za-z0-9_]+)|([A-Za-z0-9_]+)\s*=\s*\(.*?\)\s*=>')
FUNC_CALL_PATTERN = re.compile(r'([A-Za-z0-9_]+)\s*\(')


def extract_functions_and_calls(filepath):
    """Extract function definitions and calls in JS/JSX file."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()
    
    functions = set()
    for match in FUNC_DEF_PATTERN.findall(code):
        func_name = match[0] if match[0] else match[1]
        if func_name:
            functions.add(func_name)
    
    calls = [m for m in FUNC_CALL_PATTERN.findall(code)
             if m not in ['if', 'for', 'while', 'switch', 'return']]
    
    return functions, calls, len(code.splitlines())


def run_information_flow_analysis(project_dir, ignore_dirs , output_csv):
    """Analyze project and save Information Flow metrics to CSV."""
    all_funcs = defaultdict(set)
    all_calls = defaultdict(list)
    all_lengths = {}

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            if file.endswith(('.js', '.jsx')):
                path = os.path.join(root, file)
                print(f"Analyzing: {path}")
                funcs, calls, length = extract_functions_and_calls(path)
                all_funcs[path] = funcs
                all_calls[path] = calls
                all_lengths[path] = length

    fan_in = defaultdict(int)
    fan_out = defaultdict(int)
    func_to_file = {}

    for file, funcs in all_funcs.items():
        for func in funcs:
            func_to_file[func] = file

    for file, calls in all_calls.items():
        unique_calls = set(calls)
        fan_out[file] = len(unique_calls)
        for call in unique_calls:
            if call in func_to_file:
                fan_in[func_to_file[call]] += 1

    results = []
    for file in all_funcs.keys():
        L = all_lengths[file]
        FI = fan_in[file] if fan_in[file] > 0 else 1
        FO = fan_out[file] if fan_out[file] > 0 else 1
        complexity = (FI * FO) ** 2
        results.append((file, L, FI, FO, complexity))

    with open(output_csv, mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File", "Length", "FanIn", "FanOut", "Complexity"])
        for file, L, FI, FO, C in sorted(results, key=lambda x: x[-1], reverse=True):
            writer.writerow([file, L, FI, FO, C])

    print(f"\n Information Flow Metrics saved to: {output_csv}")