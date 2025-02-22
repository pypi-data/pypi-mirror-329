"""

    PROJECT: flex_toolbox
    FILENAME: test_push_command_func.py
    AUTHOR: David NAISSE
    DATE: January 05, 2024

    DESCRIPTION: push_command_func function testing
    
"""

import os.path
import shutil
import random
import json
from unittest import TestCase
from pandas import pandas
from typer.testing import CliRunner
from ftbx import ftbx
from src._environment import Environment
from src._objects import ObjectType, Objects, SubItems


runner = CliRunner()


class TestPushCommandFunc(TestCase):

    def test_push_command_func_account_property(self):
        pull = runner.invoke(ftbx, ["pull", "accountProperties", "--from", "cs-sbx"])

        assert pull.exit_code == 0

        push = runner.invoke(
            ftbx,
            [
                "push",
                "accountProperties",
                "ftbx-account-property",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
            ],
        )

        assert (
            push.exit_code == 0
            and len(os.listdir("cs-sbx/accountProperties/ftbx-account-property/backup"))
            >= 1
        )

        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_job_listen(self):
        launch = runner.invoke(
            ftbx,
            [
                "launch",
                "jobs",
                "ftbx-script-completes",
                "--in",
                "cs-sbx",
                "--listen",
            ],
            input="y",
        )

        assert launch.exit_code == 0

        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_actions_with_jars_and_imports(self):
        # ins
        pull = runner.invoke(
            ftbx,
            ["pull", "actions", "--filters", "name=ftbx-script", "--from", "cs-sbx"],
        )

        push = runner.invoke(
            ftbx,
            ["push", "actions", "ftbx-script", "--from", "cs-sbx", "--to", "cs-sbx"],
        )

        # test
        assert (
            pull.exit_code == 0
            and push.exit_code == 0
            and os.path.isdir("cs-sbx")
            and len(
                os.listdir(os.path.join("cs-sbx", "actions", "ftbx-script", "backup"))
            )
            >= 1
        )

        # reset
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_assets_metadata(self):
        # ins
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "assets",
                "--filters",
                "id=911",
                "--filters",
                "name=ftbx-asset",
                "--from",
                "cs-sbx",
            ],
        )

        # gen random number and update md
        rint = random.randint(0, 100)
        with open(
            os.path.join("cs-sbx", "assets", "911", "metadata.json"), "r"
        ) as json_metadata_file:
            metadata = json.load(json_metadata_file)
        metadata["integer-field"] = rint
        with open(
            os.path.join("cs-sbx", "assets", "911", "metadata.json"), "w"
        ) as updated_json_metadata_file:
            json.dump(metadata, updated_json_metadata_file, indent=4)

        push = runner.invoke(
            ftbx, ["push", "assets", "911", "--from", "cs-sbx", "--to", "cs-sbx"]
        )

        # test
        assert (
            pull.exit_code == 0
            and push.exit_code == 0
            and os.path.isdir(os.path.join("cs-sbx", "assets", "911"))
            and len(
                Objects(
                    object_type=ObjectType.ASSETS,
                    sub_items=SubItems.ASSETS,
                    filters={"id": 911},
                    post_filters=[f"metadata.instance.integer-field={rint}"],
                    mode="full",
                ).get_from(environment=Environment.from_env_file(environment="cs-sbx"))
            )
            == 1
        )

        # reset
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_new_actions(self):
        # ins
        env = Environment.from_env_file("cs-sbx")
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script-recreate",
                "--from",
                "cs-sbx",
            ],
        )

        # disable and delete
        script_recreate_request = Objects(
            object_type=ObjectType.ACTIONS,
            sub_items=SubItems.ACTIONS,
            filters={"name": "ftbx-script-recreate", "exactNameMatch": True},
            mode="full",
        )
        script_recreate = script_recreate_request.get_from(environment=env)[0]
        script_recreate.disable(environment=env)
        script_recreate.delete(environment=env)

        # recreate
        push = runner.invoke(
            ftbx,
            [
                "push",
                "actions",
                "ftbx-script-recreate",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
            ],
        )

        # test
        assert (
            pull.exit_code == 0
            and push.exit_code == 0
            and os.path.isdir(os.path.join("cs-sbx", "actions", "ftbx-script-recreate"))
            and len(script_recreate_request.get_from(environment=env)) == 1
        )

        # reset
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_scripted_wait(self):
        # ins
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-wait-script",
                "--from",
                "cs-sbx",
            ],
        )

        push = runner.invoke(
            ftbx,
            [
                "push",
                "actions",
                "ftbx-wait-script",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
            ],
        )

        # test
        assert (
            pull.exit_code == 0
            and push.exit_code == 0
            and os.path.isfile(
                os.path.join("cs-sbx", "actions", "ftbx-wait-script", "script.groovy")
            )
        )

        # reset
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_tasks_status(self):
        # ins
        env = Environment.from_env_file(environment="cs-sbx")
        pull = runner.invoke(
            ftbx, ["pull", "tasks", "--filters", "id=552", "--from", "cs-sbx"]
        )

        # set to taken
        with open(os.path.join("cs-sbx", "tasks", "552", "_object.json"), "r") as file:
            config = json.load(file)
        config["status"] = "Taken"
        with open(os.path.join("cs-sbx", "tasks", "552", "_object.json"), "w") as file:
            json.dump(config, file, indent=4)

        push = runner.invoke(
            ftbx, ["push", "tasks", "552", "--from", "cs-sbx", "--to", "cs-sbx"]
        )

        # test
        assert (
            pull.exit_code == 0
            and push.exit_code == 0
            and len(
                Objects(
                    object_type=ObjectType.TASKS,
                    sub_items=SubItems.TASKS,
                    filters={
                        "id": 552,
                        "name": "task",
                        "status": "Taken",
                        "exactNameMatch": True,
                    },
                ).get_from(environment=env)
            )
            == 1
        )

        # reset
        with open(os.path.join("cs-sbx", "tasks", "552", "_object.json"), "r") as file:
            config = json.load(file)
        config["status"] = "Available"
        with open(os.path.join("cs-sbx", "tasks", "552", "_object.json"), "w") as file:
            json.dump(config, file, indent=4)

        push = runner.invoke(
            ftbx, ["push", "tasks", "552", "--from", "cs-sbx", "--to", "cs-sbx"]
        )

        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_metadata_definitions(self):
        # ins
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "metadataDefinitions",
                "--filters",
                "name=ftbx-metadata-definition-asset",
                "--from",
                "cs-sbx",
            ],
        )

        push = runner.invoke(
            ftbx,
            [
                "push",
                "metadataDefinitions",
                "ftbx-metadata-definition-asset",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
            ],
        )

        # tests
        assert pull.exit_code == 0 and push.exit_code == 0

        # reset
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_push_to_failed_jobs(self):
        # ins
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script-fails",
                "--from",
                "cs-sbx",
            ],
        )

        push = runner.invoke(
            ftbx,
            [
                "push",
                "actions",
                "ftbx-script-fails",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
                "--push-to-failed-jobs",
                "all",
            ],
        )

        # tests
        assert pull.exit_code == 0 and push.exit_code == 0

        # reset
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_push_to_failed_jobs_csv(self):
        # ins
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script-fails",
                "--from",
                "cs-sbx",
            ],
        )

        df = pandas.DataFrame([{"id": 819}, {"id": 730}, {"id": 724}])
        df.to_csv("failed_jobs_to_update.csv")

        push = runner.invoke(
            ftbx,
            [
                "push",
                "actions",
                "ftbx-script-fails",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
                "--push-to-failed-jobs",
                "failed_jobs_to_update.csv",
            ],
        )

        # tests
        assert pull.exit_code == 0 and push.exit_code == 0

        # reset
        os.remove("failed_jobs_to_update.csv")
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_push_to_failed_jobs_json(self):
        # ins
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script-fails",
                "--from",
                "cs-sbx",
            ],
        )

        with open("failed_jobs_to_update.json", "w") as json_file:
            json.dump([{"id": 819}, {"id": 730}, {"id": 724}], json_file)

        push = runner.invoke(
            ftbx,
            [
                "push",
                "actions",
                "ftbx-script-fails",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
                "--push-to-failed-jobs",
                "failed_jobs_to_update.json",
            ],
        )

        # tests
        assert pull.exit_code == 0 and push.exit_code == 0

        # reset
        os.remove("failed_jobs_to_update.json")
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_push_command_func_with_dependencies(self):

        # ins
        env = Environment.from_env_file(environment="cs-sbx")
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "workflowDefinitions",
                "--filters",
                "name=ftbx-workflow-pull-with-dependencies",
                "--from",
                "cs-sbx",
                "--with-dependencies",
            ],
        )

        assert pull.exit_code == 0

        objects_to_delete = [
            ("workflowDefinitions", "ftbx-workflow-pull-with-dependencies"),
            ("actions", "ftbx-create-placeholder"),
            ("actions", "ftbx-create-proxy"),
            ("actions", "ftbx-extract-technical-metadata"),
            ("actions", "ftbx-import-asset"),
            ("actions", "ftbx-multi-decision"),
            ("actions", "ftbx-script"),
            ("profiles", "ftbx-profile"),
            ("resources", "ftbx-folder-resource"),
            ("resources", "ftbx-fsp"),
            ("resources", "ftbx-resource"),
            ("taskDefinitions", "ftbx-task-dependency"),
            ("wizards", "ftbx-wizard-task-dependency"),
        ]

        # delete everything
        for object_type_str, object_name in objects_to_delete:
            object_type = ObjectType.from_string(string=object_type_str)
            object = Objects(
                object_type=object_type,
                sub_items=SubItems.from_object_type(object_type),
                filters={"name": object_name, "exactNameMatch": True},
                mode="partial",
            ).get_from(env)[0]
            object.stop(env)
            object.disable(env)
            object.delete(env)

        push = runner.invoke(
            ftbx,
            [
                "push",
                "workflowDefinitions",
                "ftbx-workflow-pull-with-dependencies",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
                "--with-dependencies",
            ],
        )

        # test
        assert push.exit_code == 0

        # reset
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)
