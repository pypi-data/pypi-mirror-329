import requests
import os
from time import perf_counter

def get_filename_from_response(response):
    """Extract filename from Content-Disposition header if available."""
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        filename_part = content_disposition.split('filename=')[-1]
        filename = filename_part.strip('"')  # Clean up the filename
        return filename
    return "output.zip"  # Fallback if no filename is provided

def generate_scene():
    url = "http://172.178.76.173:8080/generate-obj-zip"
    data = {
        "text_prompt": "A flat plane showing a plate with cookies, a laptop, a water bottle, a charger, a pencil case, and a smartphone."
    }
    try:
        start_time = perf_counter()
        response = requests.post(url, data=data)
        end_time = perf_counter()
        print(f"[INFO] POST /generate-obj-zip completed in {end_time - start_time:.4f} seconds")

        if response.status_code == 200:
            print("[INFO] Scene generated successfully!")
            output_dir = os.getcwd()

            filename = get_filename_from_response(response)
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"[INFO] OBJ file saved as {filepath}")
        else:
            print(f"[ERROR] Failed to generate scene. Status code: {response.status_code}")
            print(f"[ERROR] Error detail: {response.json()}")
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")

if __name__ == "__main__":
    generate_scene()
