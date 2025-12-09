# Qualitas - Multi-Language Software Quality Metrics Analyzer

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![React](https://img.shields.io/badge/react-19.1.1-blue.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Qualitas** is a comprehensive software quality metrics analyzer that supports multiple programming languages and provides detailed code quality insights through various industry-standard metrics.

---

## 📋 Table of Contents

- [Features](#-features)
- [Supported Languages](#-supported-languages)
- [Metrics Calculated](#-metrics-calculated)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **Multi-Language Support**: Analyze Python, JavaScript, TypeScript, Java, and C++ projects
- **Comprehensive Metrics**: Calculate 6 different types of software quality metrics
- **Modern Web Interface**: React-based frontend with file/folder upload support
- **RESTful API**: FastAPI backend for easy integration
- **Combined Reports**: Aggregate metrics across multiple languages
- **CSV Export**: All metrics exported to CSV format for further analysis
- **Real-time Analysis**: Process files on upload or analyze local directories

---

## 🌐 Supported Languages

| Language   | Extensions               | Parser Status |
|------------|-------------------------|---------------|
| Python     | `.py`                   | ✅ Full Support |
| JavaScript | `.js`, `.jsx`           | ✅ Full Support |
| TypeScript | `.ts`, `.tsx`           | ✅ Full Support |
| Java       | `.java`                 | ✅ Full Support |
| C/C++      | `.c`, `.cpp`, `.cc`, `.h`, `.hpp` | ✅ Full Support |

---

## 📊 Metrics Calculated

### 1. **Halstead Complexity Metrics**

Measures software complexity based on operators and operands.

| Metric | Description | Formula |
|--------|-------------|---------|
| **n1** | Number of unique operators | Count of distinct operators |
| **n2** | Number of unique operands | Count of distinct operands |
| **N1** | Total number of operators | Sum of all operator occurrences |
| **N2** | Total number of operands | Sum of all operand occurrences |
| **Vocabulary (n)** | Program vocabulary | n = n1 + n2 |
| **Length (N)** | Program length | N = N1 + N2 |
| **Calculated Length (N̂)** | Estimated length | N̂ = n1×log₂(n1) + n2×log₂(n2) |
| **Volume (V)** | Program volume | V = N × log₂(n) |
| **Difficulty (D)** | Program difficulty | D = (n1/2) × (N2/n2) |
| **Effort (E)** | Programming effort | E = D × V |
| **Time (T)** | Time to program (seconds) | T = E / 18 |
| **Bugs (B)** | Estimated bugs | B = V / 3000 |

**Output**: `halstead_report.csv`

---

### 2. **Information Flow Metrics**

Analyzes function dependencies and information flow between components.

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **Fan-In** | Number of functions calling this function | Higher = more reusable |
| **Fan-Out** | Number of functions this function calls | Higher = more complex |
| **Information Flow Complexity** | Fan-In × Fan-Out | Measures coupling complexity |
| **Length** | Lines of code in function | Size indicator |

**Output**: `information_flow_metrics.csv`

---

### 3. **Live Variables Analysis**

Tracks variable scope and lifetime throughout the code.

| Metric | Description | Use Case |
|--------|-------------|----------|
| **Variables** | List of variables in scope at each line | Scope analysis |
| **Total** | Number of live variables per line | Memory usage estimation |
| **Line** | Line number reference | Debugging aid |

**Output**: `live_variable_metrics.csv`

---

### 4. **Defect Matrix**

Predicts potential defect density based on code characteristics.

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **Lines of Code** | Executable lines (excluding blanks/comments) | Direct count |
| **Cyclomatic Complexity** | Number of decision points | Count of if/for/while/case/&&/\|\| |
| **Max Nesting Depth** | Maximum indentation level | Deepest block nesting |
| **Function Count** | Number of functions/methods | Count of function definitions |
| **Defect Density Estimate** | Estimated defects per 1000 LOC | (complexity_factor × 20 + nesting_factor × 5) × 1000 |

**Output**: `defect_matrix.csv`

---

### 5. **Object-Oriented Metrics (Including C&K Metrics)**

Comprehensive OOP quality metrics including the complete Chidamber & Kemerer suite.

#### Chidamber & Kemerer (C&K) Metrics:

| Metric | Full Name | Description | Industry Benchmark |
|--------|-----------|-------------|-------------------|
| **WMC** | Weighted Methods per Class | Sum of complexities of all methods | Lower is better (< 50) |
| **DIT** | Depth of Inheritance Tree | Maximum inheritance depth | Lower is better (< 5) |
| **NOC** | Number of Children | Number of immediate subclasses | Depends on design |
| **CBO** | Coupling Between Objects | Number of classes coupled via imports | Lower is better (< 10) |
| **RFC** | Response For a Class | Methods + remote method calls | Lower is better (< 100) |
| **LCOM** | Lack of Cohesion of Methods | Methods per class ratio (simplified) | Higher indicates better cohesion |

#### Additional OOP Metrics:

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **Class Count** | Number of classes/interfaces | Project size indicator |
| **Method Count** | Total methods defined | Complexity indicator |
| **Encapsulation Score** | Percentage of private members (0-100) | Higher = better encapsulation |
| **Polymorphism Count** | Number of overridden methods | OOP design quality |

**Output**: `oop_metrics.csv`

---

### 6. **Combined Metrics**

Aggregated metrics across all languages in the project.

**Output Files**:
- `combined_halstead.csv`
- `combined_information_flow.csv`
- `combined_live_variables.csv`
- `combined_defect_matrix.csv`
- `combined_oop_metrics.csv`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                  │
│  - File/Folder Picker                                       │
│  - File Selection & Management                              │
│  - Results Display                                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI + Python)                 │
│  - File Upload Handling                                     │
│  - Request Validation                                       │
│  - Multi-language Detection                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Language-Specific Parsers                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  Python  │  │   Java   │  │   C++    │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
│  ┌──────────┐  ┌──────────┐                               │
│  │JavaScript│  │TypeScript│                               │
│  └──────────┘  └──────────┘                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Metrics Calculation Modules                 │
│  - halstead.py          - defect_matrix.py                  │
│  - information_flow.py  - oop_metrics.py                    │
│  - live_variables.py                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   CSV Report Generation                     │
│  - Per-language reports                                     │
│  - Combined cross-language reports                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **npm** or **yarn**

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kingPercy11/Qualitas.git
   cd Qualitas/Qualitas
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install fastapi uvicorn python-multipart python-dotenv
   ```

4. **Configure environment variables** (optional):
   
   Create `Backend/.env`:
   ```env
   PORT=8000
   HOST=127.0.0.1
   CORS_ALLOW_ORIGINS=http://localhost:5173,http://localhost:3000
   RELOAD=True
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   
   Create `frontend/.env`:
   ```env
   VITE_API_BASE=http://127.0.0.1:8000
   ```

---

## 💻 Usage

### Option 1: Using the Web Interface

1. **Start the Backend Server**:
   ```bash
   cd Qualitas/Backend
   uvicorn server:app --reload
   ```
   Backend will be available at `http://127.0.0.1:8000`

2. **Start the Frontend Development Server**:
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`

3. **Analyze Your Code**:
   - Open your browser to `http://localhost:5173`
   - Choose one of two methods:
     - **Method A**: Enter the full path to your project directory
     - **Method B**: Click "Select Folder" or "Select Files" to upload
   - Configure ignore directories (default: `node_modules,build,.next`)
   - Click "Analyze"
   - View results and download CSV reports

### Option 2: Using the Command Line

```bash
cd Qualitas
python quality_metrics.py
```

Follow the interactive prompts:
```
Enter project directory: /path/to/your/project
Enter comma-separated folders to ignore: node_modules,dist,build
Enter output directory for CSVs: reports
```

### Option 3: Using the Streamlit Interface

```bash
cd Qualitas
streamlit run app.py
```

Access at `http://localhost:8501`

---

## 🔌 API Reference

### Analyze Endpoint

**POST** `/api/analyze/`

Analyzes a project and returns quality metrics.

#### Request (Multipart Form Data)

**Option 1: Local Directory Analysis**
```
project_dir: string (required) - Absolute path to project
ignore_dirs: string - Comma-separated folders to ignore
output_dir: string - Where to save reports
```

**Option 2: File Upload Analysis**
```
uploaded: string - Set to "true"
project_files: File[] (required) - Array of uploaded files
ignore_dirs: string - Comma-separated folders to ignore
output_dir: string - Where to save reports
```

#### Response

```json
{
  "status": "success",
  "project_dir": "/path/to/project",
  "output_dir": "reports",
  "message": "All metrics computed successfully!",
  "results": {
    "python": {
      "halstead": "reports/python/halstead_report.csv",
      "information_flow": "reports/python/information_flow_metrics.csv",
      "live_variables": "reports/python/live_variable_metrics.csv",
      "defect_matrix": "reports/python/defect_matrix.csv",
      "oop_metrics": "reports/python/oop_metrics.csv",
      "total_ops": {...},
      "total_opnds": {...}
    },
    "javascript": {...},
    "combined": {
      "halstead_csv": "reports/combined_halstead.csv",
      "information_flow_csv": "reports/combined_information_flow.csv",
      "live_variables_csv": "reports/combined_live_variables.csv",
      "defect_matrix_csv": "reports/combined_defect_matrix.csv",
      "oop_metrics_csv": "reports/combined_oop_metrics.csv"
    }
  }
}
```

#### Error Response

```json
{
  "status": "error",
  "message": "Error description"
}
```

---

## 📁 Project Structure

```
Qualitas/
├── README.md
├── .gitignore
│
├── Qualitas/
│   ├── app.py                      # Streamlit interface
│   ├── quality_metrics.py          # Main orchestration script
│   │
│   ├── Backend/
│   │   ├── server.py               # FastAPI application
│   │   ├── .env                    # Backend configuration
│   │   ├── Controllers/
│   │   │   └── metrics_controllers.py
│   │   ├── Routes/
│   │   │   └── metrics_routes.py
│   │   └── Services/
│   │       └── metrics_services.py
│   │
│   ├── frontend/
│   │   ├── package.json
│   │   ├── vite.config.js
│   │   ├── .env                    # Frontend configuration
│   │   ├── public/
│   │   │   └── Logo.png
│   │   └── src/
│   │       ├── App.jsx
│   │       ├── main.jsx
│   │       ├── components/
│   │       │   └── MetricsForm.jsx
│   │       └── pages/
│   │           └── Home.jsx
│   │
│   └── Metrics/
│       ├── parsers/
│       │   ├── language_detector.py
│       │   ├── python/
│       │   │   └── parser.py
│       │   ├── javascript/
│       │   │   └── parser.py
│       │   ├── typescript/
│       │   │   └── parser.py
│       │   ├── java/
│       │   │   └── parser.py
│       │   └── cpp/
│       │       └── parser.py
│       │
│       └── PY/
│           ├── halstead.py
│           ├── information_flow.py
│           ├── live_variables.py
│           ├── defect_matrix.py
│           └── oop_metrics.py
│
└── reports/                        # Generated reports (not in git)
    ├── python/
    ├── javascript/
    └── combined_*.csv
```

---

## 🎯 Input & Output Details

### Input

| Input Type | Format | Description | Example |
|------------|--------|-------------|---------|
| **Project Directory** | String (absolute path) | Path to the codebase to analyze | `/Users/john/projects/myapp` |
| **Uploaded Files** | File[] (multipart) | Files uploaded via web interface | Multiple .py, .js, .java files |
| **Ignore Directories** | String (comma-separated) | Folders to exclude from analysis | `node_modules,dist,build,.next` |
| **Output Directory** | String (path) | Where to save CSV reports | `reports` or `/tmp/analysis` |

### Output

Each analysis generates CSV files organized by language and metric type:

#### Per-Language Reports

**Location**: `{output_dir}/{language}/`

- `halstead_report.csv` - Halstead metrics per file
- `information_flow_metrics.csv` - Fan-in/Fan-out per function
- `live_variable_metrics.csv` - Variable scope per line
- `defect_matrix.csv` - Defect predictions per file
- `oop_metrics.csv` - OOP and C&K metrics per file

#### Combined Reports

**Location**: `{output_dir}/`

- `combined_halstead.csv` - All languages' Halstead metrics
- `combined_information_flow.csv` - All languages' information flow
- `combined_live_variables.csv` - All languages' variable analysis
- `combined_defect_matrix.csv` - All languages' defect predictions
- `combined_oop_metrics.csv` - All languages' OOP metrics

---

## 📝 Example Usage

### Analyze a Python Project

```python
from quality_metrics import run_quality_metrics

results = run_quality_metrics(
    project_dir="/path/to/python/project",
    ignore_dirs={"__pycache__", "venv", ".git"},
    output_dir="./reports"
)

print(f"Analysis complete! Reports saved to: {results['combined']['halstead_csv']}")
```

### Analyze via API (cURL)

```bash
curl -X POST "http://127.0.0.1:8000/api/analyze/" \
  -F "project_dir=/path/to/project" \
  -F "ignore_dirs=node_modules,dist" \
  -F "output_dir=reports"
```

### Upload Files for Analysis

```bash
curl -X POST "http://127.0.0.1:8000/api/analyze/" \
  -F "uploaded=true" \
  -F "project_files=@file1.py" \
  -F "project_files=@file2.js" \
  -F "output_dir=reports"
```

---

## 🛠️ Configuration

### Backend Configuration (`.env`)

```env
# Server settings
PORT=8000
HOST=127.0.0.1
RELOAD=True

# CORS settings (comma-separated)
CORS_ALLOW_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Configuration (`.env`)

```env
# API endpoint
VITE_API_BASE=http://127.0.0.1:8000
```

---

## 🧪 Error Handling

Qualitas includes comprehensive error handling:

- ✅ Empty input validation (project directory, output directory)
- ✅ File existence checks
- ✅ Directory validation
- ✅ Uploaded file validation
- ✅ Malicious filename detection (directory traversal prevention)
- ✅ Detailed error messages in API responses
- ✅ Client-side validation before API calls

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Authors

- **Pranjal** - [kingPercy11](https://github.com/kingPercy11)

---

## 🙏 Acknowledgments

- Halstead complexity metrics based on Maurice Halstead's work
- Chidamber & Kemerer metrics suite for OOP quality assessment
- Information Flow metrics for software architecture analysis

---

## 📚 References

- [Halstead Complexity Measures](https://en.wikipedia.org/wiki/Halstead_complexity_measures)
- [Chidamber & Kemerer Metrics Suite](https://en.wikipedia.org/wiki/Programming_complexity#Chidamber_and_Kemerer_metrics)
- [Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
- [Software Quality Metrics](https://www.iso.org/standard/35733.html)

---

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub or contact the maintainers.

**Repository**: https://github.com/kingPercy11/Qualitas

---

*Made with ❤️ for better software quality*
