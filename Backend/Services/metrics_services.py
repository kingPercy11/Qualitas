import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../..")) 
sys.path.append(PROJECT_ROOT)

from quality_metrics import run_quality_metrics


def analyze_metrics(project_dir: str, ignore_dirs: set, output_dir: str):
    try:
        if not project_dir or project_dir.strip() == "":
            raise ValueError("Project directory cannot be empty")
        if not os.path.exists(project_dir):
            raise ValueError(f"Project directory does not exist: {project_dir}")
        if not os.path.isdir(project_dir):
            raise ValueError(f"Project path is not a directory: {project_dir}")
        if not output_dir or output_dir.strip() == "":
            raise ValueError("Output directory cannot be empty")
        
        os.makedirs(output_dir, exist_ok=True)
        print(f"Running quality analysis on: {project_dir}")
        results = run_quality_metrics(project_dir, ignore_dirs, output_dir)

        return {
            "status": "success",
            "project_dir": project_dir,
            "output_dir": output_dir,
            "message": "All metrics computed successfully!",
            "results": results,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }