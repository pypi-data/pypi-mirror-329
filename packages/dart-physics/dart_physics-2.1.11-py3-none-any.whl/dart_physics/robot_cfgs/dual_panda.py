
from dart_physics.robot_cfgs import * 
from pathlib import Path
import dart_physics.mink as mink 

_HERE = Path(__file__).resolve().parent


def qpos2ctrl(model, data, qpos_target): 

    ctrl = np.zeros(16)
    ctrl[:7] = qpos_target[0:7]
    ctrl[8:15] = qpos_target[9:16]

    # left gripper control
    tip1 = mink.SE3.from_mocap_name(model, data, "left_lf_target").as_matrix()
    tip2 = mink.SE3.from_mocap_name(model, data, "left_rf_target").as_matrix()

    finger_dist = np.linalg.norm(tip1[:3, 3] - tip2[:3, 3])
    max_grip = data.qpos[8] - 0.01
    ctrl[7] = np.clip(finger_dist - 0.01, max_grip, 0.04)

    # right gripper control
    tip1 = mink.SE3.from_mocap_name(model, data, "right_lf_target").as_matrix()
    tip2 = mink.SE3.from_mocap_name(model, data, "right_rf_target").as_matrix()

    finger_dist = np.linalg.norm(tip1[:3, 3] - tip2[:3, 3])
    max_grip = data.qpos[16] - 0.01
    ctrl[15] = np.clip(finger_dist - 0.01, max_grip, 0.04)


    return ctrl 



robot_cfg = {

    "name": "DualPanda",

    "robots": { 
        "l_robot": RobotConfig( 
                    xml_path = (_HERE / "../assets" / "franka_emika_panda" / "new_panda.xml").as_posix(),
                    home_q = [0, 0, 0, -1.5707899999999999, 0, 1.5707899999999999, -0.7853, 0.040000000000000001, 0.040000000000000001], 
                    freejoint = False, 
                    attach_to = [-0.4, -0.15, 0.0, 0.7071068 , 0, 0, 0.7071068 ], 
                    parallel_jaw = True, 
                    add_bodies = [ 
                        NewBodyConfig(attach_to = "right_finger", \
                                      body_name = "right_finger_base", pos = [0.0, 0.02, 0.0]),
                        NewBodyConfig(attach_to = "right_finger", \
                                        body_name = "right_finger_tip", pos = [0, 0, 0.05]), 
                        NewBodyConfig(attach_to = "left_finger", \
                                        body_name = "left_finger_base", pos = [0.0, 0.02, 0.0]),
                        NewBodyConfig(attach_to = "left_finger", \
                                        body_name = "left_finger_tip", pos = [0, 0, 0.05]),
                    ], 
                    
                ), 
        "r_robot": RobotConfig(
                    xml_path = (_HERE / "../assets" / "franka_emika_panda" / "new_panda.xml").as_posix(),
                    home_q = [0, 0, 0, -1.5707899999999999, 0, 1.5707899999999999, -0.7853, 0.040000000000000001, 0.040000000000000001], 
                    freejoint = False,
                    attach_to = [0.4, -0.15, 0.0, 0.7071068 , 0, 0, 0.7071068 ], 
                    parallel_jaw = True,
                    add_bodies = [ 
                        NewBodyConfig(attach_to = "right_finger", \
                                      body_name = "right_finger_base", pos = [0.0, 0.02, 0.0]),
                        NewBodyConfig(attach_to = "right_finger", \
                                        body_name = "right_finger_tip", pos = [0, 0, 0.05]), 
                        NewBodyConfig(attach_to = "left_finger", \
                                        body_name = "left_finger_base", pos = [0.0, 0.02, 0.0]),
                        NewBodyConfig(attach_to = "left_finger", \
                                        body_name = "left_finger_tip", pos = [0, 0, 0.05]),
                    ], 

                ) 
    }, 

    "qpos2ctrl": qpos2ctrl, 
    "obj_startidx": (7+2) * 2, 
        
    "points" : { 

        "left_lb":     FingerKeypoints("left", 3, "left_lb_target", "l_robot/left_finger_base", type = "body"),
        "left_lf":      FingerKeypoints("left", 4, "left_lf_target", "l_robot/left_finger_tip", type = "body"),
        "left_rb":      FingerKeypoints("left", 8, "left_rb_target", "l_robot/right_finger_base", type = "body"),
        "left_rf":      FingerKeypoints("left", 9, "left_rf_target", "l_robot/right_finger_tip", type = "body"),
        
        "right_lb":     FingerKeypoints("right", 8, "right_lb_target", "r_robot/left_finger_base", type = "body"),
        "right_lf":     FingerKeypoints("right", 9, "right_lf_target", "r_robot/left_finger_tip", type = "body"),
        "right_rb":     FingerKeypoints("right", 3, "right_rb_target", "r_robot/right_finger_base", type = "body"),
        "right_rf":     FingerKeypoints("right", 4, "right_rf_target", "r_robot/right_finger_tip", type = "body"),

    },

    "reverse_points": { 

        "left_lb":     FingerKeypoints("right", 3, "left_lb_target", "l_robot/right_finger_base", type = "body"),
        "left_lf":      FingerKeypoints("right", 4, "left_lf_target", "l_robot/right_finger_tip", type = "body"),
        "left_rb":      FingerKeypoints("right", 8, "left_rb_target", "l_robot/left_finger_base", type = "body"),
        "left_rf":      FingerKeypoints("right", 9, "left_rf_target", "l_robot/left_finger_tip", type = "body"),
        
        "right_lb":     FingerKeypoints("left", 8, "right_lb_target", "r_robot/right_finger_base", type = "body"),
        "right_lf":     FingerKeypoints("left", 9, "right_lf_target", "r_robot/right_finger_tip", type = "body"),
        "right_rb":     FingerKeypoints("left", 3, "right_rb_target", "r_robot/left_finger_base", type = "body"),
        "right_rf":     FingerKeypoints("left", 4, "right_rf_target", "r_robot/left_finger_tip", type = "body"),

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

    "joints" : ['l_robot/joint{}'.format(i) for i in range(1, 8)] + ['r_robot/joint{}'.format(i) for i in range(1, 8)], 

    "bodies":  {
        # left robot
        "l_robot/link0":   "panda_link0_left",   "l_robot/link1":   "panda_link1_left", 
        "l_robot/link2":   "panda_link2_left",   "l_robot/link3":   "panda_link3_left",
        "l_robot/link4":   "panda_link4_left",   "l_robot/link5":   "panda_link5_left",
        "l_robot/link6":   "panda_link6_left",   "l_robot/link7":   "panda_link7_left",
        "l_robot/hand":    "panda_hand_left",    "l_robot/left_finger": "panda_left_finger_left", 
        "l_robot/right_finger": "panda_right_finger_left",


        # right robot
        "r_robot/link0":   "panda_link0_right",   "r_robot/link1":   "panda_link1_right",
        "r_robot/link2":   "panda_link2_right",   "r_robot/link3":   "panda_link3_right",
        "r_robot/link4":   "panda_link4_right",   "r_robot/link5":   "panda_link5_right",
        "r_robot/link6":   "panda_link6_right",   "r_robot/link7":   "panda_link7_right",
        "r_robot/hand":    "panda_hand_right",    "r_robot/left_finger": "panda_left_finger_right",
        "r_robot/right_finger": "panda_right_finger_right",

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

