import fs from "fs";
import path from "path";
import readline from "readline";

// Common JS operators (extendable)
const OPERATORS = new Set([
  "+", "-", "*", "/", "%", "++", "--", "==", "===",
  "!=", "!==", ">", "<", ">=", "<=", "&&", "||", "!",
  "=", "+=", "-=", "*=", "/=", "%=", "=>", ".", ",", ";",
  "?", ":", "new", "delete", "return", "function", "if",
  "else", "switch", "case", "break", "continue", "for",
  "while", "do", "try", "catch", "finally", "throw", "await",
  "async", "import", "export", "from", "class", "extends"
]);

const TOKEN_PATTERN = /[A-Za-z_]\w*|==|===|!=|!==|<=|>=|&&|\|\||[+\-*/%=&|^<>!?;:.,{}()[\]]/g;
const COMMENT_PATTERN = /(\/\/.*?$|\/\*.*?\*\/)/gs;

// === Extract operators, operands, LOC ===
function extractOperatorsOperands(filepath) {
  const code = fs.readFileSync(filepath, "utf-8");
  const codeNoComments = code.replace(COMMENT_PATTERN, "");
  const tokens = codeNoComments.match(TOKEN_PATTERN) || [];

  const operators = [];
  const operands = [];

  for (const token of tokens) {
    if (OPERATORS.has(token)) operators.push(token);
    else operands.push(token);
  }

  const lines = codeNoComments
    .split("\n")
    .map(line => line.trim())
    .filter(line => line && !line.startsWith("//"));

  const loc = lines.length;

  return { operators, operands, loc };
}

// === Halstead metrics ===
function calculateHalstead(n1, n2, N1, N2) {
  const n = n1 + n2;
  const N = N1 + N2;
  if (n1 === 0 || n2 === 0 || n === 0) return null;

  const N_ = (n1 * Math.log2(n1)) + (n2 * Math.log2(n2));
  const V = N * Math.log2(n);
  const D = (n1 / 2) * (N2 / n2);
  const E = D * V;
  const T = E / 18;
  const B = V / 3000;

  return {
    n1, n2, N1, N2,
    Vocabulary: n,
    Length: N,
    Calc_Length: Math.round(N_ * 100) / 100,
    Volume: Math.round(V * 100) / 100,
    Difficulty: Math.round(D * 100) / 100,
    Effort: Math.round(E * 100) / 100,
    Time_sec: Math.round(T * 100) / 100,
    Bugs: Math.round(B * 100) / 100
  };
}

// === Recursive directory analysis ===
function analyzeProject(PROJECT_DIR, IGNORE_DIRS) {
  const totalOps = [];
  const totalOpnds = [];
  let totalLOC = 0;

  function walkDir(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (IGNORE_DIRS.has(entry.name)) continue;

      if (entry.isDirectory()) {
        walkDir(fullPath);
      } else if (entry.isFile() && (entry.name.endsWith(".js") || entry.name.endsWith(".jsx"))) {
        console.log(`Analyzing: ${fullPath}`);
        const { operators, operands, loc } = extractOperatorsOperands(fullPath);
        totalOps.push(...operators);
        totalOpnds.push(...operands);
        totalLOC += loc;
      }
    }
  }

  walkDir(PROJECT_DIR);

  const opSet = new Set(totalOps);
  const opdSet = new Set(totalOpnds);

  const n1 = opSet.size;
  const n2 = opdSet.size;
  const N1 = totalOps.length;
  const N2 = totalOpnds.length;

  const metrics = calculateHalstead(n1, n2, N1, N2);

  if (metrics) {
    console.log("\n=== Halstead Metrics Summary ===");
    for (const [key, value] of Object.entries(metrics)) {
      console.log(`${key.padEnd(15)}: ${value}`);
    }
    console.log(`Lines of Code  : ${totalLOC}`);
  } else {
    console.log("Insufficient data to calculate Halstead metrics.");
  }
}

// === User input ===
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question("Enter the project directory path to analyze: ", (projectDir) => {
  rl.question("Enter comma-separated folder/file names to ignore: ", (ignoreInput) => {
    const IGNORE_DIRS = new Set(ignoreInput.split(",").map(s => s.trim()).filter(Boolean));

    console.log("\nStarting analysis...\n");
    analyzeProject(projectDir, IGNORE_DIRS);
    rl.close();
  });
});