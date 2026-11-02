import argparse
import re
from pathlib import Path
import csv
import numpy as np
import os
os.environ["OPENCV_LOG_LEVEL"] = "ERROR"
import cv2
from .calculation import calculation
from .evaluation import evaluation

def main():
    """
        Provide user interaction and working with directories. Reference and Resolution names must include image name.
    """
    parser = argparse.ArgumentParser(prog="Coating thickness",description="Coating thickness calculator for images")
    parser.add_argument('-d','--dir',type=str,help="Folder containing images. Default is current directory.")
    parser.add_argument('-o','--output',type=str,help="Path where the output files will be saved. Default is a subfolder in image directory.")
    parser.add_argument('-r', '--res', type=str, help="Path to resolution.csv. Default is image directory.")
    parser.add_argument('--gray',action="store_true",help="Activate gray Scale Image output")
    parser.add_argument('--coating', action="store_true", help="Activate Coating (Black and White Image) output")
    parser.add_argument('--skeleton',action="store_true",help="Activate skeleton on Coating Image output")
    parser.add_argument('--plot',action="store_true",help="Activate Plot Output")
    parser.add_argument('--ref',nargs="?",const=True,default=False,help="Add a reference to the Plots")
    parser.add_argument('-a','--all',action="store_true",help="Activate all Outputs")

    args = parser.parse_args()

    #Verify Image Directory

    if args.dir:
        img_dir = Path(args.dir)
        if not img_dir.is_absolute():
            img_dir=Path.cwd()/img_dir
    else:
        img_dir = Path.cwd()

    if not img_dir.exists():
        raise FileNotFoundError(f"{img_dir} not found")
    if not img_dir.is_dir():
        raise NotADirectoryError(f"{img_dir} is not a directory")

    img_list = list(img_dir.glob("*.tif")) + list(img_dir.glob("*.tiff"))
    if not img_list:
        raise FileNotFoundError(f"Can't find tiff images in{img_dir}")


    #Verify Output Directory

    if args.output:
        output_dir = Path(args.output)
        if not output_dir.is_absolute():
            output_dir=img_dir/output_dir
    else:
        output_dir = img_dir/Path("output")
        if output_dir.exists():
            for i in range(1,100):
                output_dir = img_dir/Path(f"output{i}")
                if not output_dir.exists():
                    break
    if output_dir.exists():
       raise FileExistsError(f"Output directory already exists")
    output_dir.mkdir(parents=True)


    #Verify resolution file
    if args.res:
        res_path = Path(args.res)
        if not res_path.is_absolute():
            res_path=img_dir/res_path
    else:
        res_path=img_dir
    if res_path.is_file():
        if not res_path.suffix.lower()==".csv":
            raise TypeError(f"{res_path} is not a CSV file")
    else:
        res_list = list(res_path.rglob("res*.csv"))
        if not res_list:
            raise FileNotFoundError(f"{res_path} not found")
        if len(res_list) > 1:
            raise FileExistsError(f"Found more than one resolution file in '{res_path}': {res_list}")
        res_path = res_list[0]


    #Verify Reference Directory
    if args.ref or args.all:
        if args.ref is True or (args.all and args.ref is False):
            opts=["ref","reference","references"]
            path_found = False
            for opt in opts:
                ref_path = img_dir/opt
                if ref_path.is_dir():
                    path_found = True
                    break
            if not path_found:
                raise FileNotFoundError(f"Reference path not found")
        else:
            ref_path = Path(args.ref)
            if not ref_path.is_absolute():
                ref_path=img_dir/ref_path
            if not ref_path.exists():
                raise FileNotFoundError(f"{ref_path} not found")
            if not ref_path.is_dir():
                raise NotADirectoryError(f"{ref_path} is not a directory")



    #Get Resolution dict

    resolution={}
    with open(res_path,mode="r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            if not row or len(row) != 2:
                continue
            k=row[0].strip().lower()
            v=row[1].strip().lower()
            try:
                v=float(v)
            except ValueError:
                raise ValueError(f"Resolution for {k} is not a number")
            resolution[k]=v


    #Calculation for all images
    for img_path in img_list:

        width=get_width(img_path.stem)
        res=resolution.get(img_path.stem.lower())
        if not res is None:
            gray, coating, skel, means, stds=calculation(img_path,width,res)
        else:
            raise ValueError(f"Resolution for {img_path} does not exist")


        #Save requested results
        sub_output_dir=output_dir/img_path.stem
        sub_output_dir.mkdir(parents=False,exist_ok=False)

        # CSV files
        np.savetxt(sub_output_dir/f"{img_path.stem}_means.csv", means, delimiter=",")
        np.savetxt(sub_output_dir/f"{img_path.stem}_std.csv", stds, delimiter=",")

        #Gray Image
        if args.gray or args.all:
            cv2.imwrite(sub_output_dir/f"{img_path.stem}_gray.tiff", gray)

        #Black and White Image with or without Skeleton
        if args.coating or args.skeleton or args.all:
            if args.skeleton or args.all:
                img_type="coating_skeleton"
                coating=cv2.cvtColor(coating,cv2.COLOR_GRAY2RGB)
                coating[skel] = (0, 0, 255)
            else:
                img_type="coating"
            cv2.imwrite(sub_output_dir/f"{img_path.stem}_{img_type}.tiff", coating)

        #Plots
        if args.plot or args.all:
            if args.ref or args.all:
                evaluation(sub_output_dir,means,width,img_path.stem,ref_path=ref_path)
            else:
                evaluation(sub_output_dir,means,width,img_path.stem)
    parser.exit(0,"Finished")

def get_width(stem:str)->int:
    numbers=re.search(r"\d+",stem)
    if numbers:
        return int(numbers.group())
    else:
        raise ValueError(f"No number in {stem}")



if __name__ == "__main__":
    main()
