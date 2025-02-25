import os 
import gdown 
from pathlib import Path 
import platform
import subprocess
from dart_physics.dirs import * 

CUR_PATH = Path(__file__).parent.absolute()


GDRIVE_URL_MAP = {
    'yellow_drill': {
        'usdz': 'https://drive.google.com/file/d/1oV-Dyjdd22SljjD9UoA1Rv0K2s-DTJrE/view?usp=sharing', 
        'obj': 'https://drive.google.com/file/d/166iY57usZZrc0PXBiwBXEP599KL7jrKC/view?usp=sharing',
        'gltf': 'https://drive.google.com/file/d/1luhLk-1GZLs3Di_-axxy0UEMrC0vLDTQ/view?usp=sharing',
    },
    'yellow_drill_battery': {
        'obj': 'https://drive.google.com/file/d/1DC0BFLaLKW18gf0OXwmnpM7gYzBnuABI/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/1aWWi0kGzBgyKfJe1vunFyfjLIzXISOL1/view?usp=sharing', 
        'gltf': 'https://drive.google.com/file/d/1Oar0KiJ2S4KKt0TvcFlU3jBlCZA9y_Sy/view?usp=sharing',
    },
    'tongue': {
        'obj': 'https://drive.google.com/file/d/1G-zvUMpMewEihWbS0j36tX47uN3jooRg/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/17qhCX6guWPo5R8rxDKZG1NSVgDUBd_4e/view?usp=sharing',
        'gltf': 'https://drive.google.com/file/d/1abLOreAsmY-HivZaNBaot85uJ5uI2Idn/view?usp=sharing',
    },
    'red_marker': {
        'obj': 'https://drive.google.com/file/d/17u1t1BpybIsMDBR-o9H0EgPjpZYXrKgi/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/1Gtnlt-2FLk4LfvoCrqnTrpWfqXvlb56n/view?usp=sharing',
        'gltf': 'https://drive.google.com/file/d/1pBKIQE_B-uk0xvsRy5dIpNpMmyKUvx6e/view?usp=sharing', 
    },
    'red_ladle': {
        'obj':  'https://drive.google.com/file/d/1IC4TOuJwdIUJtyxsq3PXENs9_5ONLJ4i/view?usp=sharing',
        'usdz': 'https://drive.google.com/file/d/17CjiafFC7q08Q-NXgjfK3TV5Fik7QQ4k/view?usp=sharing', 
        'gltf': 'https://drive.google.com/file/d/1Haio-gOebVRqhMlKxhjps5IVOg3WPB0U/view?usp=sharing',
    },
    'milk_tea': {
        'obj': 'https://drive.google.com/file/d/1swvaJUwYtow07fTuGv8l19amZrYmYcgS/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/1LGbpiLrrPRakes5qsHBfhxHpI2tDCaSn/view?usp=sharing',
        'gltf': 'https://drive.google.com/file/d/1GH-yRxtR3M27jGUVDHGp6RxrdW0NAYVh/view?usp=sharing', 
    },
    'hanger': {
        'obj': 'https://drive.google.com/file/d/1eSiey-7sXlZpadDeWojKfVLwPEuC3ovN/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/1uEtXlncYOEq6MUVWsq7rqKJkVAq3XdIA/view?usp=sharing', 
        'gltf': 'https://drive.google.com/file/d/1LPYmCcSPAu66ELZPlwVSJBJBBVj7F3hN/view?usp=sharing',
    }, 
    'eraser': {
        'obj': 'https://drive.google.com/file/d/16yWjL55qxdgNfy7ZoJlldGZYcOuCdb0h/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/1zSN8hCHuszdUR3uucaYrF1rjnh2jK46n/view?usp=sharing',
        'gltf': 'https://drive.google.com/file/d/1dcD8vkPrp-7YRDCD4VtaoiLjqCbCjC2T/view?usp=sharing',
    },
    'emergency_kit': {
        'obj': 'https://drive.google.com/file/d/177-xepqmCnXkoiglszyk40B5m6q7m6bs/view?usp=sharing',
        'usdz': 'https://drive.google.com/file/d/1Cd2y5B3LiX_FTrCetECtRkj6ZgT-KGKI/view?usp=sharing', 
        'gltf': 'https://drive.google.com/file/d/1ETphpoipqnlujoQYTbVKsT9B3UOxaWoC/view?usp=sharing',
    },
    'drill': {
        'obj': 'https://drive.google.com/file/d/1-DpQaTe8IvcSDjXnom_XmkKdGSBxrNhW/view?usp=sharing',
        'usdz': 'https://drive.google.com/file/d/1RuSbBjj3n54uLiDI9xVcEhcLKaWLv54C/view?usp=sharing',
        'gltf': 'https://drive.google.com/file/d/1DHMhwWPrgrwu7wKSyEgVhPQRKdVWF1wm/view?usp=sharing',
    },
    'cleaner2': {
        'obj': 'https://drive.google.com/file/d/18MqSwqxC5v0nnjSQ760o1r_wxUxYbPSo/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/1u6Q9GyeBgWbyrIybg87ntQXBR3NUy_W-/view?usp=sharing',
        'gltf': 'https://drive.google.com/file/d/15_G9RsS2xR32dWuOth4wfMqo1lV0Xz8u/view?usp=sharing',
    },
    'cleaner': {
        'obj': 'https://drive.google.com/file/d/1fnIXmW71oBPvltHqcUE0fH4jwqEpqXgQ/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/1eMSoWYhN9SiN5CXQu3kOKh9JTjL-E82N/view?usp=sharing',
        'gltf': 'https://drive.google.com/file/d/1kYVERsbCy6SFpPBofaGToZFkzXgP3Jyl/view?usp=sharing',
    },
    'brown_basket': {
        'obj': 'https://drive.google.com/file/d/1ZG3u9DlWDhnI39Iac2G4eI9ViqC9ZAY8/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/1svaDdFu2_Nkctt00tSstCIjzniHevsFb/view?usp=sharing', 
        'gltf': 'https://drive.google.com/file/d/1CE4EeCOtd3piAe2w76lJ-jQhXfu6EmQX/view?usp=sharing',
    },
    'bluebottle_cup': {
        'obj': 'https://drive.google.com/file/d/1Nchl_y1Pb0tz36RGgVgDPakSxv6NB-UZ/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/1GSI5aZu9HnBDAYebuhQork_q4Eqn9TUd/view?usp=sharing', 
        'gltf': 'https://drive.google.com/file/d/1bzznDRiITn7OgvscKnqT2GE2i6bgdX4x/view?usp=sharing',
    },
    'blue_marker': {
        'obj': 'https://drive.google.com/file/d/1rjJNKSRvIuMLuhiE3j3dhcWPVxJr_E9T/view?usp=sharing', 
        'usdz': 'https://drive.google.com/file/d/1Sc1EI3AdNJC1hRoOZV15pKzEAuR3MX93/view?usp=sharing',
        'gltf': 'https://drive.google.com/file/d/1N5qh1ILddBs32KhBRNR2953e7t8qguxk/view?usp=sharing',
    },
    'bidex_table': {
        '0down': 'https://drive.google.com/file/d/1chd7S3Rx9Lf8N3QeUWAM0aTMQr22Y-dv/view?usp=sharing',
        '100down': 'https://drive.google.com/file/d/1_EHNWGFolg33HmS9V6A94ncvMQiLdqGW/view?usp=sharing',
    },
    'cambridge_mug': {
        'usdz': 'https://drive.google.com/file/d/1QSpbPFkB44w11HKk0JNfiW8oE_VlOxja/view?usp=sharing',
        'obj': 'https://drive.google.com/file/d/1CpFWNr0p4d6vZS8NZfenaC--elK4bhns/view?usp=sharing', 
        'gltf': 'https://drive.google.com/file/d/1hQUXvqkBMlC7HXIhUvtzVoYtEFwkIuoI/view?usp=sharing',
    }, 
    'tesla_battery_slot': {
        'usdz': 'https://drive.google.com/file/d/16o9vfsDnQJ8UcaAkhejUPfDQxzSP8ekJ/view?usp=sharing', 
        'obj': 'https://drive.google.com/file/d/1810oOAxD_7uq8hlTYj2XhBB53oQVqgEO/view?usp=sharing', 
    }, 
    'cylinder': {
        'usdz': 'https://drive.google.com/file/d/1uGFmQrmC77CTEsu_QT1IPoabSBUKzLNN/view?usp=sharing', 
        'obj': 'https://drive.google.com/file/d/1R7d-4sdT37sKKxsynBmmszNXLvKr3IQI/view?usp=sharing', 
    },

    'screw_18402_1_final': {
        'gltf': 'https://drive.google.com/file/d/1dBBCbMU8Sy_tlIr_VBH2lLvlh9pAb_R1/view?usp=sharing', 
    },
    'screw_18402_0_final': {
        'gltf': 'https://drive.google.com/file/d/1V6Diufo42uMe8XS_syJtE4euuWoAsDod/view?usp=sharing', 
    },
    'screw_18402_0B_final': {
        'gltf': 'https://drive.google.com/file/d/1jgxY8LgyYZW0HcgHtVDAg-hdyEEinSTD/view?usp=sharing', 
    },
    'screw_18402_1B_final': {
        'gltf': 'https://drive.google.com/file/d/1hIAdjwgZpXqFAQGrBK5qiywt5QcFHWfj/view?usp=sharing', 
    },
    '00112_0L_final': {
        'gltf': 'https://drive.google.com/file/d/1cLRcWmsjp9fu9qREu6pcygl9F2h_NWZF/view?usp=sharing',
    },
    '00112_1L_final' : {
        'gltf': 'https://drive.google.com/file/d/1MQqKxgE7XkNr_xwqVliynWFGypxod6US/view?usp=sharing',
    },

    '00015_0L_final': {
        'gltf': 'https://drive.google.com/file/d/1vrMGSN0f5lhxSd2iTunqawP9RnHK6wzj/view?usp=sharing',
    },
    '00015_1L_final': {
        'gltf': 'https://drive.google.com/file/d/1SSkfAcm61IYZjOOmxho7pEE-QiKaQEap/view?usp=sharing',
    },

    '00470_0L_final': {
        'gltf': 'https://drive.google.com/file/d/1aP12xpkRTGsa9n5grAbD8mkjejlblbsT/view?usp=sharing',
    },
    '00470_1L_final': {
        'gltf': 'https://drive.google.com/file/d/1O0R3IdlM0wVJC_kT2zkk0R2iKBc_xZPX/view?usp=sharing',
    },

    '19133_0L_final': {
        'gltf': 'https://drive.google.com/file/d/1MLp0ytrj50b-ezsmhEjPq_o1dJsO94QT/view?usp=sharing',
    },
    '19133_1L_final': {
        'gltf': 'https://drive.google.com/file/d/18KBvmFzhXffJDdKPKRVFVOem08FcfopG/view?usp=sharing',
    },

    'keylight_0L_final': {
        'gltf': 'https://drive.google.com/file/d/1_giV82Or6sYZYjlGMRrHQI8tA2wL524F/view?usp=sharing',
    },
    'keylight_1L_final': {
        'gltf': 'https://drive.google.com/file/d/18R8VipHXtqDVvQ7bT5NQ0iiKYkN4cxQ6/view?usp=sharing',
    },

    'aj_0L_final': {
        'gltf': 'https://drive.google.com/file/d/1Wk64Dl8Dtm8Ed07pw73F5u-aOQ_7M4jl/view?usp=sharing',
    },
    'aj_1L_final': {
        'gltf': 'https://drive.google.com/file/d/1aPEYHgAuz4cpLCgCcA2H6cdzVjmtIL0V/view?usp=sharing',
    },

    '00932_0L_final': {
        'gltf': 'https://drive.google.com/file/d/1zbgiXwoaCJVHQLnZDkfVhm3TqyG0BoC1/view?usp=sharing',
    },
    '00932_1L_final': {
        'gltf': 'https://drive.google.com/file/d/1VUHfNYR3AivPoeo4Xk9-feUSal8rR9Nb/view?usp=sharing',
    },

    '6-32-screw_final': {
        'gltf': 'https://drive.google.com/file/d/1YRnK6gBtv_p1xiWGgMN44NGW5NbJlrT2/view?usp=sharing',
    },
    '6-32-screwdriver_final': {
        'gltf': 'https://drive.google.com/file/d/1ARiZBn2CQyAojD9wybf5gEnNv0_z5NYd/view?usp=sharing',
    },
    '6-32-screwmount_final': {
        'gltf': 'https://drive.google.com/file/d/10MBqVOM8fT3Np1o-1N48mdzxoKFBEpzI/view?usp=sharing',
    },

    '18-8-bolt_final': {
        'gltf': 'https://drive.google.com/file/d/1ut7Tdn668Qzpn7ef762Y1nlKoCuai5gO/view?usp=sharing',
    },
    '18-8-nut_final': {
        'gltf': 'https://drive.google.com/file/d/1P5SPcqRyQjaH37VaO5-9gHVd4qc7s_FU/view?usp=sharing',
    },

    'power-plug_final': {
        'gltf': 'https://drive.google.com/file/d/1C4hyx3DJzjaKcXWEQNMHN-bTbr514-yB/view?usp=sharing',
    },
    'power-socket_final': {
        'gltf': 'https://drive.google.com/file/d/142uyHdq-C4cKBYi8VSkQy2UeHUFFzBMT/view?usp=sharing',
    },
    'toyA_base': {
        'obj': 'https://drive.google.com/file/d/1QeUbD6OfQkHPWbqHZ9Io5aQeHkiE-csW/view?usp=sharing', 
    },
    'toyA_four': { 
        'obj': 'https://drive.google.com/file/d/1ECyuWum3SoWm89pelEsX1sJor8MQ5EiN/view?usp=sharing', 
    },
    'toyA_four_CAD': { 
        'obj': 'https://drive.google.com/file/d/1F2mHM-F-_XTYxfnW-OTVxvS_Ow6BRlHg/view?usp=sharing', 
    },
    'toyA_one_CAD': { 
        'obj': 'https://drive.google.com/file/d/1n8SEiy1i_-LKsvg68os1Gdscq5qVCrfY/view?usp=sharing', 
    },
    'muggood': {
        'obj': 'https://drive.google.com/file/d/1eowHU0_huBKvJDwQiy9W2jtMiRFW0LsN/view?usp=sharing',
    }
}

def download_mesh(mesh_name, mesh_type = 'obj', save_dir = ASSET_STORE_DIR): 

    if not os.path.exists(save_dir): 
        os.makedirs(save_dir)


    if mesh_type == 'obj':


        if os.path.exists(f'{save_dir}/{mesh_name}/{mesh_name}.obj'):
            print(f'{mesh_name}.obj already exists in {save_dir}')
            return f'{save_dir}/{mesh_name}'

        gdrive_url = GDRIVE_URL_MAP[mesh_name][mesh_type]

        gdown.download(gdrive_url, f'{save_dir}/{mesh_name}_obj.zip', fuzzy = True)

        # check if unzip is installed
        if not check_unzip_installed():
            raise RuntimeError("Unzip is not installed. Please install unzip command line tool.")
                
        # unzip the downloaded file
        os.makedirs(f'{save_dir}/{mesh_name}', exist_ok = True)
        os.system(f'unzip -o {save_dir}/{mesh_name}_obj.zip -d {save_dir}/{mesh_name}')
        if platform.system() != "Windows":
            os.system(f'chmod -R 755 {save_dir}/{mesh_name}')  # Sets read, write, and execute permissions for user, and read and execute for group and others
            os.system(f'rm {save_dir}/{mesh_name}_obj.zip')
        else:
            os.remove(f'{save_dir}/{mesh_name}_obj.zip')
        
    elif mesh_type == 'usdz':
        if os.path.exists(f'{save_dir}/{mesh_name}.usdz'):
            print(f'{mesh_name}.usdz already exists in {save_dir}')
            return
        
        gdrive_url = GDRIVE_URL_MAP[mesh_name][mesh_type]

        gdown.download(gdrive_url, f'{save_dir}/{mesh_name}.usdz', fuzzy = True)
    elif mesh_type == 'gltf':
        if os.path.exists(f'{save_dir}/{mesh_name}.gltf'):
            print(f'{mesh_name}.gltf already exists in {save_dir}')
            return
        
        gdrive_url = GDRIVE_URL_MAP[mesh_name][mesh_type]

        gdown.download(gdrive_url, f'{save_dir}/{mesh_name}.gltf', fuzzy = True)

    print(f'{mesh_name}.{mesh_type} downloaded to {save_dir}')

    return f'{save_dir}/{mesh_name}'


def download_table(table_type = '100down', save_dir = ASSET_STORE_DIR):

    gdrive_url = GDRIVE_URL_MAP['bidex_table'][table_type]
    if table_type == '0down': 
        stl_name = 'table.stl'
    else:
        stl_name = f'table_{table_type}.stl'

    if os.path.exists(f'{save_dir}/{stl_name}'):
        print(f'{stl_name} already exists in {save_dir}')
        return

    gdown.download(gdrive_url, f'{save_dir}/{stl_name}', fuzzy = True)



def create_urdf(mesh_name, save_dir = ASSET_STORE_DIR):
    # Create the URDF file path
    urdf_file_path = os.path.join(save_dir, f'{mesh_name}.urdf')

    # Get the mesh file path
    mesh_file_path = os.path.join(save_dir, mesh_name, f'{mesh_name}.obj')
    material_file_path = os.path.join(save_dir, mesh_name, f'baked_mesh_tex0.png')
    mesh_exists = os.path.exists(material_file_path)

    # Create the URDF content
    urdf_content = f"""<?xml version="1.0"?>
<robot name="{mesh_name}">
<link name="base_link">
    <visual>
    <geometry>
        <mesh filename="{mesh_file_path}" scale="1 1 1"/>
    </geometry>
    <material name="material">
        <texture filename="{material_file_path}"/>
    </material>
    </visual>
    <collision>
    <geometry>
        <mesh filename="{mesh_file_path}" scale="1 1 1"/>
    </geometry>
    </collision>
</link>
</robot>
"""
    
    no_mesh_urdf_content = f"""<?xml version="1.0"?>
<robot name="{mesh_name}">
<link name="base_link">
    <visual>
    <geometry>
        <mesh filename="{mesh_file_path}" scale="1 1 1"/>
    </geometry>
    </visual>
    <collision>
    <geometry>
        <mesh filename="{mesh_file_path}" scale="1 1 1"/>
    </geometry>
    </collision>
</link> 
</robot>
"""

    # Write the URDF content to the file
    with open(urdf_file_path, 'w') as urdf_file:
        if mesh_exists:
            urdf_file.write(urdf_content)
        else:
            urdf_file.write(no_mesh_urdf_content)

    print(f'URDF file for {mesh_name} created at {urdf_file_path}')



def create_urdf_gltf(mesh_name, save_dir = ASSET_STORE_DIR, sdf = False, scale = 1.0):
    # Create the URDF file path
    urdf_file_path = os.path.join(save_dir, f'{mesh_name}.urdf')

    # Get the mesh file path
    mesh_file_path = os.path.join(save_dir, f'{mesh_name}.gltf')

    # Create the URDF content
    if sdf: 
        urdf_content = f"""<?xml version="1.0"?>
<robot name="{mesh_name}">
<link name="base_link">
    <visual>
    <geometry>
        <mesh filename="{mesh_file_path}" scale="{scale} {scale} {scale}"/>
    </geometry>
    </visual>
    <collision>
    <geometry>
        <mesh filename="{mesh_file_path}" scale="{scale} {scale} {scale}"/>
    </geometry>
    <sdf resolution="256"/>
    </collision>
</link>
</robot>
"""
        
    else:
        urdf_content = f"""<?xml version="1.0"?>
<robot name="{mesh_name}">
<link name="base_link">
    <visual>
    <geometry>
        <mesh filename="{mesh_file_path}" scale="{scale} {scale} {scale}"/>
    </geometry>
    </visual>
    <collision>
    <geometry>
        <mesh filename="{mesh_file_path}" scale="{scale} {scale} {scale}"/>
    </geometry>
    </collision>
</link>
</robot>
"""    
        
    # Write the URDF content to the file
    with open(urdf_file_path, 'w') as urdf_file:
        urdf_file.write(urdf_content)

    print(f'URDF file for {mesh_name} created at {urdf_file_path}')



def create_assembly_part_urdf(mesh_name, scale, save_dir):
    # Create the URDF file path
    urdf_file_path = os.path.join(save_dir, f'{mesh_name}.urdf')

    # Create the URDF content
    urdf_content = f"""<?xml version="1.0"?>
<robot name="{mesh_name}">
<link name="base_link">
    <visual>
    <geometry>
        <mesh filename="{mesh_name}_final.gltf" scale="{scale} {scale} {scale}"/>
    </geometry>
    </visual>
    <collision>
    <geometry>
        <mesh filename="{mesh_name}_final.gltf" scale="{scale} {scale} {scale}"/>
    </geometry>
    <sdf resolution="256"/>
    </collision>
</link>
</robot>
"""

    # Write the URDF content to the file
    with open(urdf_file_path, 'w') as urdf_file:
        urdf_file.write(urdf_content)

    print(f'URDF file for {mesh_name} created at {urdf_file_path}')

def check_unzip_installed():
    try:
        # Attempt to call the 'unzip' command
        result = subprocess.run(['unzip', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Check if the command returned successfully
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False