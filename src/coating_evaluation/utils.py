import cv2
import numpy as np
from pathlib import Path

def edges_and_areas(img_path:Path|str) -> tuple[np.ndarray, np.ndarray]:
    if not isinstance(img_path, Path):
        img_path = Path(img_path)
    if not img_path.is_file():
        raise FileNotFoundError(f"{img_path} not found")
    gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    th=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,401,-18)
    edges=cv2.Canny(th,50,150,apertureSize=5)
    closed_edges=cv2.morphologyEx(edges, cv2.MORPH_GRADIENT, np.ones((4,4),np.uint8))
    return closed_edges, th
