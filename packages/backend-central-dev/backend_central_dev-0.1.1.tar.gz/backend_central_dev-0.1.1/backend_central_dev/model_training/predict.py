import glob

from ..xai_sdk import (
    get_best_performed_ckpt_path,
    get_configurations_and_exp_exp_default_root_dir,
    get_task_execution_from_ticket,
    load_model_from_ckpt
)

import lightning as L
import os
from ..utils.data_utils import get_tensor_from_flask_file_storage
import torch.nn.functional as F
from ..constant import *


def predict(_, publisher_endpoint_url, task_parameters):
    L.seed_everything(42)
    model_training_execution_ticket = task_parameters[TaskExecution.previous_task_ticket]
    request = task_parameters['request']
    image = request.files['image']
    model_training_execution_parameters = get_task_execution_from_ticket(
        publisher_endpoint_url, model_training_execution_ticket
    )[TaskExecution.task_parameters]

    datamodule_class, datamodule_cfg, model_cfg, trainer_cfg, exp_default_root_dir = \
        get_configurations_and_exp_exp_default_root_dir(
            publisher_endpoint_url, model_training_execution_parameters)
    datamodule = datamodule_class(**datamodule_cfg)

    model_check_points_dir = os.path.join(
        exp_default_root_dir, 'lightning_logs',
        model_training_execution_ticket, "checkpoints"
    )
    ckpt_path = get_best_performed_ckpt_path(model_check_points_dir)
    model = load_model_from_ckpt(
        model_cfg, datamodule, ckpt_path,
        os.path.join(os.environ["COMPONENT_ROOT_PATH"], "model.py")
    )

    model.eval()
    image_tensor, image_save_path = get_tensor_from_flask_file_storage(
        model_training_execution_ticket, image, datamodule)
    output = model(image_tensor.to(model.device))
    result = {
        "prediction": output[0].argmax().item(),
        "prediction_softmax": F.softmax(output[0], dim=0).detach().cpu().tolist(),
        "class_labels": datamodule_class.dataset_class.class_labels
    }

    try:
        os.remove(image_save_path)
    except OSError:
        pass
    return result
