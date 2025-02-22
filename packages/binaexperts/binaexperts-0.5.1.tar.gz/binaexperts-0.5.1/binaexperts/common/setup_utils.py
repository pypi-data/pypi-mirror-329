import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YOLOV5_PATH = os.path.join(BASE_DIR, "../../yolov5")
YOLOV7_PATH = os.path.join(BASE_DIR, "../../yolov7")

def clone_repo(repo_url, path):
    """Clone a GitHub repository if it doesn't exist."""
    if not os.path.exists(path):
        print(f"📥 Cloning {repo_url} into {path} ...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, path], check=True)
    else:
        print(f"✅ {path} already exists, skipping clone.")

def download_yolo_repos():
    """Clone YOLOv5 and YOLOv7 repositories before installation."""
    clone_repo("https://github.com/ultralytics/yolov5.git", YOLOV5_PATH)
    clone_repo("https://github.com/WongKinYiu/yolov7.git", YOLOV7_PATH)
