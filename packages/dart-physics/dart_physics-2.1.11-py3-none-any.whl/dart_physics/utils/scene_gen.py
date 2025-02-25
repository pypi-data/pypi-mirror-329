
from dm_control import mjcf
import dexhub 
import numpy as np 
import mujoco
from pathlib import Path
from scipy.spatial.transform import Rotation as R 
# from robot_descriptions import robotiq_2f85_mj_description, panda_mj_description, allegro_hand_mj_description, aloha_mj_description, ur5e_mj_description
import os 
from dart_physics.utils.mesh_download import * 
import subprocess 
from dart_physics.utils.robot_keyframe_names import * 
from copy import deepcopy 

_HERE = Path(__file__).parent

def obj2mjcf(obj_name, sdf = False ):

    try: 
        path = download_mesh(obj_name)
        obj_path = os.path.join(path, obj_name, f"{obj_name}.xml")
        print(obj_path)
        if os.path.exists(obj_path):
            print("Found cached convex decomposition!")
            return mjcf.from_path(obj_path)

    except: 

        xml_path = os.path.join(_HERE, "..",  "assets", "custom", obj_name, f"{obj_name}.xml")
        return mjcf.from_path(xml_path)
        
        
    
    print(path)
    if sdf: 
        process = subprocess.Popen(
            [
                "obj2mjcf",
                "--obj-dir",
                str(path),
                "--save-mjcf",
                "--verbose",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    else: 
        process = subprocess.Popen(
            [
                "obj2mjcf",
                "--obj-dir",
                str(path),
                "--save-mjcf",
                "--decompose",
                "--verbose",
                # "--coacd-args.preprocess-resolution", 
                # "100", 
                # "--coacd-args.threshold", 
                # "0.01", 
                # "--coacd-args.mcts-iterations", 
                # "200", 
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    # Write 'n' to the process input
    stdout, stderr = process.communicate(input=b'n\n')

    return mjcf.from_path(obj_path)




def construct_scene(task_cfg, robot_cfg, thirdperson = False): 


    root = mjcf.RootElement()
    root.statistic.meansize = 0.08
    getattr(root.visual, "global").azimuth = -120
    getattr(root.visual, "global").elevation = -20

    root.option.timestep = ".002"
    root.option.integrator = task_cfg.get("integrator", "implicitfast")
    if robot_cfg["name"] == "DualPanda": 
        root.option.integrator = "implicitfast"
    # if robot_cfg["name"] == "RBY1": 
    #     root.option.integrator = "implicitfast"

    root.option.cone = robot_cfg.get("cone", "pyramidal")
    root.option.o_solref = task_cfg.get("o_solref", ".0000000001 1")
    root.option.o_solimp = task_cfg.get("o_solimp", "0.01 1")
    root.option.impratio = task_cfg.get("impratio", "10000.0")
    # root.option.o_friction= "1 1 0.5 0.5"
    root.option.flag.multiccd = task_cfg.get("multiccd", "disable")
    root.option.flag.override = task_cfg.get("override", "enable")
    root.option.solver = task_cfg.get("solver", "Newton")
    # if robot_cfg["name"] == "RBY1": s
    #     root.option.solver = "PGS"

    root.size.memory = "1000M" 

    root.worldbody.add("light", pos="0 0 1.5", directional="true")

    root.asset.add("texture", name="grid", type="2d", builtin="checker", rgb1="0.2 0.3 0.4", rgb2="0.1 0.2 0.3", width="256", height="256", mark="cross", markrgb=".0 .0 .0")
    root.asset.add("material", name="grid", texture="grid", texrepeat="1 1", texuniform="true")

    floor = root.worldbody.add("geom", name="floor", size="5 5 0.01", type="plane", material="grid")

    table_height = task_cfg.get("table_height", 0.0)    
    

    for robot_name, robot in robot_cfg['robots'].items():
        robot: RobotConfig
        robot_mjcf = mjcf.from_path(robot.xml_path)
        robot_mjcf.model = robot_name

        if robot.freejoint: 
            root.attach(robot_mjcf).add("freejoint")

        elif robot.attach_to is not None: 

            pos = robot.attach_to[:3]
            quat = robot.attach_to[3:]

            site = root.worldbody.add("site", name=f"{robot_name}_site", pos=pos,  quat=quat)
            site.attach(robot_mjcf)            


        for new_body in robot.add_bodies: 
            new_body: NewBodyConfig
            add_new_body_to_model(root, robot_name, new_body.attach_to, \
                                  new_body.body_name, new_body.pos, new_body.quat)



    try: 
        eq = root.equality
    except:
        eq = root.add("equality")

    for finger in robot_cfg["reverse_points"].values() if thirdperson else robot_cfg["points"].values():

        add_mocap_body_to_model(root, finger.mocap_frame, 1)

        if finger.weld: 
            eq.add("weld", body1 = f"{finger.mocap_frame}", body2 = finger.body_frame) # , solimp="1 1 0.5", solref="0.01 0.3")




    root, object_default_qpos = add_object_to_model(root, task_cfg)
    try: 
        for obj in task_cfg["objects"]:
            attach_viz_axis_to_body(root, obj + "/" + obj, [0, 0, 0], 6)
    except:
        pass 

    for obj in task_cfg["objects"]:
        try: 
            df = root.default.find("default", f"{obj}/collision")
            # dff = df.find("default", "cambridge_mug/collision")
            df.geom.condim = 6
            df.geom.friction = "10 10 10 10 10" 
        except:
            print(f"Object condim / friction {obj} not found in the model")


    home_q = [] 
    for robot_name, robot in robot_cfg['robots'].items(): 
        if robot.home_q is not None: 
            home_q.append(np.array(robot.home_q))

    try: 
        qpos = np.concatenate(home_q + [np.concatenate(object_default_qpos)])
    except:
        qpos = np.concatenate(home_q)
    print(len(qpos))
    qpos_string = " ".join([str(q) for q in qpos])
    
    for robot_name in robot_cfg['robots'].keys(): 
        root.keyframe.remove(f"{robot_name}/home")

    root.keyframe.add("key", name="home", time=0, qpos= qpos_string)

    # add front camera 

    # cam_body = add_mocap_body_to_model(root, "main_front") 
    # cam_body.pos = [-0.036, 1.767, 0.819]
    # cam_body.quat = R.from_euler("xyz", [0, 0, 0], degrees = True).as_quat(scalar_first = True)

    root.worldbody.add("camera", name="main_front", fovy=70, pos=[-0.0, 0.8, 0.819], xyaxes=[-1.000, -0.00, -0.000, 0.008, -1.00, 1.0])
# <camera pos="-0.036 1.767 0.819" xyaxes="-1.000 -0.020 -0.000 0.008 -0.420 0.907"/>


    robot_cams = robot_cfg.get("cameras", [])

    for i, camera in enumerate(robot_cams):
        camera: CameraInfo 
        
        if camera.attach_to is not None: 
            assert camera.attach_type is not None 

            print(f"Attaching camera {i} to {camera.attach_to} of type {camera.attach_type}")

            mat = R.from_euler("xyz", camera.euler, degrees = False).as_matrix() 
            mat = mat @ rot_y(-90)[:3, :3] @ rot_z(-90)[:3, :3]
            quat = R.from_matrix(mat).as_quat(scalar_first = True)


            root, m = attach_body_to_body(root, body_name = camera.attach_to, mocap_name = camera.name, \
                                    pos = camera.pos, quat = quat, size = 1)
            m.add("camera", name=camera.name, fovy=camera.fovy)

        else: 

            cam_body = add_mocap_body_to_model(root, camera.name) 
            cam_body.pos = camera.pos
            cam_body.quat = R.from_euler("xyz", camera.euler, degrees = True).as_quat(scalar_first = True)

            cam_body.add("camera", name=camera.name, fovy=camera.fovy)


    if "lights" in task_cfg:
        for light_cfg in task_cfg["lights"]:
            light_cfg = deepcopy(light_cfg)
            del light_cfg["custom"]
            root.worldbody.add("light", **light_cfg)

    if "render" in task_cfg:
        width, height = task_cfg["render"]["resolution"]

    getattr(root.visual, "global").offwidth = 640
    getattr(root.visual, "global").offheight = 640

    # # Add cameras to the model
    if "render" in task_cfg:
        cameras_cfg = task_cfg["render"].get("cameras", [])
        cameras_body = add_mocap_body_to_model(root, "head2", len(cameras_cfg))
        
        for i, camera_cfg in enumerate(cameras_cfg):
            camera_cfg = deepcopy(camera_cfg)
            mocap_body_name = f"camera_{camera_cfg['name']}"
            cameras_body = add_mocap_body_to_model(root, mocap_body_name, size=1)
            
            # Remove pos & rot from the camera config
            # Position and rotation will be set by the mocap body
            camera_cfg["pos"] = [0, 0, 0]
            for key in ["quat", "eulers", "euler", "axisangle", "xyaxes", "zaxis"]:
                if key in camera_cfg:
                    del camera_cfg[key]
                
            # Add resolution to the camera
            camera_cfg["resolution"] = task_cfg["render"]["resolution"]
                
            # Add camera to the model
            # print(f"Adding camera {i} with config: {camera_cfg}")
            cameras_body.add("camera", **camera_cfg)

    try: 
        material_names = ["white", "off_white", "black", "green", "light_blue"]
        reflectance = 0.2
        shininess = reflectance * 2
        specular = reflectance * 0.5

        for robot in robot_cfg["robots"].keys():
            for material_name in material_names:
                root.asset.find("material", f"{robot}/{material_name}").reflectance = reflectance
                root.asset.find("material", f"{robot}/{material_name}").shininess = shininess
                root.asset.find("material", f"{robot}/{material_name}").specular = specular

        print("material property set.")

    except:
        pass 


    # save xml     
    with open("scene.xml", "w") as f:
        f.write(root.to_xml_string())

    # dexhub.register_sim(root)
    
    # if meshcat: 

    #     from utils.meshcat_viz import MJCMeshcat
    #     from io import BytesIO

    #     mjc = MJCMeshcat()

    #     meshcat_dict = {} 

    #     meshcat_dict["material"] = {}
    #     for material in root.asset.find_all("material"):
    #         name = material.full_identifier 
    #         rgba = material.rgba
    #         texture = material.texture

    #         if texture is not None and texture != "grid": 
    #             texture_contents = BytesIO(texture.file.contents)
    #         else: 
    #             texture_contents = None
            
    #         # for method in dir(material):
    #         #     print(method, ':', str(getattr(material, method)))  

    #         mjc.register_material(name, texture_contents, rgba)

    #     # while True:
    #     #     pass 
            

    #     for mesh in root.asset.find_all("mesh"):

    #         input_io = BytesIO(mesh.file.contents)

    #         try: 
    #             scale = mesh.scale[0]
    #         except:
    #             scale = 1.0

    #         # print(mesh.name, mesh.file.extension, scale)
    #         mjc.register_mesh(mesh.name, mesh.file.extension, input_io, scale)


    #     for body in root.worldbody.find_all("body"):
    #         if body.geom is None: 
    #             continue
    #         for geom in body.geom:
    #             # print(dir(geom))
    #             # print(geom.__class__)
    #             # for method in dir(geom):
    #             #     print(method, ':', str(getattr(geom, method)))
    #             if "collision" in str(geom.dclass): 
    #                 pass
    #             else:
    #                 try: 
    #                     if geom.material is None: 
    #                         # print(str(geom.dclass))
    #                         material = geom.dclass.geom.material 
    #                     else:
    #                         material = geom.material
    #                     mjc.register_geom(body.full_identifier, geom.mesh.name, material.full_identifier, geom.pos, geom.quat)
    #                 except Exception as e:
    #                     # print(body.full_identifier, geom.name, e)
    #                     pass 

    # else:
    #     mjc = None 

    return mujoco.MjModel.from_xml_string(root.to_xml_string(), root.get_assets()), root 


def add_new_body_to_model(root, robot_name, attach_to, body_name, pos_string, quat_string): 

    rf = root.find("body", f"{robot_name}/{attach_to}")
    rfb = rf.add("body", name=body_name, pos= pos_string, quat = quat_string)
    # rfb.add(
    #     "geom",
    #     group = 5, 
    #     type="sphere",
    #     size=".02 .02 .02",
    #     contype="0",
    #     conaffinity="0",
    #     rgba=".6 .3 .3 .7",
    # )




def add_mocap_body_to_model(root, name, size = 1, pos = [0, 0, 0], quat = [1, 0, 0, 0]): 
    default = 0.01 

    size = size * default

    pos = " ".join([str(p) for p in pos])
    quat = " ".join([str(q) for q in quat])

    site = root.worldbody.add("body", name=name, mocap=True)
    site.add(
        "geom",
        type="box",
        size=f"{size} {size} {size}",
        contype="0",
        conaffinity="0",
        rgba=".3 .6 .3 .9",
        group = 4, 
    )
    site.add(
        "geom",
        type="box",
        size=f"{size} .002 .002",
        contype="0",
        conaffinity="0",
        rgba="1 0 0 1",
        pos=f"{size} 0 0",
        group = 4, 
    )
    # length 0.07 cylinder with 0.01 radius in green color indicating y-axis
    site.add(
        "geom",
        type="box",
        size=f".002 {size} .002",
        contype="0",
        conaffinity="0",
        rgba="0 1 0 1",
        pos = f"0 {size} 0",
        group = 4, 

    )
    # length 0.07 cylinder with 0.01 radius in blue color indicating z-axis
    site.add(
        "geom",
        type="box",
        size=f".002 .002 {size}",
        contype="0",
        conaffinity="0",
        rgba="0 0 1 1",
        pos = f"0 0 {size}",
        group = 4, 

    )

    return site

def add_targets_to_model(root): 

    body = root.worldbody.add("body", name="l_target", mocap=True)
    body.add(
        "geom",
        group = 5, 
        type="box",
        size=".05 .05 .05",
        contype="0",
        conaffinity="0",
        rgba=".3 .6 .3 .5",
    )
    # length 0.07 cylinder with 0.01 radius in red color indicating x-axis
    body.add(
        "geom",
        type="box",
        size=".10 .007 .007",
        contype="0",
        conaffinity="0",
        rgba="1 0 0 1",
        pos=".05 0 0",
    )
    # length 0.07 cylinder with 0.01 radius in green color indicating y-axis
    body.add(
        "geom",
        type="box",
        size=".007 .10 .007",
        contype="0",
        conaffinity="0",
        rgba="0 1 0 1",
        pos = "0 .05 0"
    )
    # length 0.07 cylinder with 0.01 radius in blue color indicating z-axis
    body.add(
        "geom",
        type="box",
        size=".007 .007 .10",
        contype="0",
        conaffinity="0",
        rgba="0 0 1 1",
        pos = "0 0 .05"
    )

    body = root.worldbody.add("body", name="r_target", mocap=True)
    body.add(
        "geom",
        type="box",
        size=".05 .05 .05",
        contype="0",
        conaffinity="0",
        rgba=".3 .3 .6 .5",
    )
    body.add(
        "geom",
        type="box",
        size=".10 .007 .007",
        contype="0",
        conaffinity="0",
        rgba="1 0 0 1",
        pos=".05 0 0",
    )
    # length 0.07 cylinder with 0.01 radius in green color indicating y-axis
    body.add(
        "geom",
        type="box",
        size=".007 .10 .007",
        contype="0",
        conaffinity="0",
        rgba="0 1 0 1",
        pos = "0 .05 0"
    )
    # length 0.07 cylinder with 0.01 radius in blue color indicating z-axis
    body.add(
        "geom",
        type="box",
        size=".007 .007 .10",
        contype="0",
        conaffinity="0",
        rgba="0 0 1 1",
        pos = "0 0 .05"
    )

    return root 



def attach_viz_axis_to_body(root, body_name, pos, size = 1): 

    default = 0.01 

    size = size * default
    print(body_name)
    body = root.worldbody.find("body", body_name)
    pos_str = " ".join([str(p) for p in pos])
    if "/" in body_name:
        site = body.add("body", name=body_name.split('/')[1] + "_axis", pos=pos_str)
    else:
        site = body.add("body", name=body_name + "_axis", pos=pos_str)
    site.add(
        "geom",
        group = 5, 
        type="box",
        size=f"{size * 0.5} {size * 0.5} {size * 0.5}",
        contype="0",
        conaffinity="0",
        rgba=".6 .3 .3 .5",
    )
    # length 0.07 cylinder with 0.01 radius in red color indicating x-axis
    site.add(
        "geom",
        group = 5, 
        type="box",
        size=f"{size} .002 .002",
        contype="0",
        conaffinity="0",
        rgba="1 0 0 .5",
        pos=f"{size} 0 0",
    )
    # length 0.07 cylinder with 0.01 radius in green color indicating y-axis
    site.add(
        "geom",
        group = 5, 
        type="box",
        size=f".002 {size} .002",
        contype="0",
        conaffinity="0",
        rgba="0 1 0 .5",
        pos = f"0 {size} 0"
    )
    # length 0.07 cylinder with 0.01 radius in blue color indicating z-axis
    site.add(
        "geom",
        group = 5, 
        type="box",
        size=f".002 .002 {size}",
        contype="0",
        conaffinity="0",
        rgba="0 0 1 .5",
        pos = f"0 0 {size}", 
    )

    return root

def attach_body_to_body(root, body_name, mocap_name, pos, quat, size = 1): 

    default = 0.01 

    size = size * default
    print(body_name)
    body = root.worldbody.find("body", body_name)
    pos_str = " ".join([str(p) for p in pos])
    quat_str = " ".join([str(q) for q in quat])
    site = body.add("body", name=mocap_name, pos=pos_str, quat=quat_str)
    site.add(
        "geom",
        group = 5, 
        type="box",
        size=f"{size * 0.5} {size * 0.5} {size * 0.5}",
        contype="0",
        conaffinity="0",
        rgba=".6 .3 .3 .5",
    )
    # length 0.07 cylinder with 0.01 radius in red color indicating x-axis
    site.add(
        "geom",
        group = 5, 
        type="box",
        size=f"{size} .002 .002",
        contype="0",
        conaffinity="0",
        rgba="1 0 0 .5",
        pos=f"{size} 0 0",
    )
    # length 0.07 cylinder with 0.01 radius in green color indicating y-axis
    site.add(
        "geom",
        group = 5, 
        type="box",
        size=f".002 {size} .002",
        contype="0",
        conaffinity="0",
        rgba="0 1 0 .5",
        pos = f"0 {size} 0"
    )
    # length 0.07 cylinder with 0.01 radius in blue color indicating z-axis
    site.add(
        "geom",
        group = 5, 
        type="box",
        size=f".002 .002 {size}",
        contype="0",
        conaffinity="0",
        rgba="0 0 1 .5",
        pos = f"0 0 {size}", 
    )

    return root, site



def add_object_to_model(model, task_cfg): 

    print("fixed objects", task_cfg.get("fixed_objects", []))


    for object in task_cfg['objects']:
        obj = obj2mjcf(object)   # mjcf.from_path("/Users/yhpark/workspace/mj_aws/assets/custom/yellow_drill/yellow_drill/yellow_drill.xml")
        # print("processing  " + object)
        if "piano" in object: 
            model.worldbody.attach(obj)

        elif object in task_cfg.get("fixed_objects", []):
            
            body = model.worldbody.attach(obj)
            body.pos = task_cfg['default_poses'][object][:3]
            body.quat = task_cfg['default_poses'][object][3:7]

        else:
            model.worldbody.attach(obj).add("freejoint")

    object_default_qpos = [] 
    for obj in task_cfg['objects']:

        if obj == "cube": 
            print("here?")

            scrambled_pose = '3.1426 -3.12861 1.56976 -0.000984066 -4.71318 -4.71315 0.500066 0.499657 -0.49985 -0.500427 -5.4361e-06 -0.00105736 0.00700177 0.999975 -0.000159023 0.707166 -0.000551277 0.707047 0.499996 -0.500004 -0.499944 0.500056 -0.000206243 0.000330177 -0.707384 0.706829 -0.707495 -0.000335452 0.706718 -0.000199843 -0.707043 0.004306 0.707141 -0.00483592 -0.50299 -0.496992 -0.502969 -0.497014 -0.000732543 1.04854e-06 -0.707166 -0.707047 1 -6.94691e-05 -0.000515106 0.000382513 0.499994 0.501014 -0.500005 0.498985 -0.00464879 -0.707305 -0.706879 0.00452857 0.00437059 0.707365 -0.706822 0.00420462 -0.000935246 -0.000398716 -0.70222 0.711959 -0.500046 -0.501052 0.500044 -0.498856 0.000141309 3.32215e-05 0.999982 -0.00592773 0.00127499 -0.706838 -0.707374 0.000114238 -0.70796 0.00437499 -0.706218 0.00552882 0.000173516 0.000281969 -0.70708 -0.707134 0.000199487 0.706843 -0.70737 -0.000112591'

            scrambled_pose = list(map(float, scrambled_pose.split()))

            pose = [0, 0.3, 0.1] + [1, 0, 0 ,0] + \
                    scrambled_pose
            # pose = [] 

        elif obj == "piano": 

            pose_key = "-0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000623174 -0.000169732 -0.000169732"
            # split the string by space and convert to float
            pose = [float(x) for x in pose_key.split(" ")]


        elif obj in task_cfg.get("fixed_objects", []):
            # print(object + " is fixed")
            pose = [] 

        else: 
            pose = task_cfg['default_poses'][obj]

        object_default_qpos.append(np.array(pose))

    # b = model.worldbody.add("body")
    # b.add("geom", type="box", size=".05 .05 .05", rgba="1 0 0 1")
    # b.add("freejoint")
    # object_default_qpos.append(np.array([0.0, 0.0, 0.026, 0.0, 0.0, 0.0, 1.0]))

    return model, object_default_qpos
