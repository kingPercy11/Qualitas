import os
import sys
import streamlit as st

# === Add Qualitas directory to Python path ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "Qualitas"))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# === Import the central analyzer ===
from quality_metrics import get_user_input, run_quality_metrics


st.set_page_config(page_title="Qualitas Code Quality Analyzer", layout="wide")

st.title("Qualitas - Software Quality Metrics Analyzer")

# === Streamlit UI Inputs ===
project_dir = st.text_input("Enter Project Directory Path", "")
ignore_input = st.text_input("Comma-separated Folders to Ignore", "node_modules,dist,build,.next")
output_dir = st.text_input("Output Directory for Reports", "reports")

if st.button("Run Analysis"):
    if not os.path.exists(project_dir):
        st.error("Invalid project directory path!")
    else:
        ignore_dirs = set(map(str.strip, ignore_input.split(",")))
        os.makedirs(output_dir, exist_ok=True)

        halstead_csv = os.path.join(output_dir, "halstead_report.csv")
        info_csv = os.path.join(output_dir, "information_flow_metrics.csv")
        live_csv = os.path.join(output_dir, "live_variable_metrics.csv")

        st.info("Running all analyses... please wait")

        try:
            with st.spinner("Running Quality Metrics..."):
                # Temporarily override input handling in quality_metrics.py
                from quality_metrics import run_halstead_analysis, run_information_flow_analysis
                from Metrics.PY.live_variables import run_live_variable_analysis

                run_halstead_analysis(project_dir, ignore_dirs, halstead_csv)
                run_information_flow_analysis(project_dir, ignore_dirs, info_csv)
                run_live_variable_analysis(project_dir, ignore_dirs, live_csv)

            st.success("All analyses complete!")

            # === Display download buttons ===
            if os.path.exists(halstead_csv):
                st.download_button("Download Halstead Report", open(halstead_csv, "rb"), file_name="halstead_report.csv")
            if os.path.exists(info_csv):
                st.download_button("Download Information Flow Report", open(info_csv, "rb"), file_name="information_flow_metrics.csv")
            if os.path.exists(live_csv):
                st.download_button("Download Live Variables Report", open(live_csv, "rb"), file_name="live_variable_metrics.csv")

        except Exception as e:
            st.error(f"Error during analysis: {e}")