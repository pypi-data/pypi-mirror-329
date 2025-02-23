from concurrent.futures import ThreadPoolExecutor
import asyncio
from scientiflow_cli.pipeline.get_jobs import get_jobs
from scientiflow_cli.pipeline.decode_and_execute import decode_and_execute_pipeline
from scientiflow_cli.pipeline.container_manager import get_job_containers
from scientiflow_cli.utils.file_manager import create_job_dirs, get_job_files


def get_all_pending_jobs() -> list[dict]:
    """
    Gets all the pending jobs using the get_jobs function
    """
    try:
        return get_jobs()

    except Exception as e:
        print("An unexpected error occurred")
        return []


def execute_jobs() -> None:
    """
    Starts the execute_jobs coroutine
    """
    asyncio.run(execute_async())


def execute_jobs_sync() -> None:
    """
    Execute all jobs synchronously and in order
    """

    all_pending_jobs: list[dict] = []
    all_pending_jobs = get_all_pending_jobs()
    all_pending_jobs = sort_jobs_by_id(all_pending_jobs)

    for job in all_pending_jobs:
        print(f"Executing job with id: {job['project']['id']}\n")
        execute_single_job(job)


def sort_jobs_by_id(all_pending_jobs: list[dict]) -> list[dict]:
    """
    Sorts all the jobs on basis of the project job id
    """

    all_pending_jobs = sorted(all_pending_jobs, key=lambda job: job['project']['id'])
    return all_pending_jobs


def store_jobs_in_dict(all_pending_jobs: list[dict]) -> dict:
    """
    Stores all the jobs in a dictionary with project job id as key
    """

    job_dict: dict[int, dict] = {}

    for job in all_pending_jobs:
        # checking if the required values are present in the job
        if 'project' not in job or 'id' not in job['project']:
            print("One or more values missing in job. Continuing without considering it.")
            continue
        
        job_dict[job['project_job']['id']] = job

    return job_dict


def execute_job_id(job_id: int) -> None:
    """
    Execute job with the given job_id
    """
    
    # Retrieve all jobs using 'get_jobs'
    all_pending_jobs: list[dict] = []
    
    all_pending_jobs = get_all_pending_jobs()

    # Store jobs in order of their job_id
    job_dict: dict[int, dict] = store_jobs_in_dict(all_pending_jobs)

    if job_id not in job_dict:
        print("Job with required job id was not found!")
        return

    execute_single_job(job_dict[job_id])
    


async def execute_async() -> None:
    """Executes the function 'execute_single_job' asynchronously."""
    
    all_pending_jobs = get_all_pending_jobs()
    
    running_jobs: list[asyncio.Task] = []  # List of running jobs

    for job in all_pending_jobs:
        job_data = execute_single_job_sync(job)

        if job_data is None:
            print(f"[SKIPPING] Job due to an error: {job}")
            continue

        base_dir, project_id, project_job_id, project_title, job_dir_name, nodes, edges, environment_variables, start_node, end_node = job_data

        print(f"[ASYNC START] Job {project_job_id} is starting...")

        # Schedule the job asynchronously
        task = asyncio.create_task(
            execute_single_job_async(
                base_dir, project_id, project_job_id, project_title, job_dir_name, nodes, edges, environment_variables, start_node, end_node
            )
        )

        running_jobs.append(task)

    await asyncio.gather(*running_jobs)  # Wait for all jobs to complete
    print("[ASYNC COMPLETE] All jobs finished!")

def execute_single_job(job: dict) -> None:

    """Function to decode and execute a job. Currently does nothing.
        Processes a job asynchronously but maintains synchronous 
        execution of the internal logic. Note: Terminal outputs will not be in order
        since multiple jobs are running simultaneously
       
       Raises:
           ValueError: If the job is missing required fields.
           RuntimeError: If the job fails during runtime
    """
    try:

        # Validate the job dictionary
        required_keys = ["server", "project", "project_job", "nodes", "edges", "new_job"]

        for key in required_keys:
            if key not in job:
                raise ValueError(f"Job is missing required key: {key}")
            

        # Store all the variables with their types
        base_dir: str = job['server']['base_directory']
        project_id: int = job['project']['id']
        project_job_id: int = job['project_job']['id']
        project_title: str = job['project']['project_title']
        job_dir_name: str = job['project_job']['job_directory']
        nodes: list[dict] = job['nodes']
        edges: list[dict] = job['edges']
        environment_variables_management: list[dict] = job['environment_variable_management']
        start_node: str = job["project_job"]['job_configuration']['start_node'] if 'job_configuration' in job["project_job"] else None
        end_node: str = job["project_job"]['job_configuration']['end_node'] if 'job_configuration' in job['project_job'] else None
        if environment_variables_management:
          environment_variables: dict = {environment_var['variable'] : environment_var['value'] for environment_var in environment_variables_management}
        else:
          environment_variables = {'variable': 't', 'type': 'text', 'value': '1AKI'}

        if job["new_job"]==1:
            # Initialize folders for the project / project_job 
            create_job_dirs(job)

        # Fetch the files and folder from the backend
        get_job_files(job)

        # Get the job containers from the backend
        get_job_containers(job)

        # Decode and execute the pipeline step by step
        asyncio.run(decode_and_execute_pipeline(base_dir, project_id, project_job_id, project_title, job_dir_name, nodes, edges, environment_variables, start_node=start_node, end_node=end_node))

    except ValueError as value_err:
        print(f"ValueError encountered while processing job: {value_err}")

    except RuntimeError as runtime_err:
        print(f"RuntimeError encountered while processing job: {runtime_err}")

    except Exception as err:
        print(err)
        print(f"An unexpected error occurred while processing job")


def execute_single_job_sync(job: dict) -> tuple:
    """Function to decode and execute a job synchronously.
       Processes a job synchronously except for the decode_and_execute_pipeline function.
       
       Raises:
           ValueError: If the job is missing required fields.
           RuntimeError: If the job fails during runtime
    """
    try:
        # Validate the job dictionary
        required_keys = ["server", "project", "project_job", "nodes", "edges", "new_job"]

        for key in required_keys:
            if key not in job:
                raise ValueError(f"Job is missing required key: {key}")

        # Store all the variables with their types
        base_dir: str = job['server']['base_directory']
        project_id: int = job['project']['id']
        project_job_id: int = job['project_job']['id']
        project_title: str = job['project']['project_title']
        job_dir_name: str = job['project_job']['job_directory']
        nodes: list[dict] = job['nodes']
        edges: list[dict] = job['edges']
        environment_variables_management: list[dict] = job['environment_variable_management']
        start_node: str = job["project_job"]['job_configuration']['start_node'] if 'job_configuration' in job["project_job"] else None
        end_node: str = job["project_job"]['job_configuration']['end_node'] if 'job_configuration' in job['project_job'] else None
        if environment_variables_management:
            environment_variables: dict = {environment_var['variable']: environment_var['value'] for environment_var in environment_variables_management}
        else:
            environment_variables = {'variable': 't', 'type': 'text', 'value': '1AKI'}

        if job["new_job"] == 1:
            # Initialize folders for the project / project_job 
            create_job_dirs(job)

        # Fetch the files and folder from the backend
        get_job_files(job)

        # Get the job containers from the backend
        get_job_containers(job)

        return base_dir, project_id, project_job_id, project_title, job_dir_name, nodes, edges, environment_variables, start_node, end_node

    except ValueError as value_err:
        print(f"ValueError encountered while processing job: {value_err}")

    except RuntimeError as runtime_err:
        print(f"RuntimeError encountered while processing job: {runtime_err}")

    except Exception as err:
        print(err)
        print(f"An unexpected error occurred while processing job")
        return None


async def execute_single_job_async(base_dir, project_id, project_job_id, project_title, job_dir_name, nodes, edges, environment_variables, start_node, end_node) -> None:
    """Function to decode and execute a job asynchronously."""
    try:
        print(f"[ASYNC RUNNING] Job {project_job_id} is executing...")

        # Ensure this function runs asynchronously (if it's blocking)
        await asyncio.to_thread(
            decode_and_execute_pipeline,
            base_dir, project_id, project_job_id, project_title, job_dir_name, nodes, edges, environment_variables, start_node, end_node
        )

        print(f"[ASYNC FINISHED] Job {project_job_id} is done!")

    except Exception as err:
        print(f"[ERROR] Job {project_job_id} failed: {err}")
