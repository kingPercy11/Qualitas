from fastapi import APIRouter, Form
from Controllers.metrics_controllers import analyze_controller

router = APIRouter()

@router.post("/analyze/")
def analyze_route(
    project_dir: str = Form(...),
    ignore_dirs: str = Form("node_modules,dist,build,.next"),
    output_dir: str = Form("reports")
):
    return analyze_controller(project_dir, ignore_dirs, output_dir)