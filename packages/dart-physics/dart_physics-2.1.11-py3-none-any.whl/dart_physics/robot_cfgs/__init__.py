import numpy as np 
from dart_physics.utils.run_functions import *


class CameraInfo: 

    def __init__(self, name, pos = [0, 0, 0], euler = [0, 0, 0], fovy = 47.5, attach_to = None, attach_type = None): 
    
        self.name = name 
        self.attach_to = attach_to
        self.attached_robot, self.attached_body = attach_to.split("/") if attach_to is not None else None, None
        self.attach_type = attach_type
        self.pos = pos
        self.fovy = fovy 
        self.euler = euler


    def __repr__(self):
            
        return f"CameraInfo(name={self.name}, attach_to={self.attach_to}, pos={self.pos}, quat={self.quat}, fovy={self.fovy}, euler={self.euler})"
    

class BodyInfo: 

    def __init__(self, name, geoms, pos= [0,0,0], quat = [1, 0, 0, 0]): 

        self.name = name 
        self.geoms = geoms

        if isinstance(pos, str): 
            pos = [float(p) for p in pos.split()]
        if isinstance(quat, str):
            quat = [float(q) for q in quat.split()]

        self.pos = pos
        self.quat = quat

    def __repr__(self):
            
        return f"BodyInfo(geoms={self.geoms}, pos={self.pos}, quat={self.quat})"

class GeomInfo: 

    def __init__(self, mesh, pos= [ 0, 0, 0] , quat = [1, 0, 0, 0]): 

        self.mesh = mesh

        if isinstance(pos, str):
            pos = [float(p) for p in pos.split()]
        if isinstance(quat, str):
            quat = [float(q) for q in quat.split()]

        self.pos = pos 
        self.quat = quat 

    def __repr__(self): 

        return f"GeomInfo(mesh={self.mesh}, pos={self.pos}, quat={self.quat})"

class FingerKeypoints:
    def __init__(self, chilarity, avp_idx, mocap_frame, body_frame, weld = False, type = "body", avp_transform = np.eye(3), init_posquat = None):
        self.chilarity = chilarity
        self.avp_idx = avp_idx
        self.mocap_frame = mocap_frame
        self.body_frame = body_frame
        self.weld = weld 
        self.type = type 
        self.avp_transform = avp_transform
        self.init_posquat = init_posquat

    def __repr__(self):
        return f"Finger(avp_idx={self.avp_idx}, mocap_frame={self.mocap_frame}, body_frame={self.body_frame})"

class IKTasks: 

    def __init__(self, target, root = None, pos_cost = 1.0, ori_cost = 0.0, scale = 1.0): 

        self.target = target 
        self.root = root 
        self.scale = scale
        self.pos_cost = pos_cost    
        self.ori_cost = ori_cost

        if root is None: 
            self.type = "absolute"
        else:
            self.type = "relative"

    def __repr__(self): 

        return f"IKTasks(target={self.target}, root={self.root}, scale={self.scale})"
    
class PostureTask: 

    def __init__(self, qpos, cost, disable_joints): 
        self.qpos = qpos
        self.cost = cost
        self.disable_joints = disable_joints

    def __repr__(self): 
        return f"PostureTask(qpos={self.qpos}, cost={self.cost}, disable_joints={self.disable_joints})"


class CoMTask: 

    def __init__(self, cost): 
        self.cost = cost

    def __repr__(self): 
        return f"CoMTask(cost={self.cost})"
    

class RelativeCoMTask: 

    def __init__(self, root_name, root_type, cost): 
        self.root_name = root_name
        self.root_type = root_type
        self.cost = cost

    def __repr__(self): 
        return f"RelativeCoMTask(root_name={self.root_name}, root_type={self.root_type}, cost={self.cost})"
    
class DampingTask: 

    def __init__(self, cost, disable_joints = None): 
        self.cost = cost
        self.disable_joints = disable_joints

    def __repr__(self): 
        return f"DampingTask(cost={self.cost}, disable_joints={self.disable_joints})"

class RobotConfig: 

    def __init__(self, xml_path, home_q, attach_to = None, freejoint = False, parallel_jaw = None, add_bodies = [] ): 

        self.home_q = home_q
        self.xml_path = xml_path
        self.freejoint = freejoint
        self.attach_to = attach_to
        self.parallel_jaw = parallel_jaw
        self.add_bodies = add_bodies

    def __repr__(self):

        return f"RobotConfig(home_q={self.home_q}, xml_path={self.xml_path})"


class NewBodyConfig: 

    def __init__(self, attach_to, body_name, pos, quat = [1, 0, 0, 0]): 

        self.attach_to = attach_to
        self.body_name = body_name
        self.pos = pos
        self.quat = quat

    def __repr__(self): 

        return f"NewBodyConfig(attach_to={self.attach_to}, body_name={self.body_name}, pos={self.pos}, quat={self.quat})"