import argparse
from scientiflow_cli.cli.login import login_user
from scientiflow_cli.cli.logout import logout_user
from scientiflow_cli.pipeline.get_jobs import get_jobs
from scientiflow_cli.services.executor import execute_jobs, execute_jobs_sync, execute_job_id
from scientiflow_cli.services.set_base_directory import set_base_directory
from scientiflow_cli.utils.singularity import install_singularity_main as install_singularity

def main():
    parser = argparse.ArgumentParser(description="Scientiflow Agent CLI")
    parser.formatter_class = lambda prog: argparse.HelpFormatter(prog, max_help_position=50)

    parser.add_argument('--login', action='store_true', help="Login using your scientiflow credentials")
    parser.add_argument('--logout', action='store_true', help="Logout from scientiflow")
    parser.add_argument('--list-jobs', action='store_true', help="Get jobs to execute")
    parser.add_argument('--set-base-directory', action='store_true', help="Set the base directory to the current working directory")
    parser.add_argument('--execute-jobs', action='store_true', help="Fetch and execute pending jobs")
    parser.add_argument('--execute-jobs-sync', action='store_true', help="Fetch and execute pending jobs synchronously in order of their job id")
    parser.add_argument('--execute-job-by-id', type=int, dest='Job_ID', help="Fetch and execute job with a specific job id")
    parser.add_argument('--install-singularity', action='store_true', help="Install Singularity")
    args = parser.parse_args()

    try:
        if args.login:
            login_user()
        
        elif args.logout:
            logout_user()

        elif args.list_jobs:
            get_jobs()

        elif args.set_base_directory:
            set_base_directory()

        elif args.execute_jobs:
            execute_jobs()
            
        elif args.execute_jobs_sync:
            execute_jobs_sync()

        elif args.Job_ID:
            execute_job_id(job_id = args.Job_ID)

        elif args.install_singularity:
            install_singularity()

        else:
            print("No arguments specified. Use --help to see available options")
    
    except Exception as e:
        print("Error: ", e)
        return


if __name__ == "__main__":
    main()

