from fastapi import Form, HTTPException, UploadFile
from Services.metrics_services import analyze_metrics
import tempfile
import os
import shutil
from typing import List, Optional


async def analyze_controller(
    project_dir: Optional[str] = Form(None),
    ignore_dirs: str = Form("node_modules,dist,build,.next"),
    output_dir: str = Form("reports"),
    uploaded: Optional[str] = Form(None),
    project_files: Optional[List[UploadFile]] = None,
):
    try:
        # If files were uploaded, save them to a temp directory and analyze that.
        if uploaded and project_files:
            tmpdir = tempfile.mkdtemp(prefix="qualitas_upload_")
            for up in project_files:
                # Sanitize filename to prevent directory traversal
                filename = up.filename.replace("\\", "/")
                filename = os.path.normpath(filename)
                if filename.startswith("..") or os.path.isabs(filename):
                    # skip suspicious files
                    continue

                dest_path = os.path.join(tmpdir, filename)
                dest_dir = os.path.dirname(dest_path)
                if dest_dir and not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)

                with open(dest_path, "wb") as f:
                    shutil.copyfileobj(up.file, f)

            project_dir_to_use = tmpdir

        else:
            if not project_dir:
                raise HTTPException(status_code=400, detail="Project directory path is required.")
            project_dir_to_use = project_dir

        ignore_set = set(map(str.strip, ignore_dirs.split(",")))
        result = analyze_metrics(project_dir_to_use, ignore_set, output_dir)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")