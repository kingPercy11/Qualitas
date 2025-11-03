import os
import re
import math
from collections import Counter

# === CONFIG ===
PROJECT_DIR = "/Users/pranjal/Desktop/Projects/UBER"  # change as needed
IGNORE_DIRS = {"node_modules", ".git", "__pycache__"}

# Common JS operators (extendable)
OPERATORS = {
    "+", "-", "*", "/", "%", "++", "--", "==", "===",
    "!=", "!==", ">", "<", ">=", "<=", "&&", "||", "!",
    "=", "+=", "-=", "*=", "/=", "%=", "=>", ".", ",", ";",
    "?", ":", "new", "delete", "return", "function", "if",
    "else", "switch", "case", "break", "continue", "for",
    "while", "do", "try", "catch", "finally", "throw", "await",
    "async", "import", "export", "from", "class", "extends"
}

# Regex patterns
TOKEN_PATTERN = re.compile(r"[A-Za-z_]\w*|==|===|!=|!==|<=|>=|&&|\|\||[+\-*/%=&|^<>!?;:.,{}()[\]]")

def extract_operators_operands(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()
    
    tokens = TOKEN_PATTERN.findall(code)
    operators, operands = [], []

    for token in tokens:
        if token in OPERATORS:
            operators.append(token)
        else:
            operands.append(token)

    return operators, operands

def calculate_halstead(n1, n2, N1, N2):
    n = n1 + n2
    N = N1 + N2
    if n1 == 0 or n2 == 0 or n == 0:
        return None

    N_ = (n1 * math.log2(n1)) + (n2 * math.log2(n2))
    V = N * math.log2(n)
    D = (n1 / 2) * (N2 / n2)
    E = D * V
    T = E / 18
    B = V / 3000

    return {
        "n1": n1, "n2": n2, "N1": N1, "N2": N2,
        "Vocabulary": n, "Length": N, "Calc_Length": round(N_, 2),
        "Volume": round(V, 2), "Difficulty": round(D, 2),
        "Effort": round(E, 2), "Time_sec": round(T, 2), "Bugs": round(B, 2)
    }

def analyze_project():
    total_ops, total_opnds = [], []

    for root, dirs, files in os.walk(PROJECT_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]  # skip ignored dirs

        for file in files:
            if file.endswith((".js", ".jsx")):
                filepath = os.path.join(root, file)
                print(f"Analyzing: {filepath}")
                ops, opnds = extract_operators_operands(filepath)
                total_ops.extend(ops)
                total_opnds.extend(opnds)

    op_counter = Counter(total_ops)
    opd_counter = Counter(total_opnds)

    n1, n2 = len(op_counter), len(opd_counter)
    N1, N2 = sum(op_counter.values()), sum(opd_counter.values())

    metrics = calculate_halstead(n1, n2, N1, N2)

    if metrics:
        print("\n=== Halstead Metrics Summary ===")
        for k, v in metrics.items():
            print(f"{k:15}: {v}")
    else:
        print("Insufficient data to calculate Halstead metrics.")

if __name__ == "__main__":
    analyze_project()