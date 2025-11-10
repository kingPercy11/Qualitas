import os
import re
import math
import csv
from collections import Counter

OPERATORS = {
    "+", "-", "*", "/", "%", "++", "--", "==", "===",
    "!=", "!==", ">", "<", ">=", "<=", "&&", "||", "!",
    "=", "+=", "-=", "*=", "/=", "%=", "=>", ".", ",", ";",
    "?", ":", "new", "delete", "return", "function", "if",
    "else", "switch", "case", "break", "continue", "for",
    "while", "do", "try", "catch", "finally", "throw", "await",
    "async", "import", "export", "from", "class", "extends"
}

TOKEN_PATTERN = re.compile(r"===|!==|==|!=|<=|>=|&&|\|\||=>|[A-Za-z_]\w*|[+\-*/%=&|^<>!?;:.,{}()[\]]")
COMMENT_PATTERN = re.compile(r"(//[^\n]*|/\*[\s\S]*?\*/)", re.MULTILINE)


def extract_operators_operands(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    code_no_comments = re.sub(COMMENT_PATTERN, "", code)
    tokens = TOKEN_PATTERN.findall(code_no_comments)

    operators, operands = [], []
    for token in tokens:
        if token in OPERATORS:
            operators.append(token)
        else:
            operands.append(token)

    lines = [line.strip() for line in code_no_comments.split("\n") if line.strip()]
    loc = len(lines)
    return operators, operands, loc


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


def run_halstead_analysis(project_dir, ignore_dirs, output_csv, file_extensions=('.js', '.jsx')):
    total_ops, total_opnds = [], []
    total_loc = 0
    file_results = []

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file.endswith(file_extensions):
                filepath = os.path.join(root, file)
                print(f"Analyzing: {filepath}")
                ops, opnds, loc = extract_operators_operands(filepath)

                op_counter = Counter(ops)
                opd_counter = Counter(opnds)
                n1, n2 = len(op_counter), len(opd_counter)
                N1, N2 = sum(op_counter.values()), sum(opd_counter.values())

                metrics = calculate_halstead(n1, n2, N1, N2)
                if metrics:
                    metrics["File"] = filepath
                    metrics["Lines_of_Code"] = loc
                    file_results.append(metrics)
                    total_ops.extend(ops)
                    total_opnds.extend(opnds)
                    total_loc += loc

    total_op_counter = Counter(total_ops)
    total_opd_counter = Counter(total_opnds)
    n1, n2 = len(total_op_counter), len(total_opd_counter)
    N1, N2 = sum(total_op_counter.values()), sum(total_opd_counter.values())

    total_metrics = calculate_halstead(n1, n2, N1, N2)
    if total_metrics:
        total_metrics["File"] = "PROJECT_TOTAL"
        total_metrics["Lines_of_Code"] = total_loc
        file_results.append(total_metrics)


    if file_results:
        keys = ["File", "n1", "n2", "N1", "N2", "Vocabulary", "Length", "Calc_Length",
                "Volume", "Difficulty", "Effort", "Time_sec", "Bugs", "Lines_of_Code"]

        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(file_results)

        print(f"\n Halstead metrics saved to: {output_csv}")
    else:
        print("\n No JS/JSX files found for analysis.")