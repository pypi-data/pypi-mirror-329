import pandas

from src._environment import Environment
from src._objects import ObjectType, Objects
from tqdm import tqdm

df = pandas.read_csv("ORPHANED_XMLS_2.txt", sep="\t")

orphans = []

for idx, row in tqdm(df.iterrows(), desc="Checking for orphans"):
    group_name = row['ORIGINAL_FILENAME_'].replace("_ingest.xml", "")
    results_rq = Objects(
        object_type=ObjectType.ASSETS,
        sub_items=[],
        filters={"fql": f"objectType.id = 2 AND name = '{group_name}'"},
    )
    results = results_rq.get_from(Environment.from_env_file(environment="wb-prod"), log=False)

    match len(results):
        case 0:
            orphans.append({'id': row['ID_'], 'name': row['ORIGINAL_FILENAME_']})
            print("+1")
        case 1:
            continue
        case _:
            print(f"WTF FOR {row['ORIGINAL_FILENAME_']}??")

orphans_csv = pandas.DataFrame(orphans)
orphans_csv.to_csv("ORPHANED_XMLS_2.csv")
