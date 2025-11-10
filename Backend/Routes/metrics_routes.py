from typing import List, Optional
from fastapi import APIRouter, Form, File, UploadFile
from Controllers.metrics_controllers import analyze_controller

router = APIRouter()


@router.post("/analyze/")
async def analyze_route(
    project_dir: Optional[str] = Form(None),
    ignore_dirs: str = Form("node_modules,dist,build,.next"),
    output_dir: str = Form("reports"),
    uploaded: Optional[str] = Form(None),
    project_files: Optional[List[UploadFile]] = File(None),
):
    """Analyze either an existing server-side project directory (project_dir)
    or uploaded files. If files are uploaded, they will be saved to a temporary
    directory and passed to the analysis controller as the project_dir.
    """
    return await analyze_controller(project_dir, ignore_dirs, output_dir, uploaded, project_files)