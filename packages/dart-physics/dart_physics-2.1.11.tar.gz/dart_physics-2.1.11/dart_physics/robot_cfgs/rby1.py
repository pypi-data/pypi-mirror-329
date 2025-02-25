
from dart_physics.robot_cfgs import * 
from pathlib import Path
import dart_physics.mink as mink 

_HERE = Path(__file__).resolve().parent


def qpos2ctrl(model, data, qpos_target): 

    ctrl = np.zeros(22)
    # ctrl
    # ctrl[:3] = qpos_target[0:3]
    # ctrl[3:9] = qpos_target[3:9] 
    # ctrl[3:10] = qpos_target[3:10]
    # ctrl[10:17] = qpos_target[12:19]
    # ctrl[0:3] = qpos_target[0:3]
    ctrl[0:6] = 0.0
    ctrl[6:13] = qpos_target[6:13] 
    ctrl[13:20] = qpos_target[15:22]
    
    # right gripper 
    # get from mocap 

    tip1 = mink.SE3.from_mocap_name(model, data, "right_rt_target").as_matrix()
    tip2 = mink.SE3.from_mocap_name(model, data, "right_lt_target").as_matrix()
    dist = np.linalg.norm(tip1[:3, 3] - tip2[:3, 3])
    max_grip = data.qpos[14] - 0.01
    ctrl[-2] = np.clip(dist - 0.01, max_grip, 0.05)
 

    # left gripper z
    # get from mocap 
    tip1 = mink.SE3.from_mocap_name(model, data, "left_rt_target").as_matrix()
    tip2 = mink.SE3.from_mocap_name(model, data, "left_lt_target").as_matrix()
    dist = np.linalg.norm(tip1[:3, 3] - tip2[:3, 3])
    max_grip = data.qpos[23] - 0.01
    ctrl[-1] = np.clip(dist - 0.01, max_grip, 0.05)
    # ctrl[20:24] = qpos_target[20:24]

    return ctrl 

joints = ["base_x", "base_y", "base_theta", "torso_0", 
          "torso_1", "torso_2", "torso_3", "torso_4", "torso_5", 
          "right_arm_0", "right_arm_1", "right_arm_2", "right_arm_3", "right_arm_4", "right_arm_5", "right_arm_6",
          "left_arm_0", "left_arm_1", "left_arm_2", "left_arm_3", "left_arm_4", "left_arm_5", "left_arm_6",
          "head_0", "head_1",
          "gripper_finger_r2", "gripper_finger_r1", "gripper_finger_l2", "gripper_finger_l1"]

bodies = {
    # "link_torso_0": "LINK_1", 
    # "link_torso_1": "LINK_2", 
    # "link_torso_2": "LINK_3", 
    # "link_torso_3": "LINK_4", 
    # "link_torso_4": "LINK_5", 
    # "link_torso_5": "LINK_6", 
    "link_right_arm_0": "LINK_7", 
    "link_right_arm_1": "LINK_8",
    "link_right_arm_2": "LINK_9",
    "link_right_arm_3": "LINK_10",
    "link_right_arm_4": "LINK_11",
    "link_right_arm_5": "LINK_12",
    "link_right_arm_6": "LINK_13",
    "FT_SENSOR_R": "FT_SENSOR_R", 
    "EE_BODY_R": "EE_BODY_RIGHT",  
    "ee_finger_r1": "EE_FINGER_RIGHT1",
    "ee_finger_r2": "EE_FINGER_RIGHT2",
    "link_left_arm_0": "LINK_14",
    "link_left_arm_1": "LINK_15",
    "link_left_arm_2": "LINK_16",
    "link_left_arm_3": "LINK_17",
    "link_left_arm_4": "LINK_18",
    "link_left_arm_5": "LINK_19",
    "link_left_arm_6": "LINK_20",
    "FT_SENSOR_L": "FT_SENSOR_L", 
    "EE_BODY_L": "EE_BODY_LEFT",  
    "ee_finger_l1": "EE_FINGER_LEFT1",
    "ee_finger_l2": "EE_FINGER_LEFT2",
}


robot_cfg = {

    "name": "RBY1_ONLY",

    "robots": { 
        "robot": RobotConfig( 
                    xml_path = (_HERE / "../assets" / "rainbow_arm_only" / "model_act.xml").as_posix(),
                    home_q = [0] * 6 + [0, 0, 0, -1.46, 0, 0, 0] + [0, 0] + [0, 0, 0, -1.46, 0, 0, 0] + [0, 0] + [0, 0], #  +  
                    freejoint = False, 
                    attach_to = [0, -0.05, -0.8, np.sqrt(2)/2, 0, 0, np.sqrt(2)/2], 
                    parallel_jaw = True, 
                    add_bodies = [ 
                        NewBodyConfig(attach_to = "ee_finger_l1", \
                                        body_name = "leftarm_right_finger_tip", pos = [0.0, 0.0, -0.05]),
                        NewBodyConfig(attach_to = "ee_finger_l2", \
                                        body_name = "leftarm_left_finger_tip", pos = [0, 0, -0.05]),

                        NewBodyConfig(attach_to="ee_finger_l1", \
                                        body_name = "leftarm_right_finger_base", pos = [0.03, 0, -0.02]),
                        NewBodyConfig(attach_to="ee_finger_l2", \
                                        body_name = "leftarm_left_finger_base", pos = [0.03, 0, -0.02]),

                        NewBodyConfig(attach_to = "ee_finger_r1", \
                                        body_name = "rightarm_right_finger_tip", pos = [0.0, 0.0, -0.05]),
                        NewBodyConfig(attach_to = "ee_finger_r2", \
                                        body_name = "rightarm_left_finger_tip", pos = [0.0, 0.0, -0.05]),

                        NewBodyConfig(attach_to = "ee_finger_r1", \
                                        body_name = "rightarm_right_finger_base", pos = [0.03, 0, -0.02]),
                        NewBodyConfig(attach_to = "ee_finger_r2", \
                                        body_name = "rightarm_left_finger_base", pos = [0.03, 0, -0.02]),

                        NewBodyConfig(attach_to = "link_head_1", \
                                        body_name = "target_head", pos = [0.0, 0.0, 0.0]),
                    ], 
                    
                ), 
    }, 

    "qpos2ctrl": qpos2ctrl, 
    "obj_startidx": 26, 
        
    "points" : { 

        "left_lb":      FingerKeypoints("left", 3, "left_lb_target", "robot/leftarm_left_finger_base", type = "body"), 
        "left_lt":      FingerKeypoints("left", 4, "left_lt_target", "robot/leftarm_left_finger_tip", type = "body"),
        "left_rb":      FingerKeypoints("left", 8, "left_rb_target", "robot/leftarm_right_finger_base", type = "body"),
        "left_rt":      FingerKeypoints("left", 9, "left_rt_target", "robot/leftarm_right_finger_tip", type = "body"),
        
        "right_lb":     FingerKeypoints("right", 3, "right_lb_target", "robot/rightarm_left_finger_base", type = "body"),
        "right_lt":     FingerKeypoints("right", 4, "right_lt_target", "robot/rightarm_left_finger_tip", type = "body"),
        "right_rb":     FingerKeypoints("right", 8, "right_rb_target", "robot/rightarm_right_finger_base", type = "body"),
        "right_rt":     FingerKeypoints("right", 9, "right_rt_target", "robot/rightarm_right_finger_tip", type = "body"),

        # "target_head":  FingerKeypoints("head", 1, "target_head", "robot/target_head", type = "body"),

    },

    "reverse_points": { 

        "left_lb":      FingerKeypoints("right", 3, "left_lb_target", "robot/leftarm_right_finger_base", type = "body"),
        "left_lt":      FingerKeypoints("right", 4, "left_lt_target", "robot/leftarm_right_finger_tip", type = "body"),
        "left_rb":      FingerKeypoints("right", 8, "left_rb_target", "robot/leftarm_left_finger_base", type = "body"),
        "left_rt":      FingerKeypoints("right", 9, "left_rt_target", "robot/leftarm_left_finger_tip", type = "body"),
        
        "right_lb":     FingerKeypoints("left", 3, "right_lb_target", "robot/rightarm_right_finger_base", type = "body"),
        "right_lt":     FingerKeypoints("left", 4, "right_lt_target", "robot/rightarm_right_finger_tip", type = "body"),
        "right_rb":     FingerKeypoints("left", 8, "right_rb_target", "robot/rightarm_left_finger_base", type = "body"),
        "right_rt":     FingerKeypoints("left", 9, "right_rt_target", "robot/rightarm_left_finger_tip", type = "body"),

        # "target_head":  FingerKeypoints("head", 1, "target_head", "robot/target_head", type = "body"),
    },

    "avp_calib": { 

        "left_lb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_rb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_lt": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_rt": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},

        "right_lb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_rb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_lt": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_rt": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},

        # "target_head": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},

    }, 

    "ik_task" : [
        IKTasks(target = "left_lb"),
        IKTasks(target = "left_lt"),
        IKTasks(target = "left_rb"),
        IKTasks(target = "left_rt"),

        IKTasks(target = "right_lb"),
        IKTasks(target = "right_lt"),
        IKTasks(target = "right_rb"),
        IKTasks(target = "right_rt"),
    ],

    "regulation_task": [ 
        # PostureTask(qpos=[0] * 26, cost = 0.01, disable_joints = [9, 10, 11, 12, 13, 14, 15, 16] + [18, 19, 20, 21, 22, 23, 24, 25],), 
        # RelativeCoMTask(root_name = "robot/base", root_type = "body", cost = 1.0),
        # DampingTask(cost = 1.0, disable_joints = [3, 4, 5, 6, 7, 8] + [10, 11, 12, 13, 14, 15, 16] + [18, 19, 20, 21, 22, 23, 24, 25])
    ], 

    "joints" : [f'robot/{j}' for j in joints],

    "bodies":  {f"robot/{b}": v for b, v in bodies.items()}, 
    
}   


if __name__ == "__main__": 

    # import trimesh 
    # from scipy.spatial.transform import Rotation as R
    # import os 

    # asset_root = os.path.join(_HERE, "../assets", "aloha", "assets")
    # usdz_root = os.path.join(_HERE, "../assets", "aloha", "transformed_stl")\

    # os.makedirs(usdz_root, exist_ok = True)

    # print([f"{k}" for k in robot_cfg["bodies"].values()])

    # for k, v in robot_cfg["usdz_geoms"].items():

    #     meshes = [] 
    #     for i, geom in enumerate(v): 
    #         geom: GeomInfo
    #         mesh = trimesh.load_mesh(f"{asset_root}/{geom.mesh}.stl")
    #         pos = np.array(geom.pos)
    #         quat = np.array(geom.quat)

    #         mesh.visual.vertex_colors = np.array([0, 0, 0, 255], dtype = np.uint8)

    #         mat = np.eye(4)
    #         mat[:3, :3] = R.from_quat(quat, scalar_first = True).as_matrix()
    #         mat[:3, 3] = pos

    #         mesh.apply_transform(mat)

    #         meshes.append(mesh)

    #     scale = [mesh.scale for mesh in meshes]
    #     avg_scale = np.mean(scale, axis = 0)
    #     print(k, avg_scale)
        
    #     meshes = trimesh.util.concatenate(meshes)

    #     if avg_scale > 100: 

    #         meshes.apply_scale(0.001)

    #     if avg_scale < 1: 

    #         meshes.apply_scale(1)
        
    #     meshes.export(f"{usdz_root}/{k}.glb")


    # print the "values" of bodies, 
    #  i need the values to be in "x", "y", "z" format 
    # i explicitly need the quoatation marks

    strings = [] 
    for k, v in robot_cfg["bodies"].items(): 
        strings.append(f'"{v}"')  # Corrected the formatting here

    print(",".join(strings))
