import os
import re
import csv
from collections import defaultdict

# === CONFIG ===
PROJECT_DIR = "/Users/pranjal/Desktop/Projects/UBER"  # Change this to your project folder
OUTPUT_CSV = os.path.join(PROJECT_DIR, "information_flow_metrics.csv")

# Regex patterns to detect JS functions and calls
FUNC_DEF_PATTERN = re.compile(r'function\s+([A-Za-z0-9_]+)|([A-Za-z0-9_]+)\s*=\s*\(.*?\)\s*=>')
FUNC_CALL_PATTERN = re.compile(r'([A-Za-z0-9_]+)\s*\(')

def extract_functions_and_calls(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()
    
    functions = set()
    for match in FUNC_DEF_PATTERN.findall(code):
        func_name = match[0] if match[0] else match[1]
        if func_name:
            functions.add(func_name)
    
    calls = [m for m in FUNC_CALL_PATTERN.findall(code) if m not in ['if', 'for', 'while', 'switch', 'return']]
    return functions, calls, len(code.splitlines())

def analyze_project():
    all_funcs = defaultdict(set)
    all_calls = defaultdict(list)
    all_lengths = {}

    # Step 1: Walk through project files
    for root, dirs, files in os.walk(PROJECT_DIR):
        # 🔹 Skip unnecessary folders
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'dist', 'report', 'build', '.next']]
        
        for file in files:
            if file.endswith(('.js', '.jsx')):
                path = os.path.join(root, file)
                
                # 🔹 Print current file being analyzed
                print(f"Analyzing: {path}")
                
                funcs, calls, length = extract_functions_and_calls(path)
                all_funcs[path] = funcs
                all_calls[path] = calls
                all_lengths[path] = length

    # Step 2: Compute Fan-in and Fan-out
    fan_in = defaultdict(int)
    fan_out = defaultdict(int)

    # Create function-to-file map
    func_to_file = {}
    for file, funcs in all_funcs.items():
        for func in funcs:
            func_to_file[func] = file

    # Count fan-in and fan-out
    for file, calls in all_calls.items():
        unique_calls = set(calls)
        fan_out[file] = len(unique_calls)
        for call in unique_calls:
            if call in func_to_file:
                fan_in[func_to_file[call]] += 1

    # Step 3: Compute Information Flow Metric
    results = []
    for file in all_funcs.keys():
        L = all_lengths[file]
        FI = fan_in[file] if fan_in[file] > 0 else 1 
        FO = fan_out[file] if fan_out[file] > 0 else 1  
        complexity =  (FI * FO)**2
        results.append((file, L, FI, FO, complexity))

    # Step 4: Print results to console
    print(f"\n{'File':70} {'Len':>6} {'FanIn':>6} {'FanOut':>6} {'Complexity':>12}")
    print("-" * 100)
    for file, L, FI, FO, C in sorted(results, key=lambda x: x[-1], reverse=True):
        print(f"{file:70} {L:6} {FI:6} {FO:6} {C:12}")

    # Step 5: Save to CSV file
    with open(OUTPUT_CSV, mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File", "Length", "FanIn", "FanOut", "Complexity"])
        for file, L, FI, FO, C in sorted(results, key=lambda x: x[-1], reverse=True):
            writer.writerow([file, L, FI, FO, C])

    print(f"\nResults saved to: {OUTPUT_CSV}")

if __name__ == "__main__":
    analyze_project()