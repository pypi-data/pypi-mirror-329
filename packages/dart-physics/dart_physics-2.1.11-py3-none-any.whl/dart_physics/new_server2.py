import platform
from flask import Flask, request, jsonify
import subprocess
import signal
import os 
import psutil
import yaml
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import threading
import base64
import os
from dart_physics.runs import load_task_cfg, load_robot_cfg
from pathlib import Path
import zipfile
import gdown 

CUR_PATH = Path(__file__).resolve().parent

ASSET_URL = "https://drive.google.com/file/d/1I4qmZYZkY9rxJZ50EZUDQdIxw5KZ4mat/view?usp=sharing"


def download_and_extract_assets():
    # Import gdown after it's installed
    # Resolve the current directory to find where dart_physics is installed
    CUR_PATH = Path(__file__).resolve().parent
    ASSET_DIR = os.path.join(CUR_PATH)
    ZIP_FILE_PATH = os.path.join(ASSET_DIR, "dart_physics_assets.zip")
    
    # Check if assets are already downloaded
    if not os.path.exists(ZIP_FILE_PATH):
        print(f"Downloading assets from {ASSET_URL}...")
        gdown.download(ASSET_URL, ZIP_FILE_PATH, quiet=False, fuzzy=True)
        print("Assets downloaded.")
    else:
        print("Assets already exist, skipping download.")

    # Unzip the downloaded file
    if not os.path.exists(os.path.join(ASSET_DIR, 'assets')):  # Check if already unzipped
        print("Unzipping assets...")
        with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
            zip_ref.extractall(ASSET_DIR)
        print("Assets unzipped.")
    else:
        print("Assets already unzipped.")
        

def get_os():
    os_name = platform.system()
    if os_name == "Darwin":
        return "macOS"
    elif os_name == "Linux":
        return "Linux (Ubuntu or other)"
    else:
        return f"Other: {os_name}"


download_and_extract_assets()


# mkdir ./logs if not exists
if not os.path.exists(os.path.join(CUR_PATH, 'logs')):
    os.makedirs(os.path.join(CUR_PATH, 'logs'), exist_ok=True)

IS_MAC = get_os() == "macOS"
print("USING MAC?", IS_MAC)

app = Flask(__name__)
current_process = None

# Set up logging
log_file = 'subprocess_output.log'
logger = logging.getLogger('SubprocessLogger')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)  # Rotate after 10 MB, keep 5 backups
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

robot_script_mapper = { 
    "Single FR3": "left_panda",
    "Single Panda": "left_panda", 
    "Dual Panda": "dual_panda",
    "ALOHA": "aloha",
    "Unitree G1": "unitree_g1", 
    "Rainbow Y1": "rby1",
    "Allegro Hand": "freefloating_dual_allegro"
}

@app.route('/run-script', methods=['POST'])
def run_script():
    global current_process
    try:
        # Get the client's IP address

        # Get the arguments from the request JSON
        data = request.get_json()
        task = data.get('task')
        robot = data.get('robot', 'Dual Panda')
        extra = data.get('extra', '')
        mobile = data.get('mobile', "Fixed Base")

        if mobile == "Mobile": 
            robot_file_name = robot_script_mapper[robot] + "_mobile"
        else: 
            robot_file_name = robot_script_mapper[robot]

        client_ip = data.get('ip')

        logger.info(f'Request received from IP: {client_ip}')
        
        if not task:
            return jsonify({'error': 'task is required'}), 400


        my_env  = os.environ.copy()


        # Construct the command with the provided task and client IP
        if IS_MAC:
            command = ['mjpython', '-m', 'dart_physics.runs.example_teleop', '--task', task, '--robot', robot_file_name, '--avp', '--th', extra, '--headless'] 
        else:
            command = ['python', '-m','dart_physics.runs.teleop', '--task', task, '--robot', robot_file_name, '--headless', '--avp', '--th', extra] 


        # Run the script using subprocess
        logger.info(f"command: {command}") 
        current_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env = my_env) 
        logger.info(f'started MuJoCo process.') 

        def log_subprocess_output(pipe):
            for line in iter(pipe.readline, ''):
                logger.info(line.strip())

        # Log stdout and stderr asynchronously 
        stdout_thread = threading.Thread(target=log_subprocess_output, args=(current_process.stdout,))
        stderr_thread = threading.Thread(target=log_subprocess_output, args=(current_process.stderr,))
        stdout_thread.start()
        stderr_thread.start()

        # Wait for the process to complete 
        # current_process.wait()
        # stdout_thread.join()
        # stderr_thread.join()

        return jsonify({'message': 'Script started successfully', 'client_ip': client_ip})
    
    except Exception as e:
        logger.error(f'Error running script: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/kill-script', methods=['POST'])
def kill_script():
    try:
        
        # Iterate through all running processes
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Check if the process command line matches 'python run.py'
                cmdline = proc.info['cmdline']
                if cmdline and cmdline[0] == 'python' and 'dart_physics.runs.teleop' in cmdline:
                    # Terminate the process
                    proc.terminate()
                    proc.wait()
                    logger.info(f'Terminated process {proc.pid}')
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return jsonify({'message': 'All run.py scripts terminated successfully'})
    
    except Exception as e:
        logger.error(f'Error terminating script: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/list-files', methods=['GET'])
def list_files():
    logger.info(f'Got request to list files.')
    cfg_path = CUR_PATH / "cfgs"
    try:
        files = os.listdir(cfg_path)
        yaml_files = [f[:-5] for f in files if f.endswith('.yaml')] +  [f[:-3] for f in files if f.endswith('.py') and f != "__init__.py"]

        # if dummy.py exists, remove it from the list 
        if 'dummy' in yaml_files:
            yaml_files.remove('dummy')

        # List PNG files
        images = {}
        image_files = [f[:-4] for f in files if f.endswith('.png')]
        for img_file in image_files:
            with open(os.path.join(cfg_path, img_file+'.png'), "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                images[img_file] = encoded_string
        logger.info(f'Files listed: {files} and images: {list(images.keys())}')
        return jsonify({'files': yaml_files, 'images': images})
    
    except Exception as e:
        logger.error(f'Error listing files: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/get-objects', methods=['POST'])
def get_objects():
    """
    # request input:  {"task": "task_name"}
    # response output: {"objects": ["object1", "object2", ...]}
    # retreive object by reading the yaml file 
    # yaml file located in "../sim/cfgs/task_name.yaml"
    # look for key "objects" in the yaml file
    """

    try:
        data = request.get_json()
        task = data.get('task')
        if not task:
            return jsonify({'error': 'task is required'}), 400

        
        # file_path = f"cfgs/{task}.yaml"
        # with open(file_path, 'r') as file:
        #     cfg = yaml.safe_load(file)

        cfg = load_task_cfg(task)

        objects = cfg.get('objects', [])

        objects_to_load = [] 
        for obj in objects: 

            body_dict = cfg.get('object_meshes',  {})
            if obj in body_dict.keys():
                bodies = body_dict[obj]
                
                for body in bodies: 
                    objects_to_load.append(obj + '_' + body)
            else:
                objects_to_load.append(obj)

        scales = cfg.get('object_scale', {obj: 1.0 for obj in objects_to_load})
        logger.info(f'Objects for task {task}: {objects_to_load}')

        return jsonify({'objects': objects_to_load, 'scales': scales, 'task_description': cfg.get('task_description', '')})
    
    except Exception as e:
        logger.error(f'Error getting objects: {str(e)}')
        return jsonify({'error': str(e)}), 500

def handle_shutdown(signal, frame):
    global current_process
    if current_process:
        current_process.terminate()
        current_process.wait()
    os._exit(0)


@app.route('/status', methods=['GET'])
def get_status():
    logger.info(f'Got request to check status.')
    try:
        return jsonify({'status': 'Active'})
    except Exception as e:
        logger.error(f'Error getting status: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':

    # Register the signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    app.run(host='0.0.0.0', port=5012)
