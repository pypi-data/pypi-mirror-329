import subprocess
from pathlib import Path
from scientiflow_cli.services.request_handler import make_auth_request

def get_job_containers(job: dict) -> None:
    base_dir = Path(job['server']['base_directory'])
    containers_dir = base_dir / "containers"
    project_job_id = job['project_job']['id']
    if not containers_dir.exists():
        containers_dir.mkdir()

    # Get names of containers already available in the user's machine
    avail_containers: set[str] = {item.name for item in containers_dir.iterdir() if item.is_file()}
    params = {"project_job_id": project_job_id}
    response = make_auth_request(endpoint="/agent-application/get-user-containers", method="GET", params=params, error_message="Unable to get containers info!")
    try:
      if response.status_code == 200:
          container_info = response.json()

          if not container_info:
              print("[X] No containers found for current User / Project")
              return
          
          current_pipeline_containers = set(container_info["current_pipeline_containers"])
          user_all_containers = set(container_info["user_all_unique_containers"])

          # Remove containers that are not needed but are present on the current machine
          containers_to_remove = avail_containers - user_all_containers
          for container_name in containers_to_remove:
              container_path = base_dir / "containers" / container_name
              container_path.unlink() # Unlinking means deleting
              
          # Download containers which are not present on the user's machine
          containers_to_download = current_pipeline_containers - avail_containers

          for container_name in container_info['container_image_details']:
              if container_name['image_name'] in containers_to_download:
                  command = f"singularity pull {container_name['image_name']}.sif {container_name['sylabs_uri']}"
                  command = command.split()
                  print(f"[+] Downloading container {container_name['image_name']}")
                  subprocess.run(command, check=True, cwd=containers_dir)
                  print("Done") 
               
    except subprocess.CalledProcessError:
        print("[x] Error executing singularity commands. Try checking your singularity installation")
        return
    
    except Exception as e:
        print(f"Error: {e}")    
    
