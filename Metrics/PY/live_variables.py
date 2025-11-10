import os
import re
import csv
from collections import defaultdict


IGNORED_DEFAULT = {"node_modules", "dist", "build", "report", ".next", "scripts"}

VAR_DECL_PATTERN = re.compile(r"\b(var|let|const)\s+([A-Za-z_]\w*)", re.MULTILINE)
FUNC_DEF_PATTERN = re.compile(r"function\s+([A-Za-z_]\w*)|\(([^\)]*?)\)\s*=>", re.MULTILINE)
BLOCK_START_PATTERN = re.compile(r"[{]")
BLOCK_END_PATTERN = re.compile(r"[}]")

class Scope:
    def __init__(self, kind, parent=None, start_line=1):
        self.kind = kind
        self.parent = parent
        self.children = []
        self.definitions = {} 
        self.start_line = start_line
        self.end_line = None

    def add_var(self, name, line):
        if name not in self.definitions:
            self.definitions[name] = line

    def vars_at(self, line):
        visible = {n for n, l in self.definitions.items() if l <= line}
        if self.parent:
            visible |= self.parent.vars_at(line)
        return visible


def get_files_by_extensions(project_dir, ignore_dirs, file_extensions=('.js', '.jsx')):
    files_list = []
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(file_extensions):
                files_list.append(os.path.join(root, file))
    return files_list


def parse_scopes(lines):
    root_scope = Scope("file", None, 1)
    current_scope = root_scope
    stack = [root_scope]

    for i, line in enumerate(lines, start=1):
        line_stripped = line.strip()
        for _, var in VAR_DECL_PATTERN.findall(line):
            current_scope.add_var(var, i)

        for match in FUNC_DEF_PATTERN.findall(line):
            func_name = match[0] or "<arrow>"
            new_scope = Scope("function", current_scope, i)
            current_scope.children.append(new_scope)
            stack.append(new_scope)
            current_scope = new_scope

            params = match[1].split(",") if match[1] else []
            for p in [p.strip() for p in params if p.strip()]:
                current_scope.add_var(p, i)

        if BLOCK_START_PATTERN.search(line_stripped):
            new_scope = Scope("block", current_scope, i)
            current_scope.children.append(new_scope)
            stack.append(new_scope)
            current_scope = new_scope

        if BLOCK_END_PATTERN.search(line_stripped):
            current_scope.end_line = i
            if len(stack) > 1:
                stack.pop()
                current_scope = stack[-1]

    for s in stack:
        if s.end_line is None:
            s.end_line = len(lines)
    return root_scope


def variables_per_line(lines, scope):
    """Compute variables available at each line."""
    results = {}
    for i in range(1, len(lines) + 1):
        results[i] = sorted(scope.vars_at(i))
    return results


def analyze_file(filepath):
    """Analyze one file and return per-line variable data."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    scope_tree = parse_scopes(lines)
    var_map = variables_per_line(lines, scope_tree)
    return var_map


def run_live_variable_analysis(project_dir, ignore_dirs, output_csv, file_extensions=('.js', '.jsx')):
    """Run live variable analysis for files matching file_extensions and export CSV."""
    ignore_dirs = ignore_dirs or IGNORED_DEFAULT
    js_files = get_files_by_extensions(project_dir, ignore_dirs, file_extensions)

    if not js_files:
        print(f"No files found for extensions: {file_extensions}")
        return

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    all_results = []

    print("\nStarting Live Variable Analysis...\n")
    for filepath in js_files:
        print(f"Analyzing: {filepath}")
        var_map = analyze_file(filepath)
        for line_num, vars_ in var_map.items():
            all_results.append({
                "File": filepath,
                "Line": line_num,
                "Variables": ";".join(vars_),
                "Total": len(vars_)
            })

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["File", "Line", "Variables", "Total"])
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nLive Variable report saved to: {output_csv}")