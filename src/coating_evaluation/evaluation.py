from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def evaluation(output_dir:Path,calc_mean:np.ndarray,width:int,stem:str,ref_path:Path=None):
    """
        Only the evaluation of the calculated data, and a comparison to measured by hand data.
    """

    #Load reference
    if ref_path is not None:
        refs=list(ref_path.glob(f"*{stem}*.csv"))
        if not refs:
            raise FileNotFoundError(f"Can't find a reference csv for {stem} in {ref_path}")
        if len(refs)>1:
            raise FileExistsError(f"Found more than one resolution file in '{ref_path}': {refs}")
        ref_path=refs[0]
        ref_mean = np.genfromtxt(ref_path, delimiter=",", filling_values=np.nan)
        ref_mean = np.delete(ref_mean, 0, axis=0)
        ref_mean = np.delete(ref_mean, 0, axis=1)
        if ref_mean.shape[0] != calc_mean.shape[0]:
            raise ValueError("Reference and calculated mean do not have the same number of rows")
        ref_x = np.linspace(0, width, ref_mean.shape[1])
    calc_x=np.linspace(0,width,calc_mean.shape[1])

    fig, axs = plt.subplots(3, 1)

    # Create x values for different size of ref and calculated. Horizontal deviation must be the same.
    for i, ax in enumerate(axs):
        if ref_mean is not None:
            ax.plot(ref_x, ref_mean[i, :], label="by hand", color="blue")
        ax.plot(calc_x, calc_mean[i, :], label="automatic", color="red")

    #Find structure type for Title
    struc = ""
    ss = ["fo", "gy", "aux"]
    ls = ["Foam", "Gyroid", "Auxetic"]
    for s, l in zip(ss, ls):
        if s.lower() in stem.lower():
            struc = l
    for l in ls:
        if l.lower() in stem.lower():
            struc = l

    #Labeling and title
    fig.supxlabel("Distance [mm]")
    fig.supylabel("Coating Thickness [mm]")
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right")
    fig.suptitle(f"{struc} {width}")

    #Export

    fig.savefig(output_dir/f"{stem}_plot.png")


