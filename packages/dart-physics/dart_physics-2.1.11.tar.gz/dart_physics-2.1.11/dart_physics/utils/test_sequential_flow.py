import os
import requests
from time import perf_counter

def generate_blockout_api(text_prompt, api_url, image_file_path=None):
    start_time = perf_counter()
    url = f"{api_url}/generate-blockout"
    data = {
        "text_prompt": text_prompt
    }
    files = None
    if image_file_path:
        files = {"image_file": open(image_file_path, "rb")}
    response = requests.post(url, data=data, files=files)
    response.raise_for_status()
    session_code = response.headers.get("Session-Code")
    output_glb_file_path = f"./outputs/{session_code}/output_scene.glb"
    output_dir = f"./outputs/{session_code}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_glb_file_path, "wb") as f:
        f.write(response.content)
    end_time = perf_counter()
    print(f"[INFO] generate_blockout_api completed in {end_time - start_time:.4f} seconds")
    return session_code, output_glb_file_path

def generate_cube_scene_api(session_code, glb_file_path, api_url, mesh_style_prompt=None):
    start_time = perf_counter()
    if not os.path.exists(glb_file_path):
        raise FileNotFoundError(f"GLB file not found: {glb_file_path}")
    url = f"{api_url}/generate-cube-scene"
    data = {
        "session_code": session_code,
        "mesh_style_prompt": mesh_style_prompt
    }
    files = {"glb_file": open(glb_file_path, "rb")}
    response = requests.post(url, data=data, files=files)
    response.raise_for_status()
    final_glb_file_path = f"./outputs/{session_code}/final_output_scene.glb"
    with open(final_glb_file_path, "wb") as f:
        f.write(response.content)
    end_time = perf_counter()
    print(f"[INFO] generate_cube_scene_api completed in {end_time - start_time:.4f} seconds")
    return final_glb_file_path

def main():
    try:
        overall_start_time = perf_counter()
        api_url = "http://172.178.76.173:8080"
        text_prompt = "Dishes and forks"
        session_code, initial_glb_file_path = generate_blockout_api(text_prompt, api_url)
        print(f"[INFO] Blockout generated with session code: {session_code}, GLB saved at: {initial_glb_file_path}")
        final_glb_file_path = generate_cube_scene_api(session_code, initial_glb_file_path, api_url)
        print(f"[INFO] Final scene generated and saved at: {final_glb_file_path}")
        overall_end_time = perf_counter()
        print(f"[INFO] Total execution time: {overall_end_time - overall_start_time:.4f} seconds")
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
