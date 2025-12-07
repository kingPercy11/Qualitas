import os
import csv
import re
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


def calculate_oop_metrics(filepath):
    """Calculate Object-Oriented Programming metrics for a single file.
    
    Returns a dict with metrics including Chidamber & Kemerer (C&K) metrics:
    - class_count: Number of classes
    - method_count: Number of methods/functions
    - inheritance_depth (DIT): Depth of Inheritance Tree
    - coupling (CBO): Coupling Between Objects
    - cohesion_estimate (LCOM): Lack of Cohesion estimate
    - encapsulation_score: Ratio of private to total members
    - polymorphism_count: Number of overridden/overloaded methods
    - wmc: Weighted Methods per Class
    - rfc: Response For a Class (methods + remote calls)
    - noc: Number of Children (subclasses)
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.split('\n')
    except Exception:
        return None

    class_count = 0
    method_count = 0
    inheritance_depth = 0  # DIT - Depth of Inheritance Tree
    coupling = 0  # CBO - Coupling Between Objects
    private_members = 0
    total_members = 0
    polymorphism_count = 0
    wmc = 0  # Weighted Methods per Class
    rfc = 0  # Response For a Class
    noc = 0  # Number of Children
    
    # Track class information for C&K metrics
    classes_info = defaultdict(lambda: {
        'methods': [],
        'parent': None,
        'children': [],
        'method_calls': set(),
        'complexity': 0
    })
    
    # Patterns for different languages
    # Class definitions
    class_patterns = [
        re.compile(r'\bclass\s+(\w+)(?:\s*\(([^)]*)\))?(?:\s*:\s*(\w+))?(?:\s*extends\s+(\w+))?(?:\s*implements\s+([^{]+))?'),
        re.compile(r'\binterface\s+(\w+)'),
        re.compile(r'\bstruct\s+(\w+)')
    ]
    
    # Method/function patterns
    method_patterns = [
        re.compile(r'\bdef\s+(\w+)\s*\('),  # Python
        re.compile(r'\bfunction\s+(\w+)\s*\('),  # JavaScript
        re.compile(r'\b(?:public|private|protected|static)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*(?:{|=>)'),  # Java/C++/TS
        re.compile(r'(\w+)\s*:\s*function\s*\('),  # Object methods
        re.compile(r'(\w+)\s*\([^)]*\)\s*{'),  # C++ methods
    ]
    
    # Import/dependency patterns
    import_patterns = [
        re.compile(r'\bimport\s+'),
        re.compile(r'\bfrom\s+\w+\s+import\s+'),
        re.compile(r'\brequire\s*\('),
        re.compile(r'\b#include\s+'),
        re.compile(r'\busing\s+'),
    ]
    
    # Private member patterns
    private_patterns = [
        re.compile(r'\bprivate\s+\w+\s+(\w+)'),
        re.compile(r'\b__\w+'),  # Python private
        re.compile(r'\b_\w+'),  # Protected/private convention
        re.compile(r'#\w+'),  # JS private fields
    ]
    
    # Public member patterns
    public_patterns = [
        re.compile(r'\bpublic\s+\w+\s+(\w+)'),
        re.compile(r'\bself\.\w+\s*='),  # Python instance vars
        re.compile(r'\bthis\.\w+\s*='),  # JS/Java instance vars
    ]
    
    # Override/polymorphism patterns
    override_patterns = [
        re.compile(r'@override'),
        re.compile(r'@Override'),
        re.compile(r'\boverride\s+'),
        re.compile(r'\bvirtual\s+'),
    ]
    
    # Method call patterns for RFC calculation
    method_call_patterns = [
        re.compile(r'(\w+)\s*\('),  # Function calls
        re.compile(r'\.(\w+)\s*\('),  # Method calls
    ]
    
    # Complexity keywords for WMC calculation
    complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'case', 'catch', 'switch', '&&', '||', '?']
    
    current_class = None
    
    # Count classes and track parent-child relationships
    for pattern in class_patterns:
        matches = pattern.findall(content)
        class_count += len(matches)
        # Track inheritance for DIT and NOC
        for match in matches:
            if isinstance(match, tuple):
                class_name = match[0]
                current_class = class_name
                # Check all captured groups for parent class indicators
                for group in match[1:]:
                    if group and group.strip():
                        parent = group.strip().split(',')[0].strip()
                        if parent:
                            classes_info[class_name]['parent'] = parent
                            if parent in classes_info:
                                classes_info[parent]['children'].append(class_name)
                                noc = max(noc, len(classes_info[parent]['children']))
                            inheritance_depth = max(inheritance_depth, 1)
    
    # Count methods and track per class for WMC
    for pattern in method_patterns:
        matches = pattern.findall(content)
        method_count += len(matches)
        for method_name in matches:
            if current_class and isinstance(method_name, str):
                classes_info[current_class]['methods'].append(method_name)
    
    # Count method calls for RFC
    for pattern in method_call_patterns:
        matches = pattern.findall(content)
        for call in matches:
            if current_class and isinstance(call, str):
                classes_info[current_class]['method_calls'].add(call)
    
    # Calculate complexity for WMC
    for line in lines:
        for keyword in complexity_keywords:
            if keyword in line:
                if current_class:
                    classes_info[current_class]['complexity'] += line.count(keyword)
    
    # Count imports/coupling (CBO)
    for pattern in import_patterns:
        coupling += len(pattern.findall(content))
    
    # Count private members
    for pattern in private_patterns:
        private_members += len(pattern.findall(content))
    
    # Count public members
    for pattern in public_patterns:
        total_members += len(pattern.findall(content))
    
    total_members += private_members
    
    # Count polymorphism (overrides)
    for pattern in override_patterns:
        polymorphism_count += len(pattern.findall(content))
    
    # Calculate C&K metrics
    # WMC - Weighted Methods per Class (sum of complexities)
    if classes_info:
        total_complexity = sum(info['complexity'] for info in classes_info.values())
        wmc = total_complexity if total_complexity > 0 else method_count
    else:
        wmc = method_count
    
    # RFC - Response For a Class (methods + remote method calls)
    if classes_info:
        total_rfc = sum(len(info['methods']) + len(info['method_calls']) for info in classes_info.values())
        rfc = round(total_rfc / max(len(classes_info), 1), 2)
    else:
        rfc = method_count
    
    # Calculate DIT - find maximum inheritance depth
    def get_depth(class_name, visited=None):
        if visited is None:
            visited = set()
        if class_name in visited:
            return 0
        visited.add(class_name)
        parent = classes_info.get(class_name, {}).get('parent')
        if parent and parent in classes_info:
            return 1 + get_depth(parent, visited)
        return 0 if not parent else 1
    
    if classes_info:
        inheritance_depth = max((get_depth(cls) for cls in classes_info.keys()), default=0)
    
    # Calculate encapsulation score (0-100)
    if total_members > 0:
        encapsulation_score = round((private_members / total_members) * 100, 2)
    else:
        encapsulation_score = 0.0
    
    # LCOM - Lack of Cohesion (simplified: inverse of methods per class ratio)
    if class_count > 0:
        cohesion_estimate = round(method_count / class_count, 2)
    else:
        cohesion_estimate = 0.0
    
    return {
        "file": filepath,
        "class_count": class_count,
        "method_count": method_count,
        "dit": inheritance_depth,  # Depth of Inheritance Tree
        "noc": noc,  # Number of Children
        "cbo": coupling,  # Coupling Between Objects
        "wmc": wmc,  # Weighted Methods per Class
        "rfc": rfc,  # Response For a Class
        "lcom": cohesion_estimate,  # Lack of Cohesion (simplified)
        "encapsulation_score": encapsulation_score,
        "polymorphism_count": polymorphism_count
    }


def run_oop_metrics_analysis(project_dir, ignore_dirs, output_csv, file_extensions=('.py',)):
    """Analyze files and generate OOP metrics CSV."""
    ignore_dirs = ignore_dirs or IGNORED_DEFAULT
    files = get_files_by_extensions(project_dir, ignore_dirs, file_extensions)
    
    if not files:
        print(f"No files found for extensions: {file_extensions}")
        return
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    all_results = []
    
    print("\nStarting OOP Metrics Analysis...\n")
    for filepath in files:
        print(f"Analyzing: {filepath}")
        metrics = calculate_oop_metrics(filepath)
        if metrics:
            all_results.append(metrics)
    
    # Write results to CSV
    if all_results:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["file", "class_count", "method_count", "dit", "noc", "cbo", 
                         "wmc", "rfc", "lcom", "encapsulation_score", "polymorphism_count"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        
        print(f"\nOOP Metrics report saved to: {output_csv}")
    else:
        print("\nNo metrics calculated.")
