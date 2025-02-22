from scientiflow_cli.services.request_handler import make_auth_request

def update_stopped_at_node(project_id: int, project_job_id: int, stopped_at_node: str):
    body = {"project_id": project_id, "project_job_id": project_job_id, "stopped_at_node": stopped_at_node}
    make_auth_request(endpoint="/jobs/update-stopped-at-node", method="POST", data=body,error_message="Unable to update stopped at node!")

def update_job_status(project_job_id: int, status: str):
    body = {"project_job_id": project_job_id, "status": status}
    make_auth_request(endpoint="/agent-application/update-project-job-status",method="POST",data=body,error_message="Unable to update job status!")
    print("[+] Project status updated successfully.")
