import subprocess
import threading
import time
from dotenv import dotenv_values
import glob
import os
import sys
import json
import shutil
from flask import Blueprint, request, jsonify, send_file, Flask, abort

from .utils.system_utils import getCurrentCommitHash
from .task_executor import TaskExecutor
from .constant import ExecutorRegInfo, TaskExecution, ExecutorType

from .xai_sdk import *

from flask_cors import CORS


def create_tmp_dir(service_init_path):
    basedir = os.path.abspath(os.path.dirname(service_init_path))
    tmpdir = os.path.join(basedir, "tmp")
    if not os.path.isdir(tmpdir):
        os.mkdir(tmpdir)


def load_env(mode, **kwargs):
    os.environ["ENV"] = mode
    print("App Mode: ", os.environ["ENV"])
    env_file = f".env.{os.environ['ENV']}"
    for f in glob.glob(os.path.join(os.getcwd(), "**", env_file), recursive=True):
        env_file = f

    for k, v in kwargs.items():
        os.environ[k] = v

    config = dotenv_values(env_file)
    for k in config.keys():
        if os.getenv(k) == None:
            os.environ[k] = config[k]


def set_app(app: Flask):
    # cors
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.static_folder = os.environ['COMPONENT_STATIC_PATH']


class ExecutorBluePrint(Blueprint):

    def __init__(
        self, name, import_name, component_path, *args, mongo=False, **kwargs
    ) -> None:

        # TODO: executor_name and context_path from config.json
        self.context_path = kwargs["url_prefix"]

        self.te = TaskExecutor(
            executor_name=name,
            component_path=component_path,
            context_path=self.context_path,
            mongo=mongo,
        )

        super().__init__(name, import_name, *args, **kwargs)

        self.tmp_path = self.te.tmp_path

        @self.route("/reset", methods=["GET"])
        def reset():
            self.te.reset()
            return ""

        @self.route("/get_available_task_function_key", methods=["GET"])
        def available_task_function_key():
            return jsonify(list(self.te.task_func_map.keys()))

        @self.route("/task_execution_result", methods=["GET"])
        def task_result():
            if request.method == "GET":
                task_ticket = request.args["task_ticket"]

                exp_rs_path = self.te.get_exp_rs_path(task_ticket)
                zip_path = os.path.join(
                    self.te.static_path, "rs", f"{task_ticket}.zip")

                if not os.path.exists(zip_path):
                    shutil.make_archive(
                        zip_path.replace('.zip', ''),
                        "zip",
                        exp_rs_path,
                    )

                if os.path.exists(zip_path):
                    return send_file(zip_path, as_attachment=True)
                else:
                    # TODO: should follow the restful specification
                    return "no such task"

        @self.route("/task_result_present", methods=["GET"])
        def task_result_present():
            if request.method == "GET":
                task_ticket = request.args["task_ticket"]
                pre = self.te.get_task_rs_presentation(task_ticket)
                return jsonify(pre)
            return ""

        @self.route("/task_status", methods=["GET", "POST"])
        def task_status():
            if request.method == "GET":
                task_ticket = request.args["task_ticket"]
                return jsonify(
                    {TaskExecution.task_status: self.te.get_task_actual_staus(
                        task_ticket)}
                )

        @self.route("/task_execution", methods=["GET", "POST"])
        def task():
            if request.method == "GET":
                pass
            else:
                form_data = request.form
                act = form_data["act"]
                # stop a task
                if act == "stop":
                    task_ticket = form_data[TaskExecution.task_ticket]
                    self.te.terminate_process(task_ticket)

                # execute a task which assigned by the central
                if act == "execute":
                    task_execution = json.loads(form_data["task_execution"])
                    pipeline_ticket = form_data.get("pipeline_ticket")
                    self.te.start_a_task(task_execution, pipeline_ticket)

                if act == "delete":
                    task_ticket = form_data[TaskExecution.task_ticket]
                    self.te.delete_the_task(task_ticket)

                if act == "run_sync":
                    task_function_key = form_data[TaskSheet.task_function_key]
                    task_parameters = json.loads(
                        form_data[TaskExecution.task_parameters])
                    task_parameters['request'] = request
                    task_parameters['run_mode'] = "run_sync"
                    publisher_endpoint_url = self.te.get_publisher_endpoint_url()
                    return jsonify(get_task_function(self.te.task_func_map, task_function_key)(
                        None,
                        publisher_endpoint_url,
                        task_parameters
                    ))

            return ""

        @self.route("/executor", methods=["POST"])
        def exe():
            if request.method == "POST":
                # register executor
                form_data = request.form
                act = form_data["act"]
                if act == "reg" or act == "update":
                    executor_id = form_data[ExecutorRegInfo.executor_id]
                    executor_name = form_data[ExecutorRegInfo.executor_name]
                    endpoint_type = form_data[ExecutorRegInfo.executor_type]
                    endpoint_url = form_data[ExecutorRegInfo.executor_endpoint_url]
                    executor_info = form_data[ExecutorRegInfo.executor_info]
                    publisher_endpoint_url = form_data[
                        ExecutorRegInfo.publisher_endpoint_url
                    ]
                    sys_info = self.te.keep_reg_info(
                        executor_id,
                        executor_name,
                        endpoint_type,
                        endpoint_url,
                        executor_info,
                        publisher_endpoint_url,
                    )
                    return jsonify(sys_info)

            return ""

        if self.te.component_info['executor_type'] == ExecutorType.dataset:
            @self.route("/dataset_source_file", methods=['GET'])
            def dataset_source_file():
                dataset_file = os.path.join(
                    self.te.component_path_parent, "dataset.py")
                if os.path.exists(dataset_file):
                    with open(dataset_file) as f:
                        content = f.read()
                        return content
                else:
                    abort(404)

        if self.te.component_info['executor_type'] == ExecutorType.model:
            @self.route("/model_source_file", methods=['GET'])
            def model_source_file():
                dataset_file = os.path.join(
                    self.te.component_path_parent, "model.py")
                if os.path.exists(dataset_file):
                    with open(dataset_file) as f:
                        content = f.read()
                        return content
                else:
                    abort(404)

    def get_task_executor(self):
        return self.te


def create_service(bp: ExecutorBluePrint):
    load_env(os.environ.get("ENV", "dev"))

    context_path = os.environ["CONTEXT_PATH"]
    static_url_path = context_path + "/static"

    app = Flask(
        __name__, instance_relative_config=True, static_url_path=static_url_path
    )

    set_app(app)
    app.register_blueprint(bp)

    component_dirname = os.environ['COMPONENT_ROOT_PATH']
    component_config_path = os.path.join(component_dirname, "config.json")

    bp.te.component_info[ExecutorRegInfo.executor_info]['code_version_hash'] = getCurrentCommitHash()
    print("Current code version hash: ",
          bp.te.component_info[ExecutorRegInfo.executor_info]['code_version_hash'])

    def run():
        while True:
            try:
                register_executor(
                    os.environ['CENTRAL_ADDR'], **bp.te.component_info
                )
                print("Reg succeed.")
                break
            except Exception as e:
                print("Reg failed: ", e)
                time.sleep(1)

    if os.path.exists(component_config_path):
        if "run" in sys.argv:
            threading.Thread(target=run).start()
    else:
        print("Please have the config.json ready.")
        sys.exit(1)

    return app
