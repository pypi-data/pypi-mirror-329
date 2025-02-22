from dask.distributed import Client, LocalCluster
from dask_jobqueue import SLURMCluster
import s3fs
import os
from dotenv import load_dotenv

def get_default_cluster_options(queue):
    """
    Get default cluster options based on the specified queue.

    Parameters:
    - queue (str): The queue for which to retrieve default options.

    Returns:
    - dict: A dictionary containing default cluster options (cores, memory, walltime).
    """
    default_options = {
        "rome": {"cores": 62, "memory": "220GB", "walltime": "08:00:00"},
        "ivyshort": {"cores": 40, "memory": "60GB", "walltime": "48:00:00"},
        "ccgp": {"cores": 38, "memory": "170GB", "walltime": "48:00:00"},
        "cclake": {"cores": 38, "memory": "170GB", "walltime": "48:00:00"},
        "haswell": {"cores": 40, "memory": "120GB", "walltime": "48:00:00"},
        "ivy": {"cores": 40, "memory": "60GB", "walltime": "48:00:00"},
        "fat": {"cores": 96, "memory": "800GB", "walltime": "48:00:00"},
        "milan": {"cores": 40, "memory": "120GB", "walltime": "12:00:00"},
    }
    return default_options.get(queue, {})

                
def getCluster(queue, nodes, jobs_per_node, scheduler_file=None, walltime=None, cores=None, memory=None):
    """
    Set up a Dask cluster for SLURM or local execution.

    Parameters:
    - queue (str): The queue to which to submit the job or 'local' for local execution.
    - nodes (int): Number of nodes requested for the current workflow.
    - jobs_per_node (int): Number of jobs submitted to a single node.
    - scheduler_file (str, optional): Path to a scheduler file for an existing Dask cluster.
    - walltime (str, optional): Walltime for SLURM jobs.
    - cores (int, optional): Number of cores for SLURM jobs.
    - memory (str, optional): Memory specification for SLURM jobs.

    Returns:
    - client (Client): Object for interacting with HPC resources and submitting jobs.
    - cluster (SLURMCluster or LocalCluster): Object with information about the cluster infrastructure.

    Usage Example:
    ```python
    client, cluster = getCluster('rome', 2, 4)
    ```
    """
    if scheduler_file is not None:
        client = Client(scheduler_file=scheduler_file)
        cluster = None
    
    else:
        if queue == "local":
            client = None
            cluster = LocalCluster()
        else:
            
            default_options = get_default_cluster_options(queue)
            
            cores = cores or default_options.get("cores")
            memory = memory or default_options.get("memory")
            walltime = walltime or default_options.get("walltime")
            
            workers = nodes * jobs_per_node

            cluster = SLURMCluster(
                cores=cores,
                memory=memory,
                processes=jobs_per_node,
                queue=queue,
                walltime=walltime,
            )

            cluster.scale(n=workers)
            client = Client(cluster)
            
    if client is not None:
        client.get_versions(check=True)
        client.amm.start()

    return client, cluster


def s3_init():
    """
    Initialize and configure an S3FileSystem instance for interacting with an S3-compatible storage.

    Returns:
    s3fs.core.S3FileSystem: An S3FileSystem instance configured with the provided access key,
                            secret key, region, endpoint URL, and verification settings.

    Example:
    
    .. code-block:: python

        s3_instance = s3_init()
        file_list = s3_instance.ls("s3://your-bucket-name/")
        print("List of files in the bucket:", file_list)

    Note:
    - Replace the access key, secret key, region, and endpoint URL with your specific credentials
      and S3-compatible storage information.
    - The 'verify' parameter is set to 'False' to disable SSL certificate verification. Adjust
      accordingly based on your security requirements.
    """
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    load_dotenv(dotenv_path)

    access_key = os.getenv("S3_ACCESS_KEY_ID")
    secret_key = os.getenv("S3_SECRET_ACCESS_KEY")
    region = os.getenv("S3_REGION")
    endpoint_url = os.getenv("S3_ENDPOINT_URL")

    s3 = s3fs.S3FileSystem(
        key=access_key,
        secret=secret_key,
        client_kwargs=dict(
            region_name=region,
            endpoint_url=endpoint_url,
            verify=False,
        ),
    )

    return s3
