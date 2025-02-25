
from dart_physics.robot_cfgs import * 
from pathlib import Path
import mujoco
import dart_physics.mink as mink 

_HERE = Path(__file__).resolve().parent


def qpos2ctrl(model, data, qpos_target): 

    ctrl = np.zeros(8)
    ctrl[:7] = qpos_target[0:7]

    # gripper control
    tip1 = mink.SE3.from_mocap_name(model, data, "left_lf_target").as_matrix()
    tip2 = mink.SE3.from_mocap_name(model, data, "left_rf_target").as_matrix()

    finger_dist = np.linalg.norm(tip1[:3, 3] - tip2[:3, 3])

    max_grip = data.qpos[8] - 0.01

    ctrl[-1] = np.clip(finger_dist - 0.01, max_grip, 0.04)

    return ctrl 


robot_cfg = {

    "name": "left_panda",

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
    }, 

    "qpos2ctrl": qpos2ctrl, 
    "obj_startidx": (7+2) , 
        
    "points" : { 

        "left_lb":     FingerKeypoints("left", 7, "left_lb_target", "l_robot/left_finger_base", type = "body"),
        "left_lf":      FingerKeypoints("left", 9, "left_lf_target", "l_robot/left_finger_tip", type = "body"),
        "left_rb":      FingerKeypoints("left", 2, "left_rb_target", "l_robot/right_finger_base", type = "body"),
        "left_rf":      FingerKeypoints("left", 4, "left_rf_target", "l_robot/right_finger_tip", type = "body"),
    },

    "avp_calib": { 

        "left_lb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_lf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_rb": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},
        "left_rf": {"scale": 1.0, "offset": np.array([0.0, 0.0, 0.0])},

    }, 

    "ik_task" : [
        IKTasks(target = "left_lb"), 
        IKTasks(target = "left_lf", pos_cost = 1.5),
        IKTasks(target = "left_rb"),
        IKTasks(target = "left_rf", pos_cost = 1.5),
    ],

    "joints" : ['l_robot/joint{}'.format(i) for i in range(1, 8)], 

    "bodies":  {
        # left robot
        "l_robot/link0":   "panda_link0_left",   "l_robot/link1":   "panda_link1_left", 
        "l_robot/link2":   "panda_link2_left",   "l_robot/link3":   "panda_link3_left",
        "l_robot/link4":   "panda_link4_left",   "l_robot/link5":   "panda_link5_left",
        "l_robot/link6":   "panda_link6_left",   "l_robot/link7":   "panda_link7_left",
        "l_robot/hand":    "panda_hand_left",    "l_robot/left_finger": "panda_left_finger_left", 
        "l_robot/right_finger": "panda_right_finger_left",

    }, 

    "cameras": [
        CameraInfo("head", pos = [-0.09433973, -0.29207777,  0.69795567], \
                   euler = [41.44131086, 0.5, 1.84107336], fovy = 47.5 ), 
        CameraInfo("wrist", attach_to = "l_robot/attachment", attach_type = "body", \
                   pos = [-0.04, 0, -0.05], euler = [0, -1.2217305, 0], fovy = 47.5),
    ]

} 
