import argparse
from pathlib import Path
import shutil


def sort_csv(source,target):
    csv_copied=0
    source_path = Path(source)
    if not source_path.is_absolute():
        source_path = Path.cwd() / source_path
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = Path.cwd() / target_path

    ext = [".csv"]
    for file_path in source_path.glob("*"):
        if file_path.is_file() and file_path.suffix.lower() in ext and "mean" in file_path.stem.lower():
            extension = file_path.suffix
            folder_name = file_path.stem.replace(" ", "").replace("__", "_").replace("2026_01_14_", "").replace(
                "_fin", "").replace("-fin", "").replace("aux","Auxetic").replace("_mean","")

            counter = 1
            new_name = f"ref_{folder_name}_{extension}"
            dest_path = target_path / new_name
            while dest_path.exists():
                counter += 1
                new_name = f"{folder_name}_{counter}{extension}"
                dest_path = target_path / new_name
            shutil.copy2(file_path, dest_path)
            csv_copied += 1
    print(f"References copied: {csv_copied}")

def sort_images(source,target):

    images_copied=0

    source_path=Path(source)
    if not source_path.is_absolute():
        source_path=Path.cwd()/source_path
    target_path=Path(target)
    if not target_path.is_absolute():
        target_path=Path.cwd()/target_path

    ext=[".tif",".tiff"]
    for file_path in source_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in ext and "fused-1" in file_path.stem.lower():
            extension=file_path.suffix
            folder_name=file_path.parent.name.replace(" ","").replace("__","_").replace("2026_01_14_","").replace("_fin","").replace("-fin","")

            counter=1
            new_name=f"{folder_name}_{extension}"
            dest_path=target_path/new_name
            while dest_path.exists():
                counter+=1
                new_name = f"{folder_name}_{counter}{extension}"
                dest_path = target_path / new_name
            shutil.copy2(file_path,dest_path)
            images_copied+=1
    print(f"Images copied: {images_copied}")
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",required=True, type=str, help="source directory")
    parser.add_argument("-t",required=True, type=str, help="target directory")
    parser.add_argument("-e",required=True,choices=["i","im","img","images","r","ref","reference","references"], type=str, help="type of data: Images or references")
    args = parser.parse_args()
    if args.e == "i"or args.e == "im"or args.e == "img"or args.e == "images":
        sort_images(args.s,args.t)
    else:
        sort_csv(args.s,args.t)

