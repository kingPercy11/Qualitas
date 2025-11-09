import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../..")) 
sys.path.append(PROJECT_ROOT)

from quality_metrics import run_quality_metrics

def analyze_metrics(project_dir: str, ignore_dirs: set, output_dir: str):
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Running quality analysis on: {project_dir}") 
        run_quality_metrics(project_dir, ignore_dirs, output_dir)

        return {
            "status": "success",
            "project_dir": project_dir,
            "output_dir": output_dir,
            "message": "All metrics computed successfully!"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }