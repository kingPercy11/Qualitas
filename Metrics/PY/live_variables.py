import os
import re
import csv
from collections import defaultdict

# === CONFIG ===
IGNORED_DEFAULT = {"node_modules", "dist", "build", "report", ".next", "scripts"}

# Regex patterns
VAR_DECL_PATTERN = re.compile(r"\b(var|let|const)\s+([A-Za-z_]\w*)", re.MULTILINE)
FUNC_DEF_PATTERN = re.compile(r"function\s+([A-Za-z_]\w*)|\(([^\)]*?)\)\s*=>", re.MULTILINE)
BLOCK_START_PATTERN = re.compile(r"[{]")
BLOCK_END_PATTERN = re.compile(r"[}]")

# === CORE CLASSES ===
class Scope:
    """Represents a variable scope in the JS file."""
    def __init__(self, kind, parent=None, start_line=1):
        self.kind = kind
        self.parent = parent
        self.children = []
        self.definitions = {}  # variable -> defined line
        self.start_line = start_line
        self.end_line = None

    def add_var(self, name, line):
        if name not in self.definitions:
            self.definitions[name] = line

    def vars_at(self, line):
        """Get all visible variables at a given line (including parent scopes)."""
        visible = {n for n, l in self.definitions.items() if l <= line}
        if self.parent:
            visible |= self.parent.vars_at(line)
        return visible


# === HELPER FUNCTIONS ===
def get_js_files(project_dir, ignore_dirs):
    """Return a list of .js/.jsx files to analyze."""
    js_files = []
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith((".js", ".jsx")):
                js_files.append(os.path.join(root, file))
    return js_files


def parse_scopes(lines):
    """Build a hierarchical scope tree."""
    root_scope = Scope("file", None, 1)
    current_scope = root_scope
    stack = [root_scope]

    for i, line in enumerate(lines, start=1):
        line_stripped = line.strip()

        # Detect variable declarations
        for _, var in VAR_DECL_PATTERN.findall(line):
            current_scope.add_var(var, i)

        # Detect function/arrow function definitions
        for match in FUNC_DEF_PATTERN.findall(line):
            func_name = match[0] or "<arrow>"
            new_scope = Scope("function", current_scope, i)
            current_scope.children.append(new_scope)
            stack.append(new_scope)
            current_scope = new_scope

            # Add function parameters
            params = match[1].split(",") if match[1] else []
            for p in [p.strip() for p in params if p.strip()]:
                current_scope.add_var(p, i)

        # Handle block starts `{`
        if BLOCK_START_PATTERN.search(line_stripped):
            new_scope = Scope("block", current_scope, i)
            current_scope.children.append(new_scope)
            stack.append(new_scope)
            current_scope = new_scope

        # Handle block ends `}`
        if BLOCK_END_PATTERN.search(line_stripped):
            current_scope.end_line = i
            if len(stack) > 1:
                stack.pop()
                current_scope = stack[-1]

    # Close any remaining scopes
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


# === MAIN ENTRY FUNCTION ===
def run_live_variable_analysis(project_dir, ignore_dirs, output_csv):
    """Run live variable analysis for all JS/JSX files and export CSV."""
    ignore_dirs = ignore_dirs or IGNORED_DEFAULT
    js_files = get_js_files(project_dir, ignore_dirs)

    if not js_files:
        print("⚠️ No JS/JSX files found for analysis.")
        return

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    all_results = []

    print("\n📊 Starting Live Variable Analysis...\n")
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

    # Save CSV output
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["File", "Line", "Variables", "Total"])
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\n✅ Live Variable report saved to: {output_csv}")