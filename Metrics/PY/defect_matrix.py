import os
import csv
from collections import defaultdict


IGNORED_DEFAULT = {"node_modules", "dist", "build", "report", ".next", "scripts"}


def get_files_by_extensions(project_dir, ignore_dirs, file_extensions):
    """Collect all files matching the given extensions."""
    files_list = []
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(file_extensions):
                files_list.append(os.path.join(root, file))
    return files_list


def calculate_defect_metrics(filepath):
    """Calculate defect-related metrics for a single file.
    
    Returns a dict with metrics:
    - lines_of_code: Total lines excluding blank and comments
    - cyclomatic_complexity: Approximation based on control flow keywords
    - nesting_depth: Maximum nesting level
    - function_count: Number of functions/methods
    - defect_density_estimate: Estimated defects per 1000 lines
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return None

    loc = 0
    complexity = 1  # Base complexity
    max_nesting = 0
    current_nesting = 0
    function_count = 0
    
    complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'case', 'catch', 'switch', '&&', '||', '?']
    function_keywords = ['def ', 'function ', 'fn ', 'func ', 'public ', 'private ', 'protected ']
    open_brackets = ['{', '(', '[']
    close_brackets = ['}', ')', ']']
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped or stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            continue
        
        loc += 1
        
        for keyword in complexity_keywords:
            if keyword in stripped:
                complexity += stripped.count(keyword)
        
        for func_kw in function_keywords:
            if func_kw in stripped:
                function_count += 1
                break
        
        current_nesting += stripped.count('{')
        max_nesting = max(max_nesting, current_nesting)
        current_nesting -= stripped.count('}')
        current_nesting = max(0, current_nesting)
    
    if loc > 0:
        complexity_factor = complexity / max(loc, 1)
        nesting_factor = max_nesting / 10.0
        defect_density = (complexity_factor * 20 + nesting_factor * 5) * 1000
    else:
        defect_density = 0.0
    
    return {
        "file": filepath,
        "lines_of_code": loc,
        "cyclomatic_complexity": complexity,
        "max_nesting_depth": max_nesting,
        "function_count": function_count,
        "defect_density_estimate": round(defect_density, 2)
    }


def run_defect_matrix_analysis(project_dir, ignore_dirs, output_csv, file_extensions=('.py',)):
    """Analyze files and generate defect matrix CSV."""
    if not project_dir or not project_dir.strip():
        raise ValueError("Project directory cannot be empty")
    if not output_csv or not output_csv.strip():
        raise ValueError("Output CSV path cannot be empty")
    
    ignore_dirs = ignore_dirs or IGNORED_DEFAULT
    files = get_files_by_extensions(project_dir, ignore_dirs, file_extensions)
    
    if not files:
        print(f"No files found for extensions: {file_extensions}")
        return
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    all_results = []
    
    print("\nStarting Defect Matrix Analysis...\n")
    for filepath in files:
        print(f"Analyzing: {filepath}")
        metrics = calculate_defect_metrics(filepath)
        if metrics:
            all_results.append(metrics)
    
    if all_results:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["file", "lines_of_code", "cyclomatic_complexity", "max_nesting_depth", 
                         "function_count", "defect_density_estimate"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        
        print(f"\nDefect Matrix report saved to: {output_csv}")
    else:
        print("\nNo metrics calculated.")
