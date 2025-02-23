import requests
from scientiflow_cli.services.request_handler import make_auth_request

def get_jobs() -> list[dict]:
    response = make_auth_request(endpoint="/agent-application/check-jobs-to-execute",method="GET", error_message="Unable to fetch jobs!")
    try:
        jobs = response.json()
        # breakpoint()
        if len(jobs) == 0:
            print("[+] No jobs to execute")
            return []
        else:
            print("\n{:<20} {:<20} {:<20}".format("Project Job ID", "Project Title", "Job Title"))
            print("===============      =============        =========")
            # for index, job in enumerate(response.json(), start=1):
            for job in response.json():
                project_job_id: int = job['project_job']['id']
                project_title: str = job['project']['project_title']
                job_title: str = job['project_job']['job_title']
                print("{:<20} {:<20} {:<20}".format(project_job_id, project_title, job_title))
            print("\n")
            return jobs

    except requests.exceptions.JSONDecodeError:
        print("Error fetching jobs - Invalid JSON")
        return []
