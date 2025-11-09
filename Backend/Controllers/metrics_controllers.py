from fastapi import Form, HTTPException
from Services.metrics_services import analyze_metrics

def analyze_controller(
    project_dir: str = Form(...),
    ignore_dirs: str = Form("node_modules,dist,build,.next"),
    output_dir: str = Form("reports")
):
    try:
        if not project_dir:
            raise HTTPException(status_code=400, detail="Project directory path is required.")

        ignore_set = set(map(str.strip, ignore_dirs.split(",")))
        return analyze_metrics(project_dir, ignore_set, output_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")