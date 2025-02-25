
from dart_physics.robot_cfgs import * 
from pathlib import Path
import dart_physics.mink as mink 

_HERE = Path(__file__).resolve().parent


def qpos2ctrl(model, data, qpos_target): 

    ctrl = np.zeros(14)
    ctrl[:6] = qpos_target[0:6]
    ctrl[7:13] = qpos_target[8:14]

    # left gripper control
    tip1 = mink.SE3.from_mocap_name(model, data, "left_lf_target").as_matrix()
    tip2 = mink.SE3.from_mocap_name(model, data, "left_rf_target").as_matrix()

    finger_dist = np.linalg.norm(tip1[:3, 3] - tip2[:3, 3])
    max_grip = data.qpos[7] - 0.01
    ctrl[6] = np.clip(finger_dist - 0.01, max_grip, 0.04)

    # right gripper control
    tip1 = mink.SE3.from_mocap_name(model, data, "right_lf_target").as_matrix()
    tip2 = mink.SE3.from_mocap_name(model, data, "right_rf_target").as_matrix()

    finger_dist = np.linalg.norm(tip1[:3, 3] - tip2[:3, 3])
    max_grip = data.qpos[15] - 0.01
    ctrl[13] = np.clip(finger_dist - 0.01, max_grip, 0.04)


    return ctrl 

joints = ["left_waist", "left_shoulder", "left_elbow", "left_forearm_roll", 
          "left_wrist_angle", "left_wrist_rotate", "left_left_finger", "left_right_finger",
          "right_waist", "right_shoulder", "right_elbow", "right_forearm_roll",
        "right_wrist_angle", "right_wrist_rotate", "right_left_finger", "right_right_finger"]

bodies = ["left_base_link", "left_shoulder_link", "left_upper_arm_link", "left_upper_forearm_link",
          "left_lower_forearm_link", "left_wrist_link", "left_gripper_base", "left_left_finger_link", 
          "left_right_finger_link"] + \
        ["right_base_link", "right_shoulder_link", "right_upper_arm_link", "right_upper_forearm_link",
        "right_lower_forearm_link", "right_wrist_link", "right_gripper_base", "right_left_finger_link", 
        "right_right_finger_link"]


robot_cfg = {

    "name": "ALOHA",

    "robots": { 
        "robot": RobotConfig( 
                    xml_path = (_HERE / "../assets" / "aloha" / "aloha.xml").as_posix(),
                    home_q = [0, -0.96, 1.16, 0, -0.3, 0, 0.0084, 0.0084, 0, -0.96, 1.16, 0, -0.3, 0, 0.0084, 0.0084], 
                    freejoint = False, 
                    attach_to = [0.0, 0.2, 0.0, 1, 0, 0, 0 ], 
                    parallel_jaw = True, 
                    add_bodies = [ 
                        NewBodyConfig(attach_to = "left_right_finger_link", \
                                      body_name = "leftarm_right_finger_base", pos = [0.0, 0.0, 0.0]),
                        NewBodyConfig(attach_to = "left_left_finger_link", \
                                        body_name = "leftarm_left_finger_base", pos = [0, 0, 0.0]), 
                        NewBodyConfig(attach_to = "left_right_finger_link", \
                                        body_name = "leftarm_right_finger_tip", pos = [0.0, 0.05, 0.02]),
                        NewBodyConfig(attach_to = "left_left_finger_link", \
                                        body_name = "leftarm_left_finger_tip", pos = [0, -0.05, 0.02]),

                        NewBodyConfig(attach_to = "right_right_finger_link", \
                                        body_name = "rightarm_right_finger_base", pos = [0.0, 0.0, 0.0]),
                        NewBodyConfig(attach_to = "right_left_finger_link", \
                                        body_name = "rightarm_left_finger_base", pos = [0, 0, 0.0]),
                        NewBodyConfig(attach_to = "right_right_finger_link", \
                                        body_name = "rightarm_right_finger_tip", pos = [0.0, 0.05, 0.02]),
                        NewBodyConfig(attach_to = "right_left_finger_link", \
                                        body_name = "rightarm_left_finger_tip", pos = [0, -0.05, 0.02]),
                                      
                    ], 
                    
                ), 
    }, 

    "qpos2ctrl": qpos2ctrl, 
    "obj_startidx": (7+1) * 2, 
        
    "points" : { 

        "left_lb":     FingerKeypoints("left", 3, "left_lb_target", "robot/leftarm_left_finger_base", type = "body"),
        "left_lf":      FingerKeypoints("left", 4, "left_lf_target", "robot/leftarm_left_finger_tip", type = "body"),
        "left_rb":      FingerKeypoints("left", 8, "left_rb_target", "robot/leftarm_right_finger_base", type = "body"),
        "left_rf":      FingerKeypoints("left", 9, "left_rf_target", "robot/leftarm_right_finger_tip", type = "body"),
        
        "right_lb":     FingerKeypoints("right", 8, "right_lb_target", "robot/rightarm_left_finger_base", type = "body"),
        "right_lf":     FingerKeypoints("right", 9, "right_lf_target", "robot/rightarm_left_finger_tip", type = "body"),
        "right_rb":     FingerKeypoints("right", 3, "right_rb_target", "robot/rightarm_right_finger_base", type = "body"),
        "right_rf":     FingerKeypoints("right", 4, "right_rf_target", "robot/rightarm_right_finger_tip", type = "body"),

    },

    "reverse_points": { 

        "left_lb":     FingerKeypoints("right", 3, "left_lb_target", "robot/leftarm_right_finger_base", type = "body"),
        "left_lf":      FingerKeypoints("right", 4, "left_lf_target", "robot/leftarm_right_finger_tip", type = "body"),
        "left_rb":      FingerKeypoints("right", 8, "left_rb_target", "robot/leftarm_left_finger_base", type = "body"),
        "left_rf":      FingerKeypoints("right", 9, "left_rf_target", "robot/leftarm_left_finger_tip", type = "body"),
        
        "right_lb":     FingerKeypoints("left", 8, "right_lb_target", "robot/rightarm_right_finger_base", type = "body"),
        "right_lf":     FingerKeypoints("left", 9, "right_lf_target", "robot/rightarm_right_finger_tip", type = "body"),
        "right_rb":     FingerKeypoints("left", 3, "right_rb_target", "robot/rightarm_left_finger_base", type = "body"),
        "right_rf":     FingerKeypoints("left", 4, "right_rf_target", "robot/rightarm_left_finger_tip", type = "body"),
    },

    "avp_calib": { 

        "left_lb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_lf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_rb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_rf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},

        "right_lb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_lf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_rb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "right_rf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},

    }, 

    "ik_task" : [
        IKTasks(target = "left_lb"), 
        IKTasks(target = "left_lf"),
        IKTasks(target = "left_rb"),
        IKTasks(target = "left_rf"),

        IKTasks(target = "right_lb"),
        IKTasks(target = "right_lf"),
        IKTasks(target = "right_rb"),
        IKTasks(target = "right_rf"),
    ],

    "joints" : [f'robot/{j}' for j in joints],

    "bodies":  {f"robot/{b}": f"final_aloha_{b}" for b in bodies}, 

    "cameras": [
        CameraInfo("stereo_cam", pos = [-0.09433973, -0.29207777,  0.69795567], \
                   euler = [41.44131086, 0.5, 1.84107336], fovy = 70.0 ), 
    ], 

    "usdz_geoms": { 
        "aloha_left_base_link": [
            GeomInfo(mesh = "vx300s_1_base", quat = [1, 0, 0, 1]),
        ], 
        "aloha_left_shoulder_link": [
            GeomInfo(mesh = "vx300s_2_shoulder", pos = [0, 0, -0.003], quat = [1, 0, 0, 1]),
        ],
        "aloha_left_upper_arm_link": [ 
            GeomInfo(mesh = "vx300s_3_upper_arm", quat = [1, 0, 0, 1]),
        ],
        "aloha_left_upper_forearm_link": [ 
            GeomInfo(mesh = "vx300s_4_upper_forearm"), 
        ],
        "aloha_left_lower_forearm_link": [ 
            GeomInfo(mesh = "vx300s_5_lower_forearm", quat = [0, 1, 0, 0]), 
        ],
        "aloha_left_wrist_link": [ 
            GeomInfo(mesh = "vx300s_6_wrist", quat = [1, 0, 0, 1]), 
        ],
        "aloha_left_gripper_base": [ 
            GeomInfo(mesh = "vx300s_7_gripper_prop"), 
            GeomInfo(mesh = "vx300s_7_gripper_bar"),
            GeomInfo(mesh = "vx300s_7_gripper_wrist_mount", pos=[0, -0.03525, -0.0227], quat=[0, -1, 0, -1]),
            GeomInfo(mesh = "d405_solid", pos=[0, -0.0824748, -0.0095955], quat=[0, 0, -0.21644, -0.976296]), 
        ],
        "aloha_left_left_finger_link": [ 
            GeomInfo(mesh = "vx300s_8_custom_finger_left", pos=[0.0141637, 0.0211727, 0.06], quat=[1, 1, 1, -1]),    
        ],
        "aloha_left_right_finger_link": [
            GeomInfo(mesh = "vx300s_8_custom_finger_right", pos=[0.0141637, -0.0211727, 0.0597067], quat=[1, -1, -1, -1]),
        ],

        "aloha_right_base_link": [
            GeomInfo(mesh = "vx300s_1_base", quat = [1, 0, 0, 1]),
        ],
        "aloha_right_shoulder_link": [
            GeomInfo(mesh = "vx300s_2_shoulder", pos = [0, 0, -0.003], quat = [1, 0, 0, 1]),
        ],
        "aloha_right_upper_arm_link": [ 
            GeomInfo(mesh = "vx300s_3_upper_arm", quat = [1, 0, 0, 1]),
        ],
        "aloha_right_upper_forearm_link": [ 
            GeomInfo(mesh = "vx300s_4_upper_forearm"), 
        ],
        "aloha_right_lower_forearm_link": [ 
            GeomInfo(mesh = "vx300s_5_lower_forearm", quat = [0, 1, 0, 0]), 
        ],
        "aloha_right_wrist_link": [ 
            GeomInfo(mesh = "vx300s_6_wrist", quat = [1, 0, 0, 1]), 
        ],
        "aloha_right_gripper_base": [ 
            GeomInfo(mesh = "vx300s_7_gripper_prop"), 
            GeomInfo(mesh = "vx300s_7_gripper_bar"),
            GeomInfo(mesh = "vx300s_7_gripper_wrist_mount", pos=[0, -0.03525, -0.0227], quat=[0, -0.707107, 0, -0.707107]),
            GeomInfo(mesh = "d405_solid", pos=[0, -0.0824748, -0.0095955], quat=[0, 0, -0.21644, -0.976296]), 
        ],
        "aloha_right_left_finger_link": [ 
            GeomInfo(mesh = "vx300s_8_custom_finger_left", pos=[0.0141637, 0.0211727, 0.06], quat=[1, 1, 1, -1]),    
        ],
        "aloha_right_right_finger_link": [
            GeomInfo(mesh = "vx300s_8_custom_finger_right", pos=[0.0141637, -0.0211727, 0.0597067], quat=[1, -1, -1, -1]),
        ],
    }

}   


if __name__ == "__main__": 

    import trimesh 
    from scipy.spatial.transform import Rotation as R
    import os 

    asset_root = os.path.join(_HERE, "../assets", "aloha", "assets")
    usdz_root = os.path.join(_HERE, "../assets", "aloha", "transformed_stl")\

    os.makedirs(usdz_root, exist_ok = True)

    print([f"{k}" for k in robot_cfg["bodies"].values()])

    for k, v in robot_cfg["usdz_geoms"].items():

        meshes = [] 
        for i, geom in enumerate(v): 
            geom: GeomInfo
            mesh = trimesh.load_mesh(f"{asset_root}/{geom.mesh}.stl")
            pos = np.array(geom.pos)
            quat = np.array(geom.quat)

            mesh.visual.vertex_colors = np.array([0, 0, 0, 255], dtype = np.uint8)

            mat = np.eye(4)
            mat[:3, :3] = R.from_quat(quat, scalar_first = True).as_matrix()
            mat[:3, 3] = pos

            mesh.apply_transform(mat)

            meshes.append(mesh)

        scale = [mesh.scale for mesh in meshes]
        avg_scale = np.mean(scale, axis = 0)
        print(k, avg_scale)
        
        meshes = trimesh.util.concatenate(meshes)

        if avg_scale > 100: 

            meshes.apply_scale(0.001)

        if avg_scale < 1: 

            meshes.apply_scale(1)
        
        meshes.export(f"{usdz_root}/{k}.glb")


