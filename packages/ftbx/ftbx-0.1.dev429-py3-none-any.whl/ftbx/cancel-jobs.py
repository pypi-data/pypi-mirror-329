from src._environment import Environment
from src._objects import Objects, ObjectType, SubItems
from tqdm import tqdm

wbdev = Environment.from_env_file("wb-dev")

jobs_to_cancel = Objects(
    object_type=ObjectType.JOBS,
    sub_items=SubItems.JOBS,
    filters={"name": "test-purge-script", "status": "Failed", "exactNameMatch": True},
    mode="partial",
)
jobs_to_cancel = jobs_to_cancel.get_from(environment=wbdev)

for job in tqdm(jobs_to_cancel, desc="Cancelling jobs"):
    job.cancel(environment=wbdev)
