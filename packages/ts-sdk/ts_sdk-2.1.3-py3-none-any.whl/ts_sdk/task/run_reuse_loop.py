import multiprocessing
import os
import shutil
import sys
import tempfile
import traceback
from threading import Timer

from .__task_script_runner import run
from .__util_log import Log
from .__util_task import (
    ContainerStoppedException,
    extend_task_timeout,
    poll_task,
    update_task_status,
    FailedPollTaskException,
)

log = Log({})


def get_run_params(task):
    params = {
        "input": task.get("input"),
        "context_from_arg": task.get("context"),
        "func": task.get("func"),
        "correlation_id": task.get("correlation_id"),
        "func_dir": task.get("func_dir"),
        "store_output": False,
        "storage_type": os.environ.get("TASK_STORAGE_TYPE"),
        "storage_bucket": os.environ.get("TASK_STORAGE_S3FILE_BUCKET"),
        "storage_file_key": os.environ.get("TASK_STORAGE_S3FILE_FILE_KEY"),
        "storage_endpoint": os.environ.get("TASK_STORAGE_S3FILE_ENDPOINT"),
        "artifact_bucket": os.environ.get("ARTIFACT_S3FILE_BUCKET"),
        "artifact_prefix": os.environ.get("ARTIFACT_S3FILE_PREFIX"),
        "artifact_endpoint": os.environ.get("ARTIFACT_S3FILE_ENDPOINT"),
        "artifact_file_key": os.environ.get("ARTIFACT_IDS_SCHEMA_S3FILE_FILE_KEY"),
        "artifact_bucket_private": os.environ.get("ARTIFACT_S3FILE_BUCKET_PRIVATE"),
        "artifact_prefix_private": os.environ.get("ARTIFACT_S3FILE_PREFIX_PRIVATE"),
        "artifact_endpoint_private": os.environ.get("ARTIFACT_S3FILE_ENDPOINT_PRIVATE"),
    }

    return params


def healtcheck_worker(run_state):
    run_state["healtcheck_timer"] = None
    task = run_state["task"]
    task_process = run_state["task_process"]

    if task and task_process:
        task_id = task.get("id")
        try:
            extend_task_timeout(task)
        except:
            log.log(f"Error during timeout extension -> killing task {task_id}")
            task_process.kill()

    healtcheck_timer = Timer(60.0, healtcheck_worker, [run_state])
    run_state["healtcheck_timer"] = healtcheck_timer
    healtcheck_timer.start()


def task_process_fn(task, shared_dict):
    task_tmp_dir = tempfile.mkdtemp()
    os.environ.update({"TMPDIR": task_tmp_dir})

    run_params = get_run_params(task)
    sys.path.append(run_params.get("func_dir"))
    try:
        shared_dict["result"] = run(**run_params)
    except:
        e = sys.exc_info()[1]
        log.log(log.generate_error(e))
        shared_dict["error"] = traceback.format_exc()
    finally:
        sys.path.remove(run_params.get("func_dir"))
        shutil.rmtree(task_tmp_dir, ignore_errors=True)


def main():
    manager = multiprocessing.Manager()

    shared_dict = manager.dict({"result": None, "error": None})
    run_state = {"task_process": None, "task": None, "healtcheck_timer": None}

    healtcheck_worker(run_state)

    while True:
        try:
            task = poll_task()
        except ContainerStoppedException:
            log.log("Container is stopped - exiting...")
            break
        except FailedPollTaskException:
            log.log("Cannot poll task - exiting...")
            break

        if task:
            task_id = task.get("id")
            log.log({"level": "debug", "message": f"Got new task {task_id}"})

            shared_dict["result"] = None
            shared_dict["error"] = None

            run_state["task"] = task
            task_process = multiprocessing.Process(
                name=f"task-{task_id}", target=task_process_fn, args=(task, shared_dict)
            )
            run_state["task_process"] = task_process
            task_process.start()
            task_process.join()

            log.log({"level": "debug", "message": f"Task {task_id} process completed"})

            run_state["task_process"] = None
            run_state["task"] = None

            exitcode = task_process.exitcode
            if exitcode != 0:
                if exitcode == -9 or exitcode == 137:
                    exitcode = 137
                    result = {
                        "error": {
                            "message": {
                                "text": f"Invalid exit code {exitcode}",
                                "oomError": True,
                            }
                        }
                    }
                else:
                    result = {"error": f"Invalid exit code {exitcode}"}
                update_task_status(
                    task,
                    {
                        "status": "failed",
                        "exitCode": exitcode,
                        "result": result,
                    },
                )
                continue

            if shared_dict["result"] != None:
                update_task_status(task, {"exitCode": 0, **shared_dict["result"]})
            else:
                update_task_status(
                    task,
                    {
                        "status": "failed",
                        "exitCode": 0,
                        "result": {
                            "error": (
                                shared_dict["error"]
                                if shared_dict["error"]
                                else "No content returned by worker"
                            )
                        },
                    },
                )

    if run_state["healtcheck_timer"] and run_state["healtcheck_timer"].is_alive():
        run_state["healtcheck_timer"].cancel()

    return shared_dict


if __name__ == "__main__":
    main()
