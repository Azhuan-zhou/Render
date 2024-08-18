import os
import random
import shutil
import sys
import natsort
from pathlib import Path
from argparse import ArgumentParser
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from visualize.render_mesh import render2mesh
try:
    import bpy
    bpy.app.debug = 0

    sys.path.append(os.path.dirname(bpy.data.filepath))

    # local packages
    sys.path.append(os.path.expanduser("~/.local/lib/python3.9/site-packages"))
except ImportError:
    raise ImportError(
        "Blender is not properly installed or not launch properly. See README.md to have instruction on how to install and use blender."
    )


# Monkey patch argparse such that
# blender / python / hydra parsing works
def parse_args(self, args=None, namespace=None):
    if args is not None:
        return self.parse_args_bak(args=args, namespace=namespace)
    try:
        idx = sys.argv.index("--")
        args = sys.argv[idx + 1:]  # the list after '--'
    except ValueError as e:  # '--' not in the list:
        args = []
    return self.parse_args_bak(args=args, namespace=namespace)


setattr(ArgumentParser, 'parse_args_bak', ArgumentParser.parse_args)
setattr(ArgumentParser, 'parse_args', parse_args)

from configs.config import parse_args


def render_cli() -> None:
    # parse options
    cfg = parse_args(phase="render")  # parse config file
    cfg.FOLDER = cfg.RENDER.FOLDER
    if cfg.RENDER.INPUT_MODE.lower() == "npy":
        output_dir = Path(os.path.dirname(cfg.RENDER.NPY))
        paths = [cfg.RENDER.NPY]
    elif cfg.RENDER.INPUT_MODE.lower() == "dir":
        output_dir = Path(cfg.RENDER.DIR)
        paths = []
        file_list = natsort.natsorted(os.listdir(cfg.RENDER.DIR))[cfg.RENDER.START_IDX:cfg.RENDER.END_IDX]

        # render mesh npy first
        for item in file_list:
            if item.endswith(".npy"):
                paths.append(os.path.join(cfg.RENDER.DIR, item))
        paths = paths
        print(f"begin to render {len(paths)} files")

    import numpy as np

    from models.render.blender import render
    from models.render.video import Video

    init = True
    for path in paths:
        print(path)
        file_name = os.path.basename(path.replace(".npy", ""))
        # check existed mp4 or under rendering
        if cfg.RENDER.MODE == "video":
            frames_folder = os.path.join('/net/acadia5a/data/ssun/HumanML3D/frames', file_name+"_frames")
            video_folder = '/net/acadia5a/data/ssun/HumanML3D/videos'
            if os.path.exists(os.path.join(video_folder,file_name+".mp4")):
                print(f"npy is rendered or under rendering {path}")
                continue
        else:
            # check existed png
            picture_folder = './data/pictures'
            if os.path.exists(os.path.join(picture_folder, file_name+".png")):
                print(f"npy is rendered or under rendering {path}")
                continue
        # prepare frame folder
        if cfg.RENDER.MODE == "video":
            os.makedirs(frames_folder, exist_ok=True)
        else:
            frames_folder = os.path.join(
                picture_folder,
                file_name+".png")

        try:
            data = np.load(path)
            if cfg.RENDER.MESH:
                print("Convert joints to mesh .......")
                data = render2mesh(data, outdir='./data/NPY', device_id=cfg.DEVICE, name=file_name)
                
                
            if data.shape[0] == 1:
                data = data[0]
        except FileNotFoundError:
            print(f"{path} not found")
            continue


        out = render(
            data,
            frames_folder,
            canonicalize=cfg.RENDER.CANONICALIZE,
            exact_frame=cfg.RENDER.EXACT_FRAME,
            num=cfg.RENDER.NUM,
            mode=cfg.RENDER.MODE,
            model_path=cfg.RENDER.MODEL_PATH,
            faces_path=cfg.RENDER.FACES_PATH,
            downsample=cfg.RENDER.DOWNSAMPLE,
            always_on_floor=cfg.RENDER.ALWAYS_ON_FLOOR,
            oldrender=cfg.RENDER.OLDRENDER,
            res=cfg.RENDER.RES,
            init=init,
            gt=cfg.RENDER.GT,
            accelerator=cfg.ACCELERATOR,
            device=cfg.DEVICE,
        )

        init = False

        if cfg.RENDER.MODE == "video":
            video = Video(frames_folder, fps=cfg.RENDER.FPS)
            vid_path = os.path.join(video_folder,file_name+".mp4")
            video.save(out_path=vid_path)
            shutil.rmtree(frames_folder)
            print(f"remove tmp fig folder and save video in {vid_path}")

        else:
            print(f"Frame generated at: {out}")


if __name__ == "__main__":
    render_cli()
