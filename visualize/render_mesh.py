from models.rotation2xyz import Rotation2xyz
import numpy as np
import os
os.environ['PYOPENGL_PLATFORM'] = "osmesa"

import torch
from visualize.simplify_loc2rot import joints2smpl

def render2mesh(motions, outdir='test_vis', device_id=0, name=None):
    print("Using cuda:",device_id)
    device_id = list(device_id)[0]
    frames, njoints, nfeats = motions.shape
    #print("motion shape:",motions.shape)
    j2s = joints2smpl(num_frames=frames, device_id=device_id, cuda=True)
    rot2xyz = Rotation2xyz(device=torch.device("cuda:{}".format(device_id)))
    faces = rot2xyz.smpl_model.faces
    if not os.path.exists(outdir + name+'.npy'):
        print(f'Running SMPLify, it may take a few minutes.')
        motion_tensor, opt_dict = j2s.joint2smpl(motions)  # [nframes, njoints, 3]

        vertices = rot2xyz(torch.tensor(motion_tensor).clone().detach(), mask=None,
                                        pose_rep='rot6d', translation=True, glob=True,
                                        jointstype='vertices',
                                        vertstrans=True)
        vertices = vertices.squeeze(dim=0).permute(2, 0, 1).cpu().numpy()
        np.save(outdir +'/'+ name+'.npy', vertices)
    else:
        vertices = np.load(outdir +'/'+ name+'.npy')
    return vertices