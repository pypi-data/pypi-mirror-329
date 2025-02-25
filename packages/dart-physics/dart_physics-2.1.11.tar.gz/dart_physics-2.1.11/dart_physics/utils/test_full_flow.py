import requests
from time import perf_counter

def test_generate_scene():
    url = "http://172.178.76.173:8080/generate-scene"
    data = {
        "text_prompt": "A forest scene."
    }
    try:
        start_time = perf_counter()
        response = requests.post(url, data=data)
        end_time = perf_counter()
        print(f"[INFO] POST /generate-scene completed in {end_time - start_time:.4f} seconds")

        if response.status_code == 200:
            print("[INFO] Scene generated successfully!")
            with open("output_scene.glb", "wb") as f:
                f.write(response.content)
            print("[INFO] GLB file saved as 'output_scene.glb'")
        else:
            print(f"[ERROR] Failed to generate scene. Status code: {response.status_code}")
            print(f"[ERROR] Error detail: {response.json()}")
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")

if __name__ == "__main__":
    test_generate_scene()
