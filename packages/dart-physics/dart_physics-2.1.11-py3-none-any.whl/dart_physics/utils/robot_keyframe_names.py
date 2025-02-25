
import numpy as np 
from dart_physics.utils.run_functions import * 
from pathlib import Path
from dart_physics.robot_cfgs import * 

_HERE = Path(__file__).resolve().parent


allegro_cfg = {

    "robot": { 
        "l_robot": RobotConfig( 
                    xml_path = (_HERE / "../assets" / "wonik_allegro" / "left_hand.xml").as_posix(),
                    home_q = np.array([-0.5, 0.0, 0.3, 0, 0, 0, 1] + [0.] * 16), 
                    freejoint = True, 
                ), 
        "r_robot": RobotConfig(
                    xml_path = (_HERE / "../assets" / "wonik_allegro" / "right_hand.xml").as_posix(),
                    home_q = np.array([0.5, 0.0, 0.3, 0, 0, 0, 1] + [0.] * 16),
                    freejoint = True,
                ) 
    }, 
        
    "points" : { 
        "left_wrist":  FingerKeypoints("left", 0, "left_wrist_target", "l_robot/palm", weld = True, avp_transform = rot_z(90) @ rot_x(90)), 
        "right_wrist": FingerKeypoints("right", 0, "right_wrist_target", "r_robot/palm", weld = True), 

        "left_ff":     FingerKeypoints("left", 9, "left_ff_tip_target", "l_robot/ff_tip", type = "site"),
        "left_mf":      FingerKeypoints("left", 14, "left_mf_tip_target", "l_robot/mf_tip", type = "site"),
        "left_rf":      FingerKeypoints("left", 19, "left_rf_tip_target", "l_robot/rf_tip", type = "site"),
        "left_th":      FingerKeypoints("left", 4, "left_th_tip_target", "l_robot/th_tip", type = "site"),
        
        "right_ff":     FingerKeypoints("right", 9, "right_ff_tip_target", "r_robot/ff_tip", type = "site"),
        "right_mf":     FingerKeypoints("right", 14, "right_mf_tip_target", "r_robot/mf_tip", type = "site"),
        "right_rf":     FingerKeypoints("right", 19, "right_rf_tip_target", "r_robot/rf_tip", type = "site"),
        "right_th":     FingerKeypoints("right", 4, "right_th_tip_target", "r_robot/th_tip", type = "site"),
    },

    "avp_calib": { 

        "left_ff": {"scale": 1.4, "offset": np.array([-0.02, 0.0, 0.0])},
        "left_mf": {"scale": 1.3, "offset": np.array([+0.00, 0.0, 0.0])},
        "left_rf": {"scale": 1.3, "offset": np.array([+0.02, 0.0, 0.0])},
        "left_th": {"scale": 1.0, "offset": np.array([+0.00, 0.0, 0.0])},

        "right_ff": {"scale": 1.2, "offset": np.array([0.0, -0.02, 0.0])},
        "right_mf": {"scale": 1.2, "offset": np.array([0.0, -0.02, 0.0])},
        "right_rf": {"scale": 1.3, "offset": np.array([0.0, +0.02, 0.0])},
        "right_th": {"scale": 1.0, "offset": np.array([0.0, +0.00, 0.0])},

    }, 

    "ik_task" : [
        IKTasks(root = "left_wrist", target = "left_rf", scale = 1.3), 
        IKTasks(root = "left_wrist", target = "left_mf", scale = 1.2),
        IKTasks(root = "left_wrist", target = "left_ff", scale = 1.2),
        IKTasks(root = "left_wrist", target = "left_th", scale = 1.0),

        IKTasks(root = "right_wrist", target = "right_rf", scale = 1.3),
        IKTasks(root = "right_wrist", target = "right_mf", scale = 1.2),
        IKTasks(root = "right_wrist", target = "right_ff", scale = 1.2),
        IKTasks(root = "right_wrist", target = "right_th", scale = 1.0),
    ],

    "joints" : [ 
        # left hand 
        "l_robot/rfj0", "l_robot/rfj1", "l_robot/rfj2", "l_robot/rfj3",
        "l_robot/mfj0", "l_robot/mfj1", "l_robot/mfj2", "l_robot/mfj3",
        "l_robot/ffj0", "l_robot/ffj1", "l_robot/ffj2", "l_robot/ffj3",
        "l_robot/thj0", "l_robot/thj1", "l_robot/thj2", "l_robot/thj3",

        # right hand
        "r_robot/rfj0", "r_robot/rfj1", "r_robot/rfj2", "r_robot/rfj3",
        "r_robot/mfj0", "r_robot/mfj1", "r_robot/mfj2", "r_robot/mfj3",
        "r_robot/ffj0", "r_robot/ffj1", "r_robot/ffj2", "r_robot/ffj3",
        "r_robot/thj0", "r_robot/thj1", "r_robot/thj2", "r_robot/thj3",
    ],

    "bodies":  {
        # ff 
        "l_robot/ff_base":   "left_allegro_ff_base",   "l_robot/ff_distal":   "left_allegro_ff_distal", 
        "l_robot/ff_medial": "left_allegro_ff_medial", "l_robot/ff_proximal": "left_allegro_ff_proximal", 
        "l_robot/ff_tip": "left_allegro_ff_tip", 

        # mf 
        "l_robot/mf_base":   "left_allegro_mf_base",   "l_robot/mf_distal":   "left_allegro_mf_distal", 
        "l_robot/mf_medial": "left_allegro_mf_medial", "l_robot/mf_proximal": "left_allegro_mf_proximal", 
        "l_robot/mf_tip": "left_allegro_mf_tip", 

        # rf 
        "l_robot/rf_base":   "left_allegro_rf_base",   "l_robot/rf_distal":   "left_allegro_rf_distal",
        "l_robot/rf_medial": "left_allegro_rf_medial", "l_robot/rf_proximal": "left_allegro_rf_proximal",
        "l_robot/rf_tip": "left_allegro_rf_tip",

        # th
        "l_robot/th_base":   "left_allegro_th_base",   "l_robot/th_distal":   "left_allegro_th_distal",
        "l_robot/th_medial": "left_allegro_th_medial", "l_robot/th_proximal": "left_allegro_th_proximal",
        "l_robot/th_tip": "left_allegro_th_tip",

    } 

} 

mocap2frame = { 
    "dual_free_shadow": { 
        "lh_thdistal_target": "l_robot/lh_thdistal",
        "lh_ffdistal_target": "l_robot/lh_ffdistal",
        "lh_mfdistal_target": "l_robot/lh_mfdistal",
        "lh_rfdistal_target": "l_robot/lh_rfdistal",
        "lh_lfdistal_target": "l_robot/lh_lfdistal",

        "rh_thdistal_target": "r_robot/rh_thdistal",
        "rh_ffdistal_target": "r_robot/rh_ffdistal",
        "rh_mfdistal_target": "r_robot/rh_mfdistal",
        "rh_rfdistal_target": "r_robot/rh_rfdistal",
        "rh_lfdistal_target": "r_robot/rh_lfdistal",
    }, 

    "dual_free_allegro":  { 
        "left_rf_tip_target": "l_robot/rf_tip",
        "left_mf_tip_target": "l_robot/mf_tip",
        "left_ff_tip_target": "l_robot/ff_tip",
        "left_th_tip_target": "l_robot/th_tip",

        "right_rf_tip_target": "r_robot/rf_tip",
        "right_mf_tip_target": "r_robot/mf_tip",
        "right_ff_tip_target": "r_robot/ff_tip",
        "right_th_tip_targe,t": "r_robot/th_tip",
    }
    
}

weld = {
    "dual_free_shadow": { 
        "left_wrist_target": "l_robot/lh_wrist",
        "right_wrist_target": "r_robot/rh_wrist",
    }, 

    "dual_free_allegro":  { 
        "left_wrist_target": "l_robot/palm", 
        "right_wrist_target": "r_robot/palm"

    }
}

ikrel = {
    # root: frame 
    "dual_free_allegro": { 
        "l_robot/palm": "l_robot/rf_tip", 
        "l_robot/palm": "l_robot/"
    }
}


avp2mocap = { 
    "dual_free_shadow": { 
        "right": {
            0 : "right_wrist_target", 
            4 : "rh_thdistal_target",
            9 : "rh_ffdistal_target",
            14: "rh_mfdistal_target",
            19: "rh_rfdistal_target",
            24: "rh_lfdistal_target",
        }, 
        "left": {
            0 : "left_wrist_target", 
            4 : "lh_thdistal_target",
            9 : "lh_ffdistal_target",
            14: "lh_mfdistal_target",
            19: "lh_rfdistal_target",
            24: "lh_lfdistal_target",
        },
    }, 

    "dual_free_allegro": { 
        "left": {
            "0": "ri"
        }
    }
}


joints = { 
    "dual_free_shadow": [ 
                            "r_robot/rh_FFJ4",
                          "r_robot/rh_FFJ3",
                            "r_robot/rh_FFJ2",
                            "r_robot/rh_FFJ1",
                            "r_robot/rh_MFJ4",
                            "r_robot/rh_MFJ3",
                            "r_robot/rh_MFJ2",
                            "r_robot/rh_MFJ1",
                            "r_robot/rh_RFJ4",
                            "r_robot/rh_RFJ3",
                            "r_robot/rh_RFJ2",
                            "r_robot/rh_RFJ1",
                            "r_robot/rh_LFJ5",
                            "r_robot/rh_LFJ4",
                            "r_robot/rh_LFJ3",
                            "r_robot/rh_LFJ2",
                            "r_robot/rh_LFJ1",
                            "r_robot/rh_THJ5",
                            "r_robot/rh_THJ4",
                            "r_robot/rh_THJ3",
                            "r_robot/rh_THJ2",
                            "r_robot/rh_THJ1",

                            "l_robot/lh_FFJ4",
                            "l_robot/lh_FFJ3",
                            "l_robot/lh_FFJ2",
                            "l_robot/lh_FFJ1",
                            "l_robot/lh_MFJ4",
                            "l_robot/lh_MFJ3",
                            "l_robot/lh_MFJ2",
                            "l_robot/lh_MFJ1",
                            "l_robot/lh_RFJ4",
                            "l_robot/lh_RFJ3",
                            "l_robot/lh_RFJ2",
                            "l_robot/lh_RFJ1",
                            "l_robot/lh_LFJ5",
                            "l_robot/lh_LFJ4",
                            "l_robot/lh_LFJ3",
                            "l_robot/lh_LFJ2",
                            "l_robot/lh_LFJ1",
                            "l_robot/lh_THJ5",
                            "l_robot/lh_THJ4",
                            "l_robot/lh_THJ3",
                            "l_robot/lh_THJ2",
                            "l_robot/lh_THJ1"
                    ]
}