import mujoco
import mujoco.viewer
from dm_control import mjcf
import numpy as np
from loop_rate_limiters import RateLimiter

import math 
import numpy as np 
import time 
import dart_physics.mink as mink
import subprocess 
import os 
import yaml 
from scipy.spatial.transform import Rotation as R
from flask import Flask, request, jsonify
import threading 
import sys 
import matplotlib.pyplot as plt 
import zmq 
from queue import Queue
from threading import Thread
from dirs import * 

# import below modules from .. path 
import sys
sys.path.append("./")
from utils.scene_gen import * 
from utils.mesh_download import download_mesh
from utils.scene_gen import USDZ_LINK_CORRESPONDENCE
from utils.opt_ik import PandaOptIK
from copy import deepcopy 
import torch 
import multiprocessing as mp

def load_cfg(path): 
    with open(path, "r") as f: 
        return yaml.load(f, Loader = yaml.FullLoader)

cfg = load_cfg(f"cfgs/mug_hang.yaml")



class BatchRenderer: 
    def __init__(self, cfg): 
        
        self.model = construct_dual_panda(cfg) 
        self.data = mujoco.MjData(self.model) 

        self.renderer = mujoco.Renderer(self.model, 480, 640)

    def render(self, qpos): 

        """
        qpos:  torch.Tensor(n_batch, qpos.shape)
        return: torch.Tensor(n_batch, 480, 640, 3)
        """

        qpos = qpos.cpu().numpy()
        imgs = [] 
        for i in range(qpos.shape[0]): 
            self.data.qpos[:] = qpos[i]
            self.renderer.update_scene(self.data, camera = 'head_cam')
            image = self.renderer.render()
            
            imgs.append(image)
        imgs = np.stack(imgs, axis = 0) 
        imgs = torch.from_numpy(imgs)

        return imgs



class MPBatchRenderer:
    def __init__(self, cfg):
        self.cfg = cfg
        self.model = construct_dual_panda(self.cfg)
        self.data = mujoco.MjData(self.model)

    def _initialize_renderer(self):
        """
        Initializes the model, data, and renderer for each process.
        This method is called once per process when it starts.
        """
        self.model = construct_dual_panda(self.cfg)
        self.data = mujoco.MjData(self.model)
        self.renderer = mujoco.Renderer(self.model, 480, 640)

    def _render_chunk(self, qpos_chunk):
        """
        Render a chunk of qpos instances.
        """
        imgs = []
        for qpos in qpos_chunk:
            self.data.qpos[:] = qpos
            self.renderer.update_scene(self.data, camera='head_cam')
            image = self.renderer.render()
            imgs.append(image)
        return imgs

    def render(self, qpos, num_workers=8):
        """
        qpos: torch.Tensor(n_batch, qpos.shape)
        return: torch.Tensor(n_batch, 480, 640, 3)
        """

        qpos = qpos.cpu().numpy()
        qpos_chunks = np.array_split(qpos, num_workers)

        with mp.Pool(processes=num_workers, initializer=self._initialize_renderer) as pool:
            results = pool.map(self._render_chunk, qpos_chunks)

        # Flatten the list of images
        imgs = [img for sublist in results for img in sublist]
        imgs = np.stack(imgs, axis=0)
        imgs = torch.from_numpy(imgs)

        return imgs


if __name__ == "__main__": 

    br = MPBatchRenderer(cfg) 

    qpos_size = br.data.qpos.shape[0]
    
    bs = 128 
    times = [] 
    for i in range(10): 
        t0 = time.time() 
        qpos =  torch.randn((bs, qpos_size))
        imgs = br.render(qpos)
        t1 = time.time()
        times.append(t1 - t0)
        print("Time taken to render {} images: {}".format(bs, t1 - t0))
    print("Average time: ", np.mean(times))
        
        


