from pathlib import Path

import mujoco
import mujoco._structs
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
from utils.scene_gen import construct_scene
from copy import deepcopy 
from PIL import Image 
from typing import * 

from dart_physics.utils.run_functions import *
from utils.diff_ik import DiffIK
from avp_stream3 import HandTrackingServer 
from runs import load_task_cfg, load_robot_cfg
from utils.aloha_zmq_sub import ALOHAZMQSubscriber
from utils.camera_viewer import * 
import warnings
warnings.filterwarnings("ignore")


control_message = None 
app = Flask(__name__)

def run_flask():
    app.run(host='0.0.0.0', port=7013)


def keyboard_listener(): 
    global control_message  
    print(f"R - Start recording\nS - Save recording\nC - Cancel recording\nD - Delete last recording\nO - Reset objects\nQ - Quit")
    while True:
        # Check if there is input available
        key = sys.stdin.read(1).strip().lower()

        if key == 's':
            # start recording 
            control_message = "start_recording"
        elif key == 'd': 
            # stop recording (without saving)
            control_message = "stop_recording"

        elif key == 'f': 
            # save recording
            control_message = "save" 

        elif key == 'q':
            control_message = "reset_scene"

        elif key == 'w': 
            control_message = "reset_robot"
            
        elif key == 't':
            control_message = "switch_sm"


@app.route('/control', methods=['POST'])
def control():
    global control_message

    data = request.json
    control_message = data['command']

    return jsonify(success=True, message=f"Received command: {control_message}")

dummy_cfg = load_task_cfg("dummy")

class MJTeleop: 
    
    def __init__(self, task, robot, headless = False, avp = False): 

        self.cfg = load_task_cfg(task)
        self.robot_cfg = load_robot_cfg(robot)
        self.headless = headless
        self.avp = avp

        self.profiler = time_profiler()

        model = construct_scene(self.cfg, self.robot_cfg)
        self.configuration = mink.Configuration(model)
        self.data = self.configuration.data
        self.model = self.configuration.model


        model = construct_scene(dummy_cfg, self.robot_cfg)
        self.dummy_configuration = mink.Configuration(model)
        self.dummy_data = self.dummy_configuration.data
        self.dummy_model = self.dummy_configuration.model

        if not self.headless:
            self.viewer = mujoco.viewer.launch_passive(
                model=self.model, data=self.data, show_left_ui=True, show_right_ui=True)


        self.ik = DiffIK(self.dummy_configuration, self.robot_cfg)

        self.mocap_indices = dict() 
        for key, value in self.robot_cfg['points'].items():
            self.mocap_indices[value.mocap_frame] = self.model.body(value.mocap_frame).mocapid[0]

        # "head_track" mocap 
        self.mocap_indices["stereo_cam"] = self.model.body("stereo_cam").mocapid[0]

        self.rate = RateLimiter(frequency=500.0)
        self.t = 0.0

        self.is_recording = False 
        self.recording_start_time = 0.0
        self.trajectory = [] 
        self.hri_cmd = None 

        self.meta_data = { 
            "task": self.cfg["name"],
            "robot": self.robot_cfg["name"],
            "objects": self.cfg['objects'],
        }

        self.init = False

        self.prev_dict = None 

        if args.render: 
            if args.stereo: 
                self.renderer = mujoco.Renderer(self.model, 240, 640)
            else:
                self.renderer = mujoco.Renderer(self.model, 240, 320)

            self.zmq_addr = "tcp://127.0.0.1:5555"
            camera_viewer_process = start_camera_viewer_process(self.zmq_addr, args.stereo)
            if args.stereo: 
                self.renderer.scene.stereo = mujoco.mjtStereo.mjSTEREO_SIDEBYSIDE

            self.socket = get_socket(self.zmq_addr)
            

        # Start Flask server in a separate thread
        threading.Thread(target=run_flask, daemon=True).start()
        threading.Thread(target=keyboard_listener, daemon=True).start()

        self.streamer = HandTrackingServer()
        self.streamer.start()

        if args.puppet: 
            self.zmq_subscriber = ALOHAZMQSubscriber(zmq_port = 5555)
            self.zmq_subscriber.start()
        

    def preprocess_targets(self): 

        for key, value in self.robot_cfg["points"].items():
            
            if value.weld: 

                pos = value.init_posquat[:3]
                quat = value.init_posquat[3:]

                self.data.mocap_pos[self.model.body(value.mocap_frame).mocapid[0]] = np.array(pos)
                self.data.mocap_quat[self.model.body(value.mocap_frame).mocapid[0]] = np.array(quat)

            else:
                mink.move_mocap_to_frame(self.model, self.data, \
                                         value.mocap_frame, value.body_frame, value.type)
    
            

    def preprocess_avp(self, latest): 

        avp_frames = dict.fromkeys(["left", "right"], []) 

        d = deepcopy(latest)

        for key, transforms in self.robot_cfg['avp_calib'].items():

            finger = self.robot_cfg['points'][key]
            avp_idx = finger.avp_idx
            chilarity = finger.chilarity

            scale = transforms['scale']
            offset = transforms['offset']

            d[chilarity + "_fingers"][avp_idx][:3, -1] *= scale
            d[chilarity + "_fingers"][avp_idx][:3, -1] += offset

        avp_frames["right"] = d['right_wrist'] @ d['right_fingers']
        avp_frames["right"][:, 2, -1] -= args.th 

        avp_frames["left"]  = d['left_wrist'] @ d['left_fingers']
        avp_frames["left"][:, 2, -1] -= args.th 


        required_frames = dict.fromkeys(["left", "right"], {})

        for key, finger in self.robot_cfg['points'].items():

            chilarity = finger.chilarity
            avp_idx = finger.avp_idx
            mocap_frame = finger.mocap_frame
            rot_transform = finger.avp_transform

            f = avp_frames[chilarity][avp_idx]
            f[:3, :3] = f[:3, :3] @ rot_transform[:3, :3]

            required_frames[chilarity] [mocap_frame] = f 

        required_frames["head"] = d['head']
        required_frames["head"][:, 2, -1] -= ( args.th )

        return required_frames


    def check_if_exploding(self, threshold = 5):

        # print max data.qvel 
        print("Max qvel", np.max(np.abs(self.data.qvel)))
        if np.any(np.abs(self.data.qvel) > threshold):
            
            return True

        return False
    

    def solve_ik(self): 

        for task_desc, task in zip (self.robot_cfg["ik_task"], self.ik.tasks) :

            if task_desc.type == "relative":

                root = task_desc.root
                target = task_desc.target

                frame1 = self.robot_cfg["points"][root].body_frame
                frame2 = self.robot_cfg["points"][target].mocap_frame

                T_pm = self.configuration.get_transform(
                    frame2, "body", frame1, "body"
                )
                task.set_target(T_pm)                    

            elif task_desc.type == "absolute":

                target = task_desc.target

                frame = self.robot_cfg["points"][target].mocap_frame
                task.set_target(mink.SE3.from_mocap_name(self.model, self.data, frame))
        
        qtarget = self.ik.solve()

        return qtarget 



    def run(self): 

        mujoco.mj_resetDataKeyframe(self.model, self.data, self.model.key("home").id)

        mujoco.mj_step(self.model, self.data)

        self.preprocess_targets()

        if not self.init: 
            self.init_data = deepcopy(self.data)
            self.init = True

        cnt = 0 

        while self.viewer.is_running() if not args.headless else True:

            self.profiler.start("total")

            self.profiler.start("avp_preprocess")

            if self.avp: 

                latest = self.streamer.get_latest()
                if latest is None: 
                    continue

                processed_avp_frames = self.preprocess_avp(latest)

                for key, value in processed_avp_frames["right"].items():
                    self.data.mocap_pos[self.mocap_indices[key]] = value[:3, -1]
                    self.data.mocap_quat[self.mocap_indices[key]] = R.from_matrix(value[:3, :3]).as_quat(scalar_first = True)

                for key, value in processed_avp_frames["left"].items():
                    self.data.mocap_pos[self.mocap_indices[key]] = value[:3, -1]
                    self.data.mocap_quat[self.mocap_indices[key]] = R.from_matrix(value[:3, :3]).as_quat(scalar_first = True)

                if args.active: 
                    # stereo_cam 
                    self.data.mocap_pos[self.mocap_indices["stereo_cam"]] = processed_avp_frames["head"][0, :3, -1]
                    self.data.mocap_quat[self.mocap_indices["stereo_cam"]] = R.from_matrix(processed_avp_frames["head"][0, :3, :3]).as_quat(scalar_first = True)

                self.hri_cmd = latest 

            self.profiler.end("avp_preprocess")

            self.profiler.start("ik solving")
            if cnt % (500 // args.freq) == 0: 
                
                if not args.puppet: 
                    qtarget = self.solve_ik()

            if args.puppet: 
                if self.zmq_subscriber.latest is not None:
                    latest = self.zmq_subscriber.latest
                    self.data.ctrl[:6] = latest[:6]
                    self.data.ctrl[6] = latest[7]
                    self.data.ctrl[7:13] = latest[9:15]
                    self.data.ctrl[13] = latest[16]

            else:
                self.data.ctrl = self.robot_cfg['qpos2ctrl'](self.model, self.data, qtarget)

            
            self.profiler.end("ik solving")

            self.profiler.start("physics step")
            mujoco.mj_step(self.model, self.data)

            self.ik.update(self.data.qpos[:self.robot_cfg["obj_startidx"]])
            self.profiler.end("physics step")

            if not self.headless:
                self.viewer.sync()

            self.profiler.start("post physics control")
            self.post_physics_control()
            self.profiler.end("post physics control")


            if control_message is None: 

                self.profiler.start("dictionary preparing")
                sim_dict = self.prepare_dict_to_send_avp() 
                self.streamer.set_sim_states(sim_dict) 
                self.prev_dict = deepcopy(sim_dict) 
                self.profiler.end("dictionary preparing")

            if args.render:

                if cnt % (500 // 20) == 0: 

                    self.renderer.update_scene(self.data, "stereo_cam")
                    img = self.renderer.render()
                    self.socket.send_pyobj(img) 

                    print("setting image from sim")
                    self.streamer.set_image_states(img, args.stereo)
                    print("setted image from sim")

            self.profiler.end("total")

            cnt += 1 
            self.rate.sleep()

    def randomize_wrist_cam(self):

        body = self.model.body("l_robot/wrist")
        body.pos = np.array([-0.04, 0, -0.05]) #+ np.random.uniform(-0.005, 0.005, (3,))
        euler = np.array([0, -1.2217305, 0]) 
        euler += np.random.uniform(-0.1, 0.1, 3)
        mat = R.from_euler("xyz", euler, degrees = False).as_matrix() 
        mat = mat @ rot_y(-90)[:3, :3] @ rot_z(-90)[:3, :3]
        quat = R.from_matrix(mat).as_quat(scalar_first = True)
        body.quat = quat
        # euler += np.random.uniform(-0.1, 0.1, 3)
        # body.quat = R.from_euler('xyz', euler, degrees = False).as_quat(scalar_first = True)


    def post_physics_control(self): 
        global control_message

        if self.is_recording:
            state_dict = self.prepare_dict_to_record()
            self.trajectory.append(state_dict)

        if control_message == "reset_robot": 

            self.data.qpos = self.init_data.qpos
            self.data.qvel = self.init_data.qvel
            self.data.ctrl = self.init_data.ctrl
            self.data.mocap_pos = self.init_data.mocap_pos
            self.data.mocap_quat = self.init_data.mocap_quat

            mujoco.mj_forward(self.model, self.data)

            if self.check_if_exploding(): 
                print("Exploding!")
            else:
                control_message = None 

            print(f"[RECORDING CTRL] Resetting Robot.") 

        if control_message == "reset_scene":
            

            reset_func = self.cfg.get('reset_function', None)

            if reset_func is not None:
                reset_func(self.model, self.data, self.robot_cfg, self.cfg)

            else:

                id = self.robot_cfg["obj_startidx"] # TODO : fix this
                vid = self.robot_cfg["obj_startidx"] 
            
                try: 
                    reset_cfg = self.cfg.get('reset_perturbation', {})
                except:
                    pass 

                        

                for ii, obj in enumerate(self.cfg['objects']): 

                    try:  
                        if not obj in reset_cfg:
                            print(f"[WARN] Object {obj} does not specify how to perturb its pose. Skipping...")
                            new_posquat = np.array(self.cfg['default_poses'][obj]).copy()
                        else:
                            new_posquat = get_random_perturbed_pose(
                                old_pose=np.array(self.cfg['default_poses'][obj]),
                                reset_spec=reset_cfg[obj],
                            )
                        
                        self.data.qpos[id:id+7] = new_posquat
                        self.data.qvel[vid:vid+6] = 0.0

                    except:
                        rand_range = self.cfg['randomize_range']
                        posquat = np.array(self.cfg['default_poses'][obj]) 
                        self.data.qpos[id:id+7] = posquat

                        if self.cfg['randomize_pos'][obj]:
                            self.data.qpos[id] += np.random.uniform(-rand_range, rand_range)
                            self.data.qpos[id+1] += np.random.uniform(-rand_range, rand_range)

                        if self.cfg['randomize_rot'][obj]:
                            rand_quat = np.random.uniform(-1, 1, 4)
                            rand_quat /= np.linalg.norm(rand_quat)
                            self.data.qpos[id+3:id+7] = rand_quat

                        self.data.qvel[vid:vid+6] = 0.0

                    id += 7 
                    vid += 6

            mujoco.mj_step(self.model, self.data)
            self.preprocess_targets()

            if self.check_if_exploding(): 
                print("Exploding!")
            else:
                control_message = None 

            print(f"[RECORDING CTRL] Resetting Scene") 


        if control_message == "start_recording": 
            self.is_recording = True 
            self.recording_start_time = time.time()
            control_message = None

            print(f"[RECORDING CTRL] Started recording.")


        if control_message == "save":
            self.is_recording = False 
            control_message = None

            # see how many files are there
            files = [f for f in os.listdir(f"{LOG_STORE_DIR}") if f.endswith(".npy")] 
            timestamp = time.strftime("%Y/%m/%d-%H:%M:%S")

            time_elapsed = time.time() - self.recording_start_time
            self.meta_data['time_elapsed'] = time_elapsed
            self.meta_data['time_stamp'] = timestamp
            self.meta_data['success'] = True 

            # save in :03d format 
            np.save(f"{LOG_STORE_DIR}/{len(files):03d}.npy", self.trajectory)
            # save meta data in yaml format
            with open(f"{LOG_STORE_DIR}/{len(files):03d}.yaml", "w") as f: 
                yaml.dump(self.meta_data, f)

            self.trajectory = [] 
            print(f"[RECORDING CTRL] Saved successful trajectory to logs/{len(files):03d}.npy")


        if control_message == "stop_recording":
            self.is_recording = False 
            control_message = None

            # see how many files are there
            files = [f for f in os.listdir(f"{LOG_STORE_DIR}") if f.endswith(".npy")] 
            timestamp = time.strftime("%Y/%m/%d-%H:%M:%S")

            time_elapsed = time.time() - self.recording_start_time
            self.meta_data['time_elapsed'] = time_elapsed
            self.meta_data['time_stamp'] = timestamp
            self.meta_data['success'] = False  

            # save in :03d format 
            np.save(f"{LOG_STORE_DIR}/{len(files):03d}.npy", self.trajectory)
            # save meta data in yaml format
            with open(f"{LOG_STORE_DIR}/{len(files):03d}.yaml", "w") as f: 
                yaml.dump(self.meta_data, f)

            self.trajectory = [] 
            print("[RECORDING CTRL] Recording saved as failure.")

        if self.data.time == 0: 

            mujoco.mj_resetDataKeyframe(self.model, self.data, self.model.key("home").id)
            mujoco.mj_forward(self.model, self.data)
            self.preprocess_targets()

        if self.data.warning[mujoco.mjtWarning.mjWARN_BADQACC].number > 0:
            
            print("warning: bad qacc")
            mujoco.mj_resetDataKeyframe(self.model, self.data, self.model.key("home").id)
            mujoco.mj_forward(self.model, self.data)
            self.preprocess_targets()


    def prepare_dict_to_send_avp(self): 

        # this is a dictionary that I send to vision pro for AR rendering. 

        state_dict = {}

        for body_name, usdz_name in self.robot_cfg["bodies"].items(): 
            _body = self.data.body(body_name)
            state_dict[usdz_name] = mink.SE3.from_rotation_and_translation(rotation = mink.SO3(_body.xquat), translation = _body.xpos).as_matrix()

        for obj in self.cfg['objects']: 
            body_lists = self.cfg.get('object_meshes', {}) 

            if obj not in body_lists.keys(): 
                _obj = self.data.body(obj + '/')
                state_dict[obj] = mink.SE3.from_rotation_and_translation(rotation = mink.SO3(_obj.xquat), translation = _obj.xpos).as_matrix() 
            else: 
                body_list = body_lists[obj] 
                for body in body_list: 
                    _obj = self.data.body(obj + '/' + body)
                    state_dict[obj + '_' + body] = mink.SE3.from_rotation_and_translation(rotation = mink.SO3(_obj.xquat), translation = _obj.xpos).as_matrix()
                
        for v in state_dict.values():
            v[2, -1] += args.th

        return state_dict 

    def compare_dicts(self, prev_dict, new_dict): 

        if prev_dict is None: 
            return new_dict
        else:
            # compare diffeernces for every items, and only send the keys that are "different" to the server
            diff_dict = {}
            for key in prev_dict.keys():
                diff = np.linalg.norm(prev_dict[key] - new_dict[key])
                if diff > 1e-4:
                    diff_dict[key] = new_dict[key]

            return diff_dict


    def prepare_dict_to_record(self): 

        # need to prepare a dictionary containing simulation states to send to server 
        
        state_dict = {}

        for obj in self.cfg["objects"]: 
            _obj = self.data.body(obj + '/')
            state_dict[obj] = mink.SE3.from_rotation_and_translation(rotation = mink.SO3(_obj.xquat), translation = _obj.xpos).as_matrix()

        state_dict['entire_qpos'] = deepcopy(self.data.qpos)
        state_dict['entire_qvel'] = deepcopy(self.data.qvel)

        state_dict['qpos'] = deepcopy(self.data.qpos[..., :18])
        state_dict['qvel'] = deepcopy(self.data.qvel[..., :18])
        state_dict['ctrl'] = deepcopy(self.data.ctrl)
        state_dict['hri_cmd'] = self.hri_cmd

        return state_dict 


if __name__ == "__main__":
    
    import argparse 

    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", default = "mug_hang")
    parser.add_argument("--task", default = "mug_hang")
    parser.add_argument("--headless", action = 'store_true')
    parser.add_argument("--avp", action = 'store_true')
    parser.add_argument("--th", type = float, default = 0.75)
    parser.add_argument("--render", action = 'store_true')
    parser.add_argument("--puppet", action = 'store_true')
    parser.add_argument("--stereo", action = 'store_true')
    parser.add_argument("--active", action = 'store_true')
    # choose control frequency, choice of 10, 20, 25, 50 
    parser.add_argument("--freq", type = int, default = 100, choices = [10, 20, 25, 50, 100, 500])
    args = parser.parse_args()    

    teleop = MJTeleop(args.task, args.robot, args.headless, args.avp)
    teleop.run()