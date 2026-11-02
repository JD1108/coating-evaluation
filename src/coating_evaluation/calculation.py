from pathlib import Path
import numpy as np
import os
os.environ["OPENCV_LOG_LEVEL"] = "ERROR" #removes cv2 warning for tiff meta data.
import cv2
from skimage.morphology import skeletonize
from scipy.stats import trim_mean


def edges_and_areas(gray:np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
        Extract Coating and the edges from a grayscale image
    """
    # Gaussion blur, which reduces single pixel holes. Bigger kernel will bring less distortion, but also less resolution.
    blur = cv2.GaussianBlur(gray,(3,3),0)
    # Create black and white images, Pictures with high difference in brightness may need smaller blocks.
    th=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,401,-18)
    # Since there are only two Values, the thresholds have no effect.
    edges=cv2.Canny(th,50,150,apertureSize=5)
    # Combines line sections. Shape must be bigger than Blur kernel size. Defines nearest distance between two independent lines.
    closed_edges=cv2.morphologyEx(edges, cv2.MORPH_GRADIENT, np.ones((4,4),np.uint8))
    return closed_edges, th

def calculation(img_path:Path|str,sample_width:int,res:float) ->tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
        Calculating Coating thickness by measure the distance between the center contour (skelet) and the edge.
    """
    #Import image
    gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    edge, coating =edges_and_areas(gray)

    #divide in smaller sections
    # for small structures with wide openings more than 15 is inadvisable
    divider=sample_width//15
    if divider<3:
        divider=3
    height,width=edge.shape[:2]
    step_height=height//3
    step_width=width//divider
    means=np.zeros((3,divider))
    stds=np.zeros((3,divider))
    skel=np.zeros_like(coating,dtype=bool)

    #Calculating for every section
    for i in range(3):
        for j in range(divider):
            x0 = j * step_width
            x1 = (j + 1) * step_width
            y0 = i * step_height
            y1 = (i + 1) * step_height
            part = coating[y0:y1, x0:x1]
            skeleton = skeletonize(part>0)
            skel[y0:y1, x0:x1] = skeleton
            #Shortest Distance center to edge
            dist = cv2.distanceTransform(part, cv2.DIST_L2, 3)
            #Approximatly the coating thickness ist calculated by multiplying the distance by 2
            thickness = 2 * dist[skeleton > 0]
            #Calculating the mean and ignoring the highest and lowest 1%
            mean = trim_mean(thickness[thickness > 0],0.01)
            std = np.std(thickness)
            means[i, j] = mean
            stds[i, j] = std

    means/=res
    stds/=res
    return gray, coating, skel, means, stds





