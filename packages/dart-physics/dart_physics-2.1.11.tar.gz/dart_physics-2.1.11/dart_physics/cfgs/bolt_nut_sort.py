
import sys
from dart_physics.robot_cfgs import GeomInfo
from scipy.spatial.transform import Rotation as R
import random
from pathlib import Path
from dart_physics.utils.run_functions import * 

HERE = Path(__file__).parent.absolute()

def random_xyz(i):
    return [random.uniform(-0.1, 0.1), random.uniform(0.15, 0.2), 0.01 + 0.01 * i ]

def duplicate_objects(name, num_max): 

    objs =  [name + "_{}".format(i) if i>0 else name for i in range(num_max)]

    # replicate the object 
    import shutil 
    obj_path = f"{HERE}/../assets/custom/{name}/{name}"
    
    for i in range(len(objs)):
        copy_path = f"{HERE}/../assets/custom/{name}_{i}"
        try: 
            shutil.copytree(obj_path, copy_path)
            shutil.move(f"{copy_path}/{name}.xml", f"{copy_path}/{name}_{i}.xml")
            # change the model name in the xml file
        except: 
            pass 
        # change the xml file (name.xml) to (name{i}.xml)

    return objs

def reset_function(model, data, robot_cfg, task_cfg): 

    id = robot_cfg["obj_startidx"] 
    vid = robot_cfg["obj_startidx"] 

    table_height = task_cfg.get("table_height", 0.0)

    for ii, obj in enumerate(task_cfg['objects']): 

        if "basket" in obj: 
            pass 

        else:
            new_pos = random_xyz(ii)
            new_quat = R.from_euler('xyz', [0, 0, np.random.randint(180)], degrees = True).as_quat(scalar_first = True).tolist()

            print(obj, len(new_pos))
            data.qpos[id:id+3] = new_pos
            data.qpos[id+3:id+7] = new_quat
            data.qvel[vid:vid+6] = 0.0

            data.qpos[id+2] += table_height

            id += 7 
            vid += 6


utensils = duplicate_objects("sorting_bolt2", 5) + duplicate_objects("sorting_nut1", 5)

task_cfg = { 
    "name": "stack_dishes", 

    "objects": ["wood_basket", "wood_basket_2"] + utensils, 

    "fixed_objects": ["wood_basket", "wood_basket_2"],

    "task_description": "Sort the bolts and nuts into the baskets.",

    "cone": "elliptic", 
    "o_solref": ".000000001 1",
    "o_solimp": ".001 1",
    "impratio": "100.0",
    "multiccd": "disable" ,
    "override": "enable",

    "default_poses": {
        "wood_basket": [-0.1, 0.35, 0.0] + R.from_euler('xyz', [90, 0, 0], degrees = True).as_quat(scalar_first = True).tolist(), 
        "wood_basket_2": [+0.1, 0.35, 0.0] + R.from_euler('xyz', [90, 0, 0], degrees = True).as_quat(scalar_first = True).tolist(),
    }, 

    "reset_function": reset_function, 
    
}

task_cfg["default_poses"].update({obj: random_xyz(i) + R.from_euler('xyz', [0, 0, np.random.randint(180)], degrees = True).as_quat(scalar_first = True).tolist() for i, obj in enumerate(utensils)})



if __name__ == "__main__":


    from runs import * 
    from utils.scene_gen import construct_scene
    import mujoco
    from loop_rate_limiters import RateLimiter


    robot = "dual_panda"
    robot_cfg = load_robot_cfg(robot)

    model = construct_scene(task_cfg, robot_cfg)
    data = mujoco.MjData(model)

    viewer = mujoco.viewer.launch_passive(
        model=model, data=data, show_left_ui=True, show_right_ui=True)
    
    mujoco.mj_resetDataKeyframe(model, data, 0)
    mujoco.mj_forward(model, data)
    mujoco.mj_camlight(model, data)

    rate = RateLimiter(500)
    while True:
        mujoco.mj_step(model, data)
        viewer.sync()
        rate.sleep()
    